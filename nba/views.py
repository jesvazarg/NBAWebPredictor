from django.db.models import Value, CharField, F, Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import Season, SeasonMonth, Team, Player, TeamHist, PlayerHist, Game, ThreePointerPlay, TwoPointerPlay, \
    FreeThrowPlay, ReboundPlay, TurnoverPlay, FoulPlay


def welcome(request):
    games_predicted = Game.objects.filter(prediction__isnull=False)
    accuracy = 0
    if games_predicted.count() > 0:
        well_predicted_games_v = games_predicted.filter(visitor_point__gt=F('home_point')).\
            filter(prediction=F('visitor_team_id')).count()
        well_predicted_games_h = games_predicted.filter(home_point__gt=F('visitor_point')).\
            filter(prediction=F('home_team_id')).count()
        accuracy = ((well_predicted_games_v + well_predicted_games_h) / games_predicted.count()) * 100

    return render(request, 'nba/welcome.html', {'games_predicted': games_predicted.count(), 'accuracy': accuracy})


def team_list(request):
    atlantic_division = Team.objects.filter(division='AT').order_by('name')
    central_division = Team.objects.filter(division='CE').order_by('name')
    southeast_division = Team.objects.filter(division='SE').order_by('name')
    northwest_division = Team.objects.filter(division='NW').order_by('name')
    pacific_division = Team.objects.filter(division='PA').order_by('name')
    southwest_division = Team.objects.filter(division='SW').order_by('name')

    return render(request, 'nba/team_list.html',
                  {'atlantic_division': atlantic_division, 'central_division': central_division
                      , 'southeast_division': southeast_division, 'northwest_division': northwest_division
                      , 'pacific_division': pacific_division, 'southwest_division': southwest_division})


def team(request, team_id: str):
    max_season = Season.objects.latest('id')
    months = SeasonMonth.objects.filter(season_id=max_season.id)

    team = get_object_or_404(Team, id=team_id)
    team.victory = Game.objects.filter(season_month_id__in=months).filter(visitor_team_id=team.id).\
                       filter(visitor_point__gt=F('home_point')).count() + \
                   Game.objects.filter(season_month_id__in=months).filter(home_team_id=team.id).\
                       filter(home_point__gt=F('visitor_point')).count()
    team.defeat = Game.objects.filter(season_month_id__in=months).filter(visitor_team_id=team.id).\
                      filter(home_point__gt=F('visitor_point')).count() + \
                   Game.objects.filter(season_month_id__in=months).filter(home_team_id=team.id).\
                       filter(visitor_point__gt=F('home_point')).count()

    players = Player.objects.filter(team_id=team_id).order_by('name')

    team_hist_list = TeamHist.objects.filter(team_id=team_id).order_by('-season_id')

    for team_hist in team_hist_list:
        months = SeasonMonth.objects.filter(season_id=team_hist.season_id)
        team_hist.victory = Game.objects.filter(season_month_id__in=months).filter(visitor_team_id=team_hist.team_id).\
                                filter(visitor_point__gt=F('home_point')).count() + \
                            Game.objects.filter(season_month_id__in=months).filter(home_team_id=team_hist.team_id).\
                                filter(home_point__gt=F('visitor_point')).count()
        team_hist.defeat = Game.objects.filter(season_month_id__in=months).filter(visitor_team_id=team_hist.team_id).\
                               filter(home_point__gt=F('visitor_point')).count() + \
                           Game.objects.filter(season_month_id__in=months).filter(home_team_id=team_hist.team_id).\
                               filter(visitor_point__gt=F('home_point')).count()

    return render(request, 'nba/team.html', {'team': team, 'players': players, 'max_season': max_season,
                                             'team_hist_list': team_hist_list})


def player_list(request):
    name = ""
    filter_team = ""
    order_player = "name_asc"
    teams = Team.objects.all()
    players = Player.objects
    if request.method == 'POST':
        name = request.POST.get('name')
        filter_team = request.POST.get('team')
        if filter_team != "no_filter":
            if filter_team == "no_team":
                players = players.filter(team_id__isnull=True)
            else:
                players = players.filter(team_id=filter_team)
        players = players.filter(name__icontains=name)
        order_player = request.POST.get('order')
    else:
        players = players.all()

    match order_player:
        case "name_asc":
            players = players.order_by('name')
        case "name_desc":
            players = players.order_by('-name')
        case "team_asc":
            players = players.order_by('team')
        case "team_desc":
            players = players.order_by('-team')
        case "age_asc":
            players = players.order_by('-dob')
        case "age_desc":
            players = players.order_by('dob')

    return render(request, 'nba/player_list.html', {'players': players, 'name': name, 'teams': teams,
                                                    'filter_team': filter_team, 'order_player': order_player})


def player(request, player_id: str):
    player = get_object_or_404(Player, id=player_id)
    position = ""
    for i in range(0, len(player.position), 2):
        if i != 0:
            position += ", "
        if (player.position[i] + player.position[i + 1]) == "PG":
            position += "Base"
        elif (player.position[i] + player.position[i + 1]) == "SG":
            position += "Escolta"
        elif (player.position[i] + player.position[i + 1]) == "SF":
            position += "Alero"
        elif (player.position[i] + player.position[i + 1]) == "PF":
            position += "Ala pivot"
        elif (player.position[i] + player.position[i + 1]) == "CE":
            position += "Pivot"
    shoot = ""
    if player.shoot == "R":
        shoot = "Diestro"
    elif player.shoot == "L":
        shoot = "Zurdo"

    max_season = Season.objects.latest('id')
    player_hist_list = PlayerHist.objects.filter(player_id=player_id).order_by('-season_id')

    return render(request, 'nba/player.html', {'player': player, 'max_season': max_season, 'position': position,
                                               'shoot': shoot, 'player_hist_list': player_hist_list})


def game_list(request, season_id: str = None, month: str = None):
    seasons = Season.objects.all()
    months = []
    var_season = None
    var_month = None
    game_list = []
    if len(seasons) > 0:
        if season_id is None:
            var_season = seasons.latest('id')
        else:
            var_season = seasons.filter(id=season_id).latest('id')

        months = SeasonMonth.objects.filter(season_id=var_season.id)

        if len(months) > 0:
            if month is None:
                if season_id is None:
                    var_month = months.latest('id')
                else:
                    var_month = months.earliest('id')
            else:
                month = month_to_english(month)
                var_month = months.filter(month=month).latest('id')

            game_list = Game.objects.filter(season_month_id=var_month.id)
            game_list = sorted(game_list, key=lambda x: (x.game_date, x.game_time), reverse=False)

            var_month.month = month_to_spanish(var_month.month)
            for month in months:
                month.month = month_to_spanish(month.month)

    return render(request, 'nba/game_list.html', {'seasons': seasons, 'months': months, 'var_season': var_season,
                                                  'var_month': var_month, 'game_list': game_list})


