import datetime
from enum import Enum

from django.utils import timezone
from django.db import models


# Create your models here.

class Season(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=7)

    class Meta:
        db_table = "season"

    def __str__(self):
        return self.name


class SeasonMonth(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    month = models.CharField(max_length=14)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    class Meta:
        db_table = "season_month"

    def __str__(self):
        return self.month


class Team(models.Model):
    """
    class Conference(models.TextChoices):
        EASTERN = 'E'
        WESTERN = 'W'
    """
    class Conference(models.TextChoices):
        ORIENTAL = 'E'
        OCCIDENTAL = 'W'
    """
    class Division(models.TextChoices):
        ATLANTIC = 'AT'
        CENTRAL = 'CE'
        SOUTHEAST = 'SE'
        NORTHWEST = 'NW'
        PACIFIC = 'PA'
        SOUTHWEST = 'SW'
    """

    class Division(models.TextChoices):
        ATLÁNTICO = 'AT'
        CENTRAL = 'CE'
        SURESTE = 'SE'
        NOROESTE = 'NW'
        PACÍFICO = 'PA'
        SUROESTE = 'SW'

    id = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='teams', null=True, blank=False, default=None)
    conference = models.CharField(max_length=1, choices=Conference.choices, null=True)
    division = models.CharField(max_length=2, choices=Division.choices, null=True)
    old_id = models.TextField(blank=True)
    coach = models.CharField(max_length=50, blank=True, null=True)
    arena = models.CharField(max_length=50, blank=True, null=True)
    game = models.PositiveSmallIntegerField(default=0)
    point = models.PositiveIntegerField(default=0)
    tp = models.PositiveIntegerField(default=0)
    tpa = models.PositiveIntegerField(default=0)
    dp = models.PositiveIntegerField(default=0)
    dpa = models.PositiveIntegerField(default=0)
    ft = models.PositiveIntegerField(default=0)
    fta = models.PositiveIntegerField(default=0)
    orb = models.PositiveIntegerField(default=0)
    drb = models.PositiveIntegerField(default=0)
    ast = models.PositiveIntegerField(default=0)
    stl = models.PositiveIntegerField(default=0)
    blk = models.PositiveIntegerField(default=0)
    tov = models.PositiveIntegerField(default=0)
    foul = models.PositiveIntegerField(default=0)
    drw = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "team"

    def __str__(self):
        return self.name


class TeamHist(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    season = models.ForeignKey(Season, on_delete=models.DO_NOTHING)
    game = models.PositiveSmallIntegerField(default=0)
    point = models.PositiveIntegerField(default=0)
    tp = models.PositiveIntegerField(default=0)
    tpa = models.PositiveIntegerField(default=0)
    dp = models.PositiveIntegerField(default=0)
    dpa = models.PositiveIntegerField(default=0)
    ft = models.PositiveIntegerField(default=0)
    fta = models.PositiveIntegerField(default=0)
    orb = models.PositiveIntegerField(default=0)
    drb = models.PositiveIntegerField(default=0)
    ast = models.PositiveIntegerField(default=0)
    stl = models.PositiveIntegerField(default=0)
    blk = models.PositiveIntegerField(default=0)
    tov = models.PositiveIntegerField(default=0)
    foul = models.PositiveIntegerField(default=0)
    drw = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "team_hist"
        verbose_name_plural = "Team history"
        constraints = [
            models.UniqueConstraint(
                fields=['team', 'season'], name='unique_team_season_combination'
            )
        ]

    def __str__(self):
        return self.team + " - " + self.season

"""
class Position(Enum):
    POINT_GUARD = 'PG'
    SHOOTING_GUARD = 'SG'
    SMALL_FORWARD = 'SF'
    POWER_FORWARD = 'PF'
    CENTER = 'CE'
"""
class Position(Enum):
    BASE = 'PG'
    ESCOLTA = 'SG'
    ALERO = 'SF'
    ALA_PIVOT = 'PF'
    PIVOT = 'CE'

class Player(models.Model):
    """
    class Shoot(models.TextChoices):
        RIGHT = 'R'
        LEFT = 'L'
    """
    class Shoot(models.TextChoices):
        ZURDO = 'R'
        DIESTRO = 'L'

    id = models.CharField(primary_key=True, max_length=9)
    name = models.CharField(max_length=50)
    number = models.PositiveSmallIntegerField(null=True)
    photo = models.ImageField(upload_to='players', null=True, blank=False)
    dob = models.DateField(null=True)
    position = models.CharField(max_length=10, null=True)
    shoot = models.CharField(max_length=1, choices=Shoot.choices, null=True)
    height = models.PositiveSmallIntegerField(default=0, null=True)
    weight = models.PositiveSmallIntegerField(default=0, null=True)
    team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING, related_name='players_team',
                             related_query_name='player_team')
    game = models.PositiveSmallIntegerField(default=0)
    point = models.PositiveIntegerField(default=0)
    mp = models.DurationField(default=datetime.timedelta(days=0, seconds=0))
    tp = models.PositiveIntegerField(default=0)
    tpa = models.PositiveIntegerField(default=0)
    dp = models.PositiveIntegerField(default=0)
    dpa = models.PositiveIntegerField(default=0)
    ft = models.PositiveIntegerField(default=0)
    fta = models.PositiveIntegerField(default=0)
    orb = models.PositiveIntegerField(default=0)
    drb = models.PositiveIntegerField(default=0)
    ast = models.PositiveIntegerField(default=0)
    stl = models.PositiveIntegerField(default=0)
    blk = models.PositiveIntegerField(default=0)
    tov = models.PositiveIntegerField(default=0)
    foul = models.PositiveIntegerField(default=0)
    drw = models.PositiveIntegerField(default=0)

    def get_positions(self) -> list:
        """Obtiene una lista de las posiciones donde juega el propio jugador"""
        positions = []

        # self.position es una concatenación de las iniciales de las posiciones del jugador
        # por lo que se va a fraccionar para obtener una lista
        if len(self.position) % 2 == 0:
            for letra in range(0, len(self.position), 2):
                position = self.position[letra] + self.position[letra + 1]
                positions.append(Position(position))
        else:
            print(" *** ERROR EN LA POSICIÓN DEL JUGADOR ***")

        return positions

    def get_main_position(self) -> str:
        """Obtiene la posición principal del propio jugador"""
        position = ""

        # self.position es una concatenación de las iniciales de las posiciones del jugador
        # por lo que se va coger la primera posición
        if len(self.position) % 2 == 0:
            position = self.position[0] + self.position[1]
        else:
            print(" *** ERROR EN LA POSICIÓN DEL JUGADOR ***")

        return position

    class Meta:
        db_table = "player"

    def __str__(self):
        return self.name


class PlayerHist(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    season = models.ForeignKey(Season, on_delete=models.DO_NOTHING)
    game = models.PositiveSmallIntegerField(default=0)
    point = models.PositiveIntegerField(default=0)
    mp = models.DurationField(default=datetime.timedelta(days=0, seconds=0))
    tp = models.PositiveIntegerField(default=0)
    tpa = models.PositiveIntegerField(default=0)
    dp = models.PositiveIntegerField(default=0)
    dpa = models.PositiveIntegerField(default=0)
    ft = models.PositiveIntegerField(default=0)
    fta = models.PositiveIntegerField(default=0)
    orb = models.PositiveIntegerField(default=0)
    drb = models.PositiveIntegerField(default=0)
    ast = models.PositiveIntegerField(default=0)
    stl = models.PositiveIntegerField(default=0)
    blk = models.PositiveIntegerField(default=0)
    tov = models.PositiveIntegerField(default=0)
    foul = models.PositiveIntegerField(default=0)
    drw = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "player_hist"
        verbose_name_plural = "Player history"
        constraints = [
            models.UniqueConstraint(
                fields=['player', 'team', 'season'], name='unique_player_team_season_combination'
            )
        ]

    def __str__(self):
        return self.player + " - " + self.team + " - " + self.season


class Game(models.Model):
    class GameType(models.TextChoices):
        SEASON = 'SE'
        PLAY_IN = 'PI'
        PLAY_OFF = 'PO'
        PLAY_OFF_EAST_FIRST_ROUND = 'POER'
        PLAY_OFF_EAST_SEMIFINAL = 'POES'
        PLAY_OFF_EAST_FINAL = 'POEF'
        PLAY_OFF_WEST_FIRST_ROUND = 'POWR'
        PLAY_OFF_WEST_SEMIFINAL = 'POWS'
        PLAY_OFF_WEST_FINAL = 'POWF'
        PLAY_OFF_FINAL = 'POF'

    id = models.CharField(primary_key=True, max_length=12)
    season_month = models.ForeignKey(SeasonMonth, null=True, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=4, choices=GameType.choices, null=True)
    game_date = models.DateField(null=True)
    game_time = models.TimeField(null=True)
    visitor_team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING, related_name='games_visitor_team',
                                     related_query_name='game_visitor_team')
    visitor_point = models.PositiveSmallIntegerField(default=0)
    visitor_players = models.ManyToManyField(Player, through='GameVisitorPlayer', related_name='games_visitor_players',
                                             related_query_name='game_visitor_players')
    home_team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING, related_name='games_home_team',
                                  related_query_name='game_home_team')
    home_point = models.PositiveSmallIntegerField(default=0)
    home_players = models.ManyToManyField(Player, through='GameHomePlayer', related_name='games_home_players',
                                          related_query_name='game_home_players')
    prediction = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING, related_name='predictions_team',
                                   related_query_name='prediction_team')

    class Meta:
        db_table = "game"

    def __str__(self):
        return self.id