def game(request, game_id: str):
    game = Game.objects.filter(id=game_id).latest('id')
    max_quarter = TwoPointerPlay.objects.filter(game_id=game_id).latest('quarter').quarter

    visitor_point = 0
    home_point = 0

    tp_list_1 = ThreePointerPlay.objects.filter(game_id=game_id, quarter=1). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    tp_list_1 = tp_list_1.annotate(type=Value('tp', output_field=CharField()))
    dp_list_1 = TwoPointerPlay.objects.filter(game_id=game_id, quarter=1). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    dp_list_1 = dp_list_1.annotate(type=Value('dp', output_field=CharField()))
    ft_list_1 = FreeThrowPlay.objects.filter(game_id=game_id, quarter=1). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    ft_list_1 = ft_list_1.annotate(type=Value('ft', output_field=CharField()))
    rb_list_1 = ReboundPlay.objects.filter(game_id=game_id, quarter=1). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    rb_list_1 = rb_list_1.annotate(hit=Value(0))
    rb_list_1 = rb_list_1.annotate(type=Value('rb', output_field=CharField()))
    to_list_1 = TurnoverPlay.objects.filter(game_id=game_id, quarter=1). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    to_list_1 = to_list_1.annotate(hit=Value(0))
    to_list_1 = to_list_1.annotate(type=Value('to', output_field=CharField()))
    fl_list_1 = FoulPlay.objects.filter(game_id=game_id, quarter=1). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    fl_list_1 = fl_list_1.annotate(hit=Value(0))
    fl_list_1 = fl_list_1.annotate(type=Value('fl', output_field=CharField()))

    quarter_1 = tp_list_1.union(dp_list_1, ft_list_1, rb_list_1, to_list_1, fl_list_1). \
        order_by('quarter', 'play_time', 'id')

    tp_list_2 = ThreePointerPlay.objects.filter(game_id=game_id, quarter=2). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    tp_list_2 = tp_list_2.annotate(type=Value('tp'))
    dp_list_2 = TwoPointerPlay.objects.filter(game_id=game_id, quarter=2). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    dp_list_2 = dp_list_2.annotate(type=Value('dp'))
    ft_list_2 = FreeThrowPlay.objects.filter(game_id=game_id, quarter=2). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    ft_list_2 = ft_list_2.annotate(type=Value('ft'))
    rb_list_2 = ReboundPlay.objects.filter(game_id=game_id, quarter=2). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    rb_list_2 = rb_list_2.annotate(hit=Value(0))
    rb_list_2 = rb_list_2.annotate(type=Value('rb'))
    to_list_2 = TurnoverPlay.objects.filter(game_id=game_id, quarter=2). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    to_list_2 = to_list_2.annotate(hit=Value(0))
    to_list_2 = to_list_2.annotate(type=Value('to'))
    fl_list_2 = FoulPlay.objects.filter(game_id=game_id, quarter=2). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    fl_list_2 = fl_list_2.annotate(hit=Value(0))
    fl_list_2 = fl_list_2.annotate(type=Value('fl'))

    quarter_2 = tp_list_2.union(dp_list_2, ft_list_2, rb_list_2, to_list_2, fl_list_2). \
        order_by('quarter', 'play_time', 'id')

    tp_list_3 = ThreePointerPlay.objects.filter(game_id=game_id, quarter=3). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    tp_list_3 = tp_list_3.annotate(type=Value('tp'))
    dp_list_3 = TwoPointerPlay.objects.filter(game_id=game_id, quarter=3). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    dp_list_3 = dp_list_3.annotate(type=Value('dp'))
    ft_list_3 = FreeThrowPlay.objects.filter(game_id=game_id, quarter=3). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    ft_list_3 = ft_list_3.annotate(type=Value('ft'))
    rb_list_3 = ReboundPlay.objects.filter(game_id=game_id, quarter=3). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    rb_list_3 = rb_list_3.annotate(hit=Value(0))
    rb_list_3 = rb_list_3.annotate(type=Value('rb'))
    to_list_3 = TurnoverPlay.objects.filter(game_id=game_id, quarter=3). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    to_list_3 = to_list_3.annotate(hit=Value(0))
    to_list_3 = to_list_3.annotate(type=Value('to'))
    fl_list_3 = FoulPlay.objects.filter(game_id=game_id, quarter=3). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    fl_list_3 = fl_list_3.annotate(hit=Value(0))
    fl_list_3 = fl_list_3.annotate(type=Value('fl'))

    quarter_3 = tp_list_3.union(dp_list_3, ft_list_3, rb_list_3, to_list_3, fl_list_3). \
        order_by('quarter', 'play_time', 'id')

    tp_list_4 = ThreePointerPlay.objects.filter(game_id=game_id, quarter=4). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    tp_list_4 = tp_list_4.annotate(type=Value('tp'))
    dp_list_4 = TwoPointerPlay.objects.filter(game_id=game_id, quarter=4). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    dp_list_4 = dp_list_4.annotate(type=Value('dp'))
    ft_list_4 = FreeThrowPlay.objects.filter(game_id=game_id, quarter=4). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    ft_list_4 = ft_list_4.annotate(type=Value('ft'))
    rb_list_4 = ReboundPlay.objects.filter(game_id=game_id, quarter=4). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    rb_list_4 = rb_list_4.annotate(hit=Value(0))
    rb_list_4 = rb_list_4.annotate(type=Value('rb'))
    to_list_4 = TurnoverPlay.objects.filter(game_id=game_id, quarter=4). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    to_list_4 = to_list_4.annotate(hit=Value(0))
    to_list_4 = to_list_4.annotate(type=Value('to'))
    fl_list_4 = FoulPlay.objects.filter(game_id=game_id, quarter=4). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    fl_list_4 = fl_list_4.annotate(hit=Value(0))
    fl_list_4 = fl_list_4.annotate(type=Value('fl'))

    quarter_4 = tp_list_4.union(dp_list_4, ft_list_4, rb_list_4, to_list_4, fl_list_4). \
        order_by('quarter', 'play_time', 'id')

    tp_list_ot = ThreePointerPlay.objects.filter(game_id=game_id, quarter__gt=4). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    tp_list_ot = tp_list_ot.annotate(type=Value('tp'))
    dp_list_ot = TwoPointerPlay.objects.filter(game_id=game_id, quarter__gt=4). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    dp_list_ot = dp_list_ot.annotate(type=Value('dp'))
    ft_list_ot = FreeThrowPlay.objects.filter(game_id=game_id, quarter__gt=4). \
        values('quarter', 'play_time', 'text', 'id', 'team', 'hit')
    ft_list_ot = ft_list_ot.annotate(type=Value('ft'))
    rb_list_ot = ReboundPlay.objects.filter(game_id=game_id, quarter__gt=4). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    rb_list_ot = rb_list_ot.annotate(hit=Value(0))
    rb_list_ot = rb_list_ot.annotate(type=Value('rb'))
    to_list_ot = TurnoverPlay.objects.filter(game_id=game_id, quarter__gt=4). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    to_list_ot = to_list_ot.annotate(hit=Value(0))
    to_list_ot = to_list_ot.annotate(type=Value('to'))
    fl_list_ot = FoulPlay.objects.filter(game_id=game_id, quarter__gt=4). \
        values('quarter', 'play_time', 'text', 'id', 'team')
    fl_list_ot = fl_list_ot.annotate(hit=Value(0))
    fl_list_ot = fl_list_ot.annotate(type=Value('fl'))

    quarter_ot = tp_list_ot.union(dp_list_ot, ft_list_ot, rb_list_ot, to_list_ot, fl_list_ot). \
        order_by('quarter', 'play_time', 'id')

    return render(request, 'nba/game.html', {'game': game, 'quarter_1': quarter_1, 'quarter_2': quarter_2,
                                             'quarter_3': quarter_3, 'quarter_4': quarter_4, 'quarter_ot': quarter_ot,
                                             'visitor_point': visitor_point, 'home_point': home_point,
                                             'max_quarter': max_quarter})


def standings(request, season_id: str = None):
    seasons = Season.objects.all()
    eastern_teams = []
    western_teams = []
    var_season = None
    play_in_e = []
    play_in_w = []
    fr_play_off = []
    sf_play_off = []
    f_play_off = []
    ff_play_off = []
    if len(seasons) > 0:
        if season_id is None:
            var_season = seasons.latest('id')
        else:
            var_season = seasons.filter(id=season_id).latest('id')

        months = SeasonMonth.objects.filter(season_id=var_season.id)

        if len(months) > 0:
            eastern_teams = Team.objects.filter(conference="E")
            eastern_teams = eastern_teams.annotate(season_game=Value(0))
            eastern_teams = eastern_teams.annotate(victory=Value(0))
            eastern_teams = eastern_teams.annotate(defeat=Value(0))
            eastern_teams = eastern_teams.annotate(season_point=Value(0))
            eastern_teams = eastern_teams.annotate(tie_break=Value(0))

            western_teams = Team.objects.filter(conference="W")
            western_teams = western_teams.annotate(season_game=Value(0))
            western_teams = western_teams.annotate(victory=Value(0))
            western_teams = western_teams.annotate(defeat=Value(0))
            western_teams = western_teams.annotate(season_point=Value(0))
            western_teams = western_teams.annotate(tie_break=Value(0))

            for team in eastern_teams:
                season_game_v = Game.objects.filter(season_month_id__in=months).filter(type="SE").\
                                       filter(visitor_team_id=team.id).count()
                season_game_h = Game.objects.filter(season_month_id__in=months).filter(type="SE").\
                                       filter(home_team_id=team.id).count()
                team.season_game = (season_game_v if season_game_v is not None else 0) + \
                                   (season_game_h if season_game_h is not None else 0)
                victory_v = Game.objects.filter(season_month_id__in=months).filter(type="SE").\
                                   filter(visitor_team_id=team.id).filter(visitor_point__gt=F('home_point')).count()
                victory_h = Game.objects.filter(season_month_id__in=months).filter(type="SE").\
                                   filter(home_team_id=team.id).filter(home_point__gt=F('visitor_point')).count()
                team.victory = (victory_v if victory_v is not None else 0) + \
                               (victory_h if victory_h is not None else 0)
                defeat_v = Game.objects.filter(season_month_id__in=months).filter(type="SE").\
                                  filter(visitor_team_id=team.id).filter(home_point__gt=F('visitor_point')).count()
                defeat_h = Game.objects.filter(season_month_id__in=months).filter(type="SE").\
                                  filter(home_team_id=team.id).filter(visitor_point__gt=F('home_point')).count()
                team.defeat = (defeat_v if defeat_v is not None else 0) + \
                              (defeat_h if defeat_h is not None else 0)
                season_point_v = Game.objects.filter(season_month_id__in=months).filter(type="SE").\
                                        filter(visitor_team_id=team.id).aggregate(sp_v=Sum('visitor_point'))['sp_v']
                season_point_h = Game.objects.filter(season_month_id__in=months).filter(type="SE").\
                                        filter(home_team_id=team.id).aggregate(sp_h=Sum('home_point'))['sp_h']
                team.season_point = (season_point_v if season_point_v is not None else 0) + \
                                    (season_point_h if season_point_h is not None else 0)

            eastern_teams_sorted = sorted(eastern_teams, key=lambda x: (x.victory, x.tie_break), reverse=True)
            before_teams = []
            for team in eastern_teams_sorted:
                if len(before_teams) == 0:
                    before_teams.append(team)
                else:
                    if team.victory == before_teams[0].victory:
                        before_teams.append(team)
                    else:
                        tie_break(before_teams, months)
                        before_teams = [team]
            if len(before_teams) > 1:
                tie_break(before_teams, months)
            eastern_teams = sorted(eastern_teams, key=lambda x: (x.victory, x.tie_break), reverse=True)

            for team in western_teams:
                season_game_v = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                        filter(visitor_team_id=team.id).count()
                season_game_h = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                        filter(home_team_id=team.id).count()
                team.season_game = (season_game_v if season_game_v is not None else 0) + \
                                   (season_game_h if season_game_h is not None else 0)
                victory_v = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                    filter(visitor_team_id=team.id).filter(visitor_point__gt=F('home_point')).count()
                victory_h = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                    filter(home_team_id=team.id).filter(home_point__gt=F('visitor_point')).count()
                team.victory = (victory_v if victory_v is not None else 0) + \
                               (victory_h if victory_h is not None else 0)
                defeat_v = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                    filter(visitor_team_id=team.id).filter(home_point__gt=F('visitor_point')).count()
                defeat_h = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                    filter(home_team_id=team.id).filter(visitor_point__gt=F('home_point')).count()
                team.defeat = (defeat_v if defeat_v is not None else 0) + \
                              (defeat_h if defeat_h is not None else 0)
                season_point_v = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                        filter(visitor_team_id=team.id).aggregate(sp_v=Sum('visitor_point'))['sp_v']
                season_point_h = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                        filter(home_team_id=team.id).aggregate(sp_h=Sum('home_point'))['sp_h']
                team.season_point = (season_point_v if season_point_v is not None else 0) + \
                                    (season_point_h if season_point_h is not None else 0)

            western_teams_sorted = sorted(western_teams, key=lambda x: (x.victory, x.tie_break), reverse=True)
            before_teams = []
            for team in western_teams_sorted:
                if len(before_teams) == 0:
                    before_teams.append(team)
                else:
                    if team.victory == before_teams[0].victory:
                        before_teams.append(team)
                    else:
                        tie_break(before_teams, months)
                        before_teams = [team]
            if len(before_teams) > 1:
                tie_break(before_teams, months)
            western_teams = sorted(western_teams, key=lambda x: (x.victory, x.tie_break), reverse=True)

            # Play-In Eastern
            seven_e = None
            eight_e = None
            nine_e = None
            seven_e_victory = num_victory(months, eastern_teams[6], eastern_teams[7], "PI")
            eight_e_victory = num_victory(months, eastern_teams[7], eastern_teams[6], "PI")
            if seven_e_victory > 0 or eight_e_victory > 0:
                play_in_e.append([eastern_teams[6], eastern_teams[7], seven_e_victory, eight_e_victory, "Puesto 7"])
                if seven_e_victory > eight_e_victory:
                    seven_e = eastern_teams[6]
                    eight_e = eastern_teams[7]
                else:
                    seven_e = eastern_teams[7]
                    eight_e = eastern_teams[6]

            nine_e_victory = num_victory(months, eastern_teams[8], eastern_teams[9], "PI")
            ten_e_victory = num_victory(months, eastern_teams[9], eastern_teams[8], "PI")
            if nine_e_victory > 0 or ten_e_victory > 0:
                play_in_e.append([eastern_teams[8], eastern_teams[9], nine_e_victory, ten_e_victory, "Opción puesto 8"])
                if nine_e_victory > ten_e_victory:
                    nine_e = eastern_teams[8]
                else:
                    nine_e = eastern_teams[9]

            if eight_e is not None and nine_e is not None:
                eight_e_victory = num_victory(months, eight_e, nine_e, "PI")
                nine_e_victory = num_victory(months, nine_e, eight_e, "PI")
                if eight_e_victory > 0 or nine_e_victory > 0:
                    play_in_e.append([eight_e, nine_e, eight_e_victory, nine_e_victory, "Puesto 8"])
                    if eight_e_victory < nine_e_victory:
                        eight_e = nine_e

            if var_season.id >= 2020 and len(play_in_e) == 0:
                play_in_games_e = Game.objects.filter(season_month_id__in=months).filter(type="PI"). \
                    filter(visitor_team_id__in=eastern_teams)
                for game in play_in_games_e:
                    play_in_e.append([game.visitor_team, game.home_team,
                                     1 if game.visitor_point > game.home_point else 0,
                                     1 if game.home_point > game.visitor_point else 0, " - "])

                eight_game_e = Game.objects.filter(season_month_id__in=months).filter(type="POER"). \
                    filter(visitor_team_id=eastern_teams[0])
                eight_e = eight_game_e[0].home_team if len(eight_game_e) > 0 else eastern_teams[7]
                seven_game_e = Game.objects.filter(season_month_id__in=months).filter(type="POER"). \
                    filter(visitor_team_id=eastern_teams[1])
                seven_e = seven_game_e[0].home_team if len(seven_game_e) > 0 else eastern_teams[6]

            # Play-In Western
            seven_w = None
            eight_w = None
            nine_w = None
            seven_w_victory = num_victory(months, western_teams[6], western_teams[7], "PI")
            eight_w_victory = num_victory(months, western_teams[7], western_teams[6], "PI")
            if seven_w_victory > 0 or eight_w_victory > 0:
                play_in_w.append([western_teams[6], western_teams[7], seven_w_victory, eight_w_victory, "Puesto 7"])
                if seven_w_victory > eight_w_victory:
                    seven_w = western_teams[6]
                    eight_w = western_teams[7]
                else:
                    seven_w = western_teams[7]
                    eight_w = western_teams[6]

            nine_w_victory = num_victory(months, western_teams[8], western_teams[9], "PI")
            ten_w_victory = num_victory(months, western_teams[9], western_teams[8], "PI")
            if nine_w_victory > 0 or ten_w_victory > 0:
                play_in_w.append([western_teams[8], western_teams[9], nine_w_victory, ten_w_victory, "Opción puesto 8"])
                if nine_w_victory > ten_w_victory:
                    nine_w = western_teams[8]
                else:
                    nine_w = western_teams[9]

            if eight_w is not None and nine_w is not None:
                eight_w_victory = num_victory(months, eight_w, nine_w, "PI")
                nine_w_victory = num_victory(months, nine_w, eight_w, "PI")
                if eight_w_victory > 0 or nine_w_victory > 0:
                    play_in_w.append([eight_w, nine_w, eight_w_victory, nine_w_victory, "Puesto 8"])
                    if eight_w_victory < nine_w_victory:
                        eight_w = nine_w

            if var_season.id >= 2020 and len(play_in_w) == 0:
                play_in_games_w = Game.objects.filter(season_month_id__in=months).filter(type="PI"). \
                    filter(visitor_team_id__in=western_teams)
                for game in play_in_games_w:
                    play_in_w.append([game.visitor_team, game.home_team,
                                     1 if game.visitor_point > game.home_point else 0,
                                     1 if game.home_point > game.visitor_point else 0, " - "])

                eight_game_w = Game.objects.filter(season_month_id__in=months).filter(type="POWR"). \
                    filter(visitor_team_id=western_teams[0])
                eight_w = eight_game_w[0].home_team if len(eight_game_w) > 0 else western_teams[7]
                seven_game_w = Game.objects.filter(season_month_id__in=months).filter(type="POWR"). \
                    filter(visitor_team_id=western_teams[1])
                seven_w = seven_game_w[0].home_team if len(seven_game_w) > 0 else western_teams[6]

            # First Round Play-Off Eastern
            one_e = None
            two_e = None
            three_e = None
            four_e = None
            extra_teams_e = []
            games_poer = Game.objects.filter(season_month_id__in=months).filter(type="POER")
            if len(games_poer) > 0:
                if seven_e is None:
                    seven_e = eastern_teams[6]
                if eight_e is None:
                    eight_e = eastern_teams[7]
                poer_teams = [eastern_teams[0], eastern_teams[1], eastern_teams[2], eastern_teams[3],
                              eastern_teams[4], eastern_teams[5], seven_e, eight_e]

                one_e_victory = num_victory(months, eastern_teams[0], eight_e, "POER")
                eight_e_victory = num_victory(months, eight_e, eastern_teams[0], "POER")
                if one_e_victory > 0 or eight_e_victory > 0:
                    fr_play_off.append([eastern_teams[0], eight_e, one_e_victory, eight_e_victory, "Oriental"])
                    poer_teams.remove(eastern_teams[0])
                    poer_teams.remove(eight_e)
                    if one_e_victory > eight_e_victory:
                        one_e = eastern_teams[0]
                    else:
                        one_e = eight_e

                four_e_victory = num_victory(months, eastern_teams[3], eastern_teams[4], "POER")
                five_e_victory = num_victory(months, eastern_teams[4], eastern_teams[3], "POER")
                if four_e_victory > 0 or five_e_victory > 0:
                    fr_play_off.append([eastern_teams[3], eastern_teams[4], four_e_victory, five_e_victory, "Oriental"])
                    poer_teams.remove(eastern_teams[3])
                    poer_teams.remove(eastern_teams[4])
                    if four_e_victory > five_e_victory:
                        four_e = eastern_teams[3]
                    else:
                        four_e = eastern_teams[4]

                three_e_victory = num_victory(months, eastern_teams[2], eastern_teams[5], "POER")
                six_e_victory = num_victory(months, eastern_teams[5], eastern_teams[2], "POER")
                if three_e_victory > 0 or six_e_victory > 0:
                    fr_play_off.append([eastern_teams[2], eastern_teams[5], three_e_victory, six_e_victory, "Oriental"])
                    poer_teams.remove(eastern_teams[2])
                    poer_teams.remove(eastern_teams[5])
                    if three_e_victory > six_e_victory:
                        three_e = eastern_teams[2]
                    else:
                        three_e = eastern_teams[5]

                two_e_victory = num_victory(months, eastern_teams[1], seven_e, "POER")
                seven_e_victory = num_victory(months, seven_e, eastern_teams[1], "POER")
                if two_e_victory > 0 or seven_e_victory > 0:
                    fr_play_off.append([eastern_teams[1], seven_e, two_e_victory, seven_e_victory, "Oriental"])
                    poer_teams.remove(eastern_teams[1])
                    poer_teams.remove(seven_e)
                    if two_e_victory > seven_e_victory:
                        two_e = eastern_teams[1]
                    else:
                        two_e = seven_e

                if len(poer_teams) > 0:
                    for team in poer_teams:
                        if team not in extra_teams_e:
                            games = games_poer.filter(visitor_team_id=team.id)
                            if len(games) > 0:
                                visitor_team_victory = num_victory(months, games[0].visitor_team, games[0].home_team, "POER")
                                home_team_victory = num_victory(months, games[0].home_team, games[0].visitor_team, "POER")
                                fr_play_off.append([games[0].visitor_team, games[0].home_team, visitor_team_victory,
                                                    home_team_victory, "Oriental"])
                                extra_teams_e.append(games[0].visitor_team)
                                extra_teams_e.append(games[0].home_team)

            # First Round Play-Off Western
            one_w = None
            two_w = None
            three_w = None
            four_w = None
            extra_teams_w = []
            games_powr = Game.objects.filter(season_month_id__in=months).filter(type="POWR")
            if len(games_powr) > 0:
                if seven_w is None:
                    seven_w = western_teams[6]
                if eight_w is None:
                    eight_w = western_teams[7]
                powr_teams = [western_teams[0], western_teams[1], western_teams[2], western_teams[3],
                              western_teams[4], western_teams[5], seven_w, eight_w]

                one_w_victory = num_victory(months, western_teams[0], eight_w, "POWR")
                eight_w_victory = num_victory(months, eight_w, western_teams[0], "POWR")
                if one_w_victory > 0 or eight_w_victory > 0:
                    fr_play_off.append([western_teams[0], eight_w, one_w_victory, eight_w_victory, "Occidental"])
                    powr_teams.remove(western_teams[0])
                    powr_teams.remove(eight_w)
                    if one_w_victory > eight_w_victory:
                        one_w = western_teams[0]
                    else:
                        one_w = eight_w

                four_w_victory = num_victory(months, western_teams[3], western_teams[4], "POWR")
                five_w_victory = num_victory(months, western_teams[4], western_teams[3], "POWR")
                if four_w_victory > 0 or five_w_victory > 0:
                    fr_play_off.append([western_teams[3], western_teams[4], four_w_victory, five_w_victory, "Occidental"])
                    powr_teams.remove(western_teams[3])
                    powr_teams.remove(western_teams[4])
                    if four_w_victory > five_w_victory:
                        four_w = western_teams[3]
                    else:
                        four_w = western_teams[4]

                three_w_victory = num_victory(months, western_teams[2], western_teams[5], "POWR")
                six_w_victory = num_victory(months, western_teams[5], western_teams[2], "POWR")
                if three_w_victory > 0 or six_w_victory > 0:
                    fr_play_off.append([western_teams[2], western_teams[5], three_w_victory, six_w_victory, "Occidental"])
                    powr_teams.remove(western_teams[2])
                    powr_teams.remove(western_teams[5])
                    if three_w_victory > six_w_victory:
                        three_w = western_teams[2]
                    else:
                        three_w = western_teams[5]

                two_w_victory = num_victory(months, western_teams[1], seven_w, "POWR")
                seven_w_victory = num_victory(months, seven_w, western_teams[1], "POWR")
                if two_w_victory > 0 or seven_w_victory > 0:
                    fr_play_off.append([western_teams[1], seven_w, two_w_victory, seven_w_victory, "Occidental"])
                    powr_teams.remove(western_teams[1])
                    powr_teams.remove(seven_w)
                    if two_w_victory > seven_w_victory:
                        two_w = western_teams[1]
                    else:
                        two_w = seven_w

                if len(powr_teams) > 0:
                    for team in powr_teams:
                        if team not in extra_teams_w:
                            games = games_powr.filter(visitor_team_id=team.id)
                            if len(games) > 0:
                                visitor_team_victory = num_victory(months, games[0].visitor_team, games[0].home_team, "POWR")
                                home_team_victory = num_victory(months, games[0].home_team, games[0].visitor_team, "POWR")
                                fr_play_off.append([games[0].visitor_team, games[0].home_team, visitor_team_victory,
                                                    home_team_victory, "Occidental"])
                                extra_teams_w.append(games[0].visitor_team)
                                extra_teams_w.append(games[0].home_team)

            # Semifinal Play-Off Eastern
            games_poes = Game.objects.filter(season_month_id__in=months).filter(type="POES")
            if len(games_poes) > 0:
                poes_teams = [one_e, two_e, three_e, four_e]
                poes_teams = [i for i in poes_teams if i]
                poes_teams.extend(extra_teams_e)

                if one_e is not None and four_e is not None:
                    one_e_victory = num_victory(months, one_e, four_e, "POES")
                    four_e_victory = num_victory(months, four_e, one_e, "POES")
                    if one_e_victory > 0 or four_e_victory > 0:
                        sf_play_off.append([one_e, four_e, one_e_victory, four_e_victory, "Oriental"])
                        poes_teams.remove(one_e)
                        poes_teams.remove(four_e)
                        if one_e_victory > four_e_victory:
                            one_e = one_e
                        else:
                            one_e = four_e

                if two_e is not None and three_e is not None:
                    three_e_victory = num_victory(months, three_e, two_e, "POES")
                    two_e_victory = num_victory(months, two_e, three_e, "POES")
                    if three_e_victory > 0 or two_e_victory > 0:
                        sf_play_off.append([three_e, two_e, three_e_victory, two_e_victory, "Oriental"])
                        poes_teams.remove(two_e)
                        poes_teams.remove(three_e)
                        if three_e_victory > two_e_victory:
                            two_e = three_e
                        else:
                            two_e = two_e

                extra_teams_e = []
                if len(poes_teams) > 0:
                    for team in poes_teams:
                        if team not in extra_teams_e:
                            games = games_poes.filter(visitor_team_id=team.id)
                            if len(games) > 0:
                                visitor_team_victory = num_victory(months, games[0].visitor_team, games[0].home_team,
                                                                   "POES")
                                home_team_victory = num_victory(months, games[0].home_team, games[0].visitor_team,
                                                                "POES")
                                sf_play_off.append([games[0].visitor_team, games[0].home_team, visitor_team_victory,
                                                    home_team_victory, "Oriental"])
                                extra_teams_e.append(games[0].visitor_team)
                                extra_teams_e.append(games[0].home_team)

            # Semifinal Play-Off Western
            games_pows = Game.objects.filter(season_month_id__in=months).filter(type="POWS")
            if len(games_pows) > 0:
                pows_teams = [one_w, two_w, three_w, four_w]
                pows_teams = [i for i in pows_teams if i]
                pows_teams.extend(extra_teams_w)

                if one_w is not None and four_w is not None:
                    one_w_victory = num_victory(months, one_w, four_w, "POWS")
                    four_w_victory = num_victory(months, four_w, one_w, "POWS")
                    if one_w_victory > 0 or four_w_victory > 0:
                        sf_play_off.append([one_w, four_w, one_w_victory, four_w_victory, "Occidental"])
                        poes_teams.remove(one_w)
                        poes_teams.remove(four_w)
                        if one_w_victory > four_w_victory:
                            one_w = one_w
                        else:
                            one_w = four_w

                if two_w is not None and three_w is not None:
                    three_w_victory = num_victory(months, three_w, two_w, "POWS")
                    two_w_victory = num_victory(months, two_w, three_w, "POWS")
                    if three_w_victory > 0 or two_w_victory > 0:
                        sf_play_off.append([three_w, two_w, three_w_victory, two_w_victory, "Occidental"])
                        poes_teams.remove(two_w)
                        poes_teams.remove(three_w)
                        if three_w_victory > two_w_victory:
                            two_w = three_w
                        else:
                            two_w = two_w

                extra_teams_w = []
                if len(pows_teams) > 0:
                    for team in pows_teams:
                        if team not in extra_teams_w:
                            games = games_pows.filter(visitor_team_id=team.id)
                            if len(games) > 0:
                                visitor_team_victory = num_victory(months, games[0].visitor_team, games[0].home_team,
                                                                   "POWS")
                                home_team_victory = num_victory(months, games[0].home_team, games[0].visitor_team,
                                                                "POWS")
                                sf_play_off.append([games[0].visitor_team, games[0].home_team, visitor_team_victory,
                                                    home_team_victory, "Occidental"])
                                extra_teams_w.append(games[0].visitor_team)
                                extra_teams_w.append(games[0].home_team)

            # Final Play-Off Eastern
            games_poef = Game.objects.filter(season_month_id__in=months).filter(type="POEF")
            if len(games_poef) > 0:
                poef_teams = [one_w, two_w]
                poef_teams = [i for i in poef_teams if i]
                poef_teams.extend(extra_teams_e)
                extra_teams_e = []

                if one_e is not None and two_e is not None:
                    one_e_victory = num_victory(months, one_e, two_e, "POEF")
                    two_e_victory = num_victory(months, two_e, one_e, "POEF")
                    if one_e_victory > 0 or two_e_victory > 0:
                        f_play_off.append([one_e, two_e, one_e_victory, two_e_victory, "Oriental"])
                        if one_e_victory > two_e_victory:
                            one_e = one_e
                        else:
                            one_e = two_e
                elif len(poef_teams) > 0:
                    games = games_poef.filter(visitor_team_id=poef_teams[0].id)
                    if len(games) > 0:
                        visitor_team_victory = num_victory(months, games[0].visitor_team, games[0].home_team,
                                                           "POEF")
                        home_team_victory = num_victory(months, games[0].home_team, games[0].visitor_team,
                                                        "POEF")
                        f_play_off.append([games[0].visitor_team, games[0].home_team, visitor_team_victory,
                                           home_team_victory, "Oriental"])
                        extra_teams_e.append(games[0].visitor_team)
                        extra_teams_e.append(games[0].home_team)

            # Final Play-Off Western
            games_powf = Game.objects.filter(season_month_id__in=months).filter(type="POWF")
            if len(games_powf) > 0:
                powf_teams = [one_w, two_w]
                powf_teams = [i for i in powf_teams if i]
                powf_teams.extend(extra_teams_w)
                extra_teams_w = []

                if one_w is not None and two_w is not None:
                    one_w_victory = num_victory(months, one_w, two_w, "POWF")
                    two_w_victory = num_victory(months, two_w, one_w, "POWF")
                    if one_w_victory > 0 or two_w_victory > 0:
                        f_play_off.append([one_w, two_w, one_w_victory, two_w_victory, "Occidental"])
                        if one_w_victory > two_w_victory:
                            one_w = one_w
                        else:
                            one_w = two_w
                elif len(powf_teams) > 0:
                    games = games_powf.filter(visitor_team_id=poef_teams[0].id)
                    if len(games) > 0:
                        visitor_team_victory = num_victory(months, games[0].visitor_team, games[0].home_team,
                                                           "POWF")
                        home_team_victory = num_victory(months, games[0].home_team, games[0].visitor_team,
                                                        "POWF")
                        f_play_off.append([games[0].visitor_team, games[0].home_team, visitor_team_victory,
                                           home_team_victory, "Occidental"])
                        extra_teams_w.append(games[0].visitor_team)
                        extra_teams_w.append(games[0].home_team)

            # Final Play-Off
            games_pof = Game.objects.filter(season_month_id__in=months).filter(type="POF")
            if len(games_pof) > 0:
                pof_teams = [one_e, one_w]
                pof_teams = [i for i in pof_teams if i]
                pof_teams.extend(extra_teams_e)
                pof_teams.extend(extra_teams_w)

                if one_e is not None and one_w is not None:
                    one_e_victory = num_victory(months, one_e, one_w, "POF")
                    one_w_victory = num_victory(months, one_w, one_e, "POF")
                    if one_e_victory > 0 or one_w_victory > 0:
                        ff_play_off.append([one_e, one_w, one_e_victory, one_w_victory])
                elif len(powf_teams) > 0:
                    games = games_pof.filter(visitor_team_id=poef_teams[0].id)
                    if len(games) > 0:
                        visitor_team_victory = num_victory(months, games[0].visitor_team, games[0].home_team,
                                                           "POF")
                        home_team_victory = num_victory(months, games[0].home_team, games[0].visitor_team,
                                                        "POF")
                        ff_play_off.append([games[0].visitor_team, games[0].home_team, visitor_team_victory,
                                           home_team_victory])

    return render(request, 'nba/standings.html', {'eastern_teams': eastern_teams, 'western_teams': western_teams,
                                                  'seasons': seasons, 'var_season': var_season,
                                                  'play_in_e': play_in_e, 'play_in_w': play_in_w,
                                                  'fr_play_off': fr_play_off, 'sf_play_off': sf_play_off,
                                                  'f_play_off': f_play_off, 'ff_play_off': ff_play_off})