class GameVisitorPlayer(models.Model):
    id = models.CharField(primary_key=True, max_length=21)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gamevisitorplayers_game',
                             related_query_name='gamevisitorplayer_game')
    player = models.ForeignKey(Player, default=None, on_delete=models.DO_NOTHING,
                               related_name='gamevisitorplayers_player', related_query_name='gamevisitorplayer_player')
    mp = models.TimeField(default=datetime.timedelta(minutes=0))

    class Meta:
        db_table = "game_visitor_player"


class GameHomePlayer(models.Model):
    id = models.CharField(primary_key=True, max_length=21)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gamehomeplayers_game',
                             related_query_name='gamehomeplayer_game')
    player = models.ForeignKey(Player, default=None, on_delete=models.DO_NOTHING,
                               related_name='gamehomeplayers_player', related_query_name='gamehomeplayer_player')
    mp = models.TimeField(default=datetime.timedelta(minutes=0))

    class Meta:
        db_table = "game_home_player"


class Play(models.Model):
    id = models.CharField(primary_key=True, max_length=15)
    quarter = models.PositiveSmallIntegerField(default=1)
    play_time = models.TimeField(default=datetime.time(0, 0, 0))
    text = models.TextField(default='')

    class Meta:
        abstract = True


class ThreePointerPlay(Play):
    distance = models.PositiveSmallIntegerField(default=0)
    hit = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='threepointerplays_team',
                             related_query_name='threepointerplay_team')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='threepointerplays_game',
                             related_query_name='threepointerplay_game')
    player = models.ForeignKey(Player, default=None, on_delete=models.DO_NOTHING,
                               related_name='threepointerplay_player', related_query_name='threepointerplay_player')
    assist = models.ForeignKey(Player, null=True, default=None, on_delete=models.DO_NOTHING,
                               related_name='threepointerplay_assist', related_query_name='threepointerplay_assist')
    block = models.ForeignKey(Player, null=True, default=None, on_delete=models.DO_NOTHING,
                              related_name='threepointerplay_block', related_query_name='threepointerplay_block')

    class Meta:
        db_table = "three_pointer_play"

    def __str__(self):
        return self.text


class TwoPointerPlay(Play):
    distance = models.PositiveSmallIntegerField(default=0)
    hit = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='twopointerplays_team',
                             related_query_name='twopointerplay_team')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='twopointerplays_game',
                             related_query_name='twopointerplay_game')
    player = models.ForeignKey(Player, default=None, on_delete=models.DO_NOTHING,
                               related_name='twopointerplay_player', related_query_name='twopointerplay_player')
    assist = models.ForeignKey(Player, null=True, default=None, on_delete=models.DO_NOTHING,
                               related_name='twopointerplay_assist', related_query_name='twopointerplay_assist')
    block = models.ForeignKey(Player, null=True, default=None, on_delete=models.DO_NOTHING,
                              related_name='twopointerplay_block', related_query_name='twopointerplay_block')

    class Meta:
        db_table = "two_pointer_play"

    def __str__(self):
        return self.text


class FreeThrowPlay(Play):
    hit = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='freethrowplays_team',
                             related_query_name='freethrowplay_team')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='freethrowplays_game',
                             related_query_name='freethrowplay_game')
    player = models.ForeignKey(Player, default=None, on_delete=models.DO_NOTHING,
                               related_name='freethrowplay_player', related_query_name='freethrowplay_player')

    class Meta:
        db_table = "free_throw_play"

    def __str__(self):
        return self.text


class ReboundPlay(Play):
    class ReboundType(models.TextChoices):
        OFFENSIVE = 'O'
        DEFENSIVE = 'D'
        UNKNOWN = 'X'

    type = models.CharField(max_length=1, choices=ReboundType.choices)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='reboundplays_team',
                             related_query_name='reboundplay_team')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reboundplays_game',
                             related_query_name='reboundplay_game')
    player = models.ForeignKey(Player, null=True, default=None, on_delete=models.DO_NOTHING,
                               related_name='reboundplay_player', related_query_name='reboundplay_player')

    class Meta:
        db_table = "rebound_play"

    def __str__(self):
        return self.text


class TurnoverPlay(Play):
    class TurnoverType(models.TextChoices):
        LOST_BALL = 'LB'
        BAD_PASS = 'BP'
        TRAVELING = 'TR'
        STEP_OUT_OF_BOUNDS = 'SB'
        OFFENSIVE_FOUL = 'OF'
        SHOT_CLOCK = 'SC'
        OUT_OF_BOUNDS_LOST_BALL = 'OL'
        PALMING = 'PA'
        DRIBBLE = 'DB'
        TSEC = 'TS'
        OFF_GOALTENDING = 'OG'
        UNKNOWN = 'XX'

    type = models.CharField(max_length=2, choices=TurnoverType.choices)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='turnoverplays_team',
                             related_query_name='turnoverplay_team')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='turnoverplays_game',
                             related_query_name='turnoverplay_game')
    player = models.ForeignKey(Player, null=True, default=None, on_delete=models.DO_NOTHING,
                               related_name='turnoverplay_player', related_query_name='turnoverplay_player')
    steal = models.ForeignKey(Player, null=True, default=None, on_delete=models.DO_NOTHING,
                              related_name='turnoverplay_steal', related_query_name='turnoverplay_steal')

    class Meta:
        db_table = "turnover_play"

    def __str__(self):
        return self.text


class FoulPlay(Play):
    class FoulType(models.TextChoices):
        SHOOTING = 'SH'
        LOOSE_BALL = 'LB'
        OFFENSIVE_CHARGE = 'OC'
        OFFENSIVE = 'OF'
        TECHNICAL = 'TE'
        AWAY_FROM_PLAY = 'AF'
        PERSONAL = 'PE'
        FLAGRANT = 'FL'
        CLEAR_PATH = 'CP'
        UNKNOWN = 'XX'

    type = models.CharField(max_length=2, choices=FoulType.choices)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='foulplays_team',
                             related_query_name='foulplay_team')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='foulplays_game',
                             related_query_name='foulplay_game')
    player = models.ForeignKey(Player, null=True, default=None, on_delete=models.DO_NOTHING,
                               related_name='foulplay_player', related_query_name='foulplay_player')
    drawn = models.ForeignKey(Player, null=True, default=None, on_delete=models.DO_NOTHING,
                              related_name='foulplay_drawn', related_query_name='foulplay_drawn')

    class Meta:
        db_table = "foul_play"

    def __str__(self):
        return self.text


class SubstitutionPlay(Play):
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='substitutionplays_team',
                             related_query_name='substitutionplay_team')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='substitutionplays_game',
                             related_query_name='substitutionplay_game')
    enter = models.ForeignKey(Player, null=True, default=None, on_delete=models.DO_NOTHING,
                              related_name='substitutionplay_enter', related_query_name='substitutionplay_enter')
    leave = models.ForeignKey(Player, null=True, default=None, on_delete=models.DO_NOTHING,
                              related_name='substitutionplay_leave', related_query_name='substitutionplay_leave')

    class Meta:
        db_table = "substitution_play"

    def __str__(self):
        return self.text