def month_to_spanish(month: str) -> str:
    split_month = month.split("-")
    month_1 = split_month[0]
    match month_1:
        case "january":
            month_1 = "enero"
        case "february":
            month_1 = "febrero"
        case "march":
            month_1 = "marzo"
        case "april":
            month_1 = "abril"
        case "may":
            month_1 = "mayo"
        case "june":
            month_1 = "junio"
        case "july":
            month_1 = "julio"
        case "august":
            month_1 = "agosto"
        case "september":
            month_1 = "septiembree"
        case "october":
            month_1 = "octubre"
        case "november":
            month_1 = "noviembre"
        case "december":
            month_1 = "diciembre"
        case _:
            month_1 = month
    if len(split_month) > 1:
        return month_1 + "-" + split_month[1]
    else:
        return month_1


def month_to_english(month: str) -> str:
    split_month = month.split("-")
    month_1 = split_month[0]
    match month_1:
        case "enero":
            month_1 = "january"
        case "febrero":
            month_1 = "february"
        case "marzo":
            month_1 = "march"
        case "abril":
            month_1 = "april"
        case "mayo":
            month_1 = "may"
        case "junio":
            month_1 = "june"
        case "julio":
            month_1 = "july"
        case "agosto":
            month_1 = "august"
        case "septiembre":
            month_1 = "september"
        case "octubre":
            month_1 = "october"
        case "noviembre":
            month_1 = "november"
        case "diciembre":
            month_1 = "december"
        case _:
            month_1 = month
    if len(split_month) > 1:
        return month_1 + "-" + split_month[1]
    else:
        return month_1


def tie_break(before_teams, months):
    """Tie breaker for the season standings"""
    # Tie breaker for two teams
    if len(before_teams) == 2:
        # Better balance of results in the matches between the two teams
        before_teams[0].tie_break = Game.objects.filter(season_month_id__in=months).filter(type="SE").\
                          filter(visitor_team_id=before_teams[0].id).filter(home_team_id=before_teams[1].id).\
                          filter(visitor_point__gt=F('home_point')).count() + \
                      Game.objects.filter(season_month_id__in=months).filter(type="SE").\
                          filter(home_team_id=before_teams[0].id).filter(visitor_team_id=before_teams[1].id).\
                          filter(home_point__gt=F('visitor_point')).count()

        before_teams[1].tie_break = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                          filter(visitor_team_id=before_teams[1].id).filter(home_team_id=before_teams[0].id). \
                          filter(visitor_point__gt=F('home_point')).count() + \
                      Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                          filter(home_team_id=before_teams[1].id).filter(visitor_team_id=before_teams[0].id). \
                          filter(home_point__gt=F('visitor_point')).count()

        # Who has won their division
        if before_teams[0].tie_break == before_teams[1].tie_break:
            teams_div_0 = Team.objects.filter(division=before_teams[0].division)
            teams_div_1 = Team.objects.filter(division=before_teams[1].division)

            for team in teams_div_0:
                team.victory = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                   filter(visitor_team_id=team.id).filter(visitor_point__gt=F('home_point')).count() + \
                               Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                   filter(home_team_id=team.id).filter(home_point__gt=F('visitor_point')).count()
            teams_div_0 = sorted(teams_div_0, key=lambda x: (x.victory), reverse=True)
            if teams_div_0[0].id == before_teams[0].id and teams_div_0[1].id != before_teams[1].id:
                before_teams[0].tie_break += 1

            for team in teams_div_1:
                team.victory = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                   filter(visitor_team_id=team.id).filter(visitor_point__gt=F('home_point')).count() + \
                               Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                   filter(home_team_id=team.id).filter(home_point__gt=F('visitor_point')).count()
            teams_div_1 = sorted(teams_div_1, key=lambda x: (x.victory), reverse=True)
            if teams_div_1[0].id == before_teams[1].id and teams_div_1[1].id != before_teams[0].id:
                before_teams[1].tie_break += 1

            # Best win % against rivals in the same division
            if before_teams[0].tie_break == before_teams[1].tie_break:
                if before_teams[0].division == before_teams[1].division:
                    teams_div = Team.objects.filter(division=before_teams[0].division)

                    team_victory_0 = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                         filter(visitor_team_id=before_teams[0].id).filter(home_team_id__in=teams_div).\
                                         filter(visitor_point__gt=F('home_point')).count() + \
                                     Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                         filter(home_team_id=before_teams[0].id).filter(visitor_team_id__in=teams_div).\
                                         filter(home_point__gt=F('visitor_point')).count()

                    team_victory_1 = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                         filter(visitor_team_id=before_teams[1].id).filter(home_team_id__in=teams_div).\
                                         filter(visitor_point__gt=F('home_point')).count() + \
                                     Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                         filter(home_team_id=before_teams[1].id).filter(visitor_team_id__in=teams_div).\
                                         filter(home_point__gt=F('visitor_point')).count()

                    if team_victory_0 > team_victory_1:
                        before_teams[0].tie_break += 1
                    elif team_victory_0 < team_victory_1:
                        before_teams[1].tie_break += 1

                # Best win % in the same conference
                if before_teams[0].tie_break == before_teams[1].tie_break:
                    teams_conf = Team.objects.filter(conference=before_teams[0].conference)

                    team_victory_0 = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                         filter(visitor_team_id=before_teams[0].id).filter(home_team_id__in=teams_conf). \
                                         filter(visitor_point__gt=F('home_point')).count() + \
                                     Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                         filter(home_team_id=before_teams[0].id).filter(visitor_team_id__in=teams_conf). \
                                         filter(home_point__gt=F('visitor_point')).count()

                    team_victory_1 = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                         filter(visitor_team_id=before_teams[1].id).filter(home_team_id__in=teams_conf). \
                                         filter(visitor_point__gt=F('home_point')).count() + \
                                     Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                         filter(home_team_id=before_teams[1].id).filter(visitor_team_id__in=teams_conf). \
                                         filter(home_point__gt=F('visitor_point')).count()

                    if team_victory_0 > team_victory_1:
                        before_teams[0].tie_break += 1
                    elif team_victory_0 < team_victory_1:
                        before_teams[1].tie_break += 1

    # Tie breaker for more than two teams
    elif len(before_teams) > 2:
        # Who has won their division
        for b_team in before_teams:
            teams_div = Team.objects.filter(division=b_team.division)

            for team in teams_div:
                team.victory = Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                   filter(visitor_team_id=team.id).filter(visitor_point__gt=F('home_point')).count() + \
                               Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                   filter(home_team_id=team.id).filter(home_point__gt=F('visitor_point')).count()
            teams_div = sorted(teams_div, key=lambda x: (x.victory), reverse=True)
            if teams_div[0].id == b_team.id or \
                    (teams_div[1].id != b_team.id and teams_div[0].victory == teams_div[1].victory):
                b_team.tie_break += 1000
            else:
                b_team.tie_break -= 1000

        # Better balance of results in the matches between their
        for b_team in before_teams:
            b_team.tie_break += (Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                            filter(visitor_team_id=b_team.id).filter(home_team_id__in=before_teams). \
                                            filter(visitor_point__gt=F('home_point')).count() + \
                                Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                            filter(home_team_id=b_team.id).filter(visitor_team_id__in=before_teams). \
                                            filter(home_point__gt=F('visitor_point')).count())*100

        # Best win % against rivals in the same division
        div = None
        for b_team in before_teams:
            if div is None:
                div = b_team.division
            elif div != b_team.division:
                div = None
                break
        if div is not None:
            teams_div = Team.objects.filter(division=before_teams[0].division)
            for b_team in before_teams:
                b_team.tie_break += (Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                        filter(visitor_team_id=b_team.id).filter(home_team_id__in=teams_div). \
                                        filter(visitor_point__gt=F('home_point')).count() + \
                                    Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                        filter(home_team_id=b_team.id).filter(visitor_team_id__in=teams_div). \
                                        filter(home_point__gt=F('visitor_point')).count())*10

        # Best win % in the same conference
        for b_team in before_teams:
            teams_conf = Team.objects.filter(conference=before_teams[0].conference)
            b_team.tie_break += Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                 filter(visitor_team_id=b_team.id).filter(home_team_id__in=teams_conf). \
                                 filter(visitor_point__gt=F('home_point')).count() + \
                             Game.objects.filter(season_month_id__in=months).filter(type="SE"). \
                                 filter(home_team_id=b_team.id).filter(visitor_team_id__in=teams_conf). \
                                 filter(home_point__gt=F('visitor_point')).count()


def num_victory(months, v_team, h_team, type):
    return Game.objects.filter(season_month_id__in=months).filter(type=type).\
                filter(visitor_team_id=v_team.id).filter(home_team_id=h_team.id).\
                filter(visitor_point__gt=F('home_point')).count() + \
            Game.objects.filter(season_month_id__in=months).filter(type=type).\
                filter(home_team_id=v_team.id).filter(visitor_team_id=h_team.id).\
                filter(home_point__gt=F('visitor_point')).count()
