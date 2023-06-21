# Generated by Django 4.1.7 on 2023-05-24 15:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('SE', 'Season'), ('PI', 'Play In'), ('PO', 'Play Off'), ('POER', 'Play Off East First Round'), ('POES', 'Play Off East Semifinal'), ('POEF', 'Play Off East Final'), ('POWR', 'Play Off West First Round'), ('POWS', 'Play Off West Semifinal'), ('POWF', 'Play Off West Final'), ('POF', 'Play Off Final')], max_length=4, null=True)),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True)),
                ('visitor_point', models.PositiveSmallIntegerField(default=0)),
                ('home_point', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'game',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('number', models.PositiveSmallIntegerField(null=True)),
                ('photo', models.ImageField(null=True, upload_to='players')),
                ('dob', models.DateField(null=True)),
                ('position', models.CharField(max_length=10, null=True)),
                ('shoot', models.CharField(choices=[('R', 'Right'), ('L', 'Left')], max_length=1, null=True)),
                ('height', models.PositiveSmallIntegerField(default=0, null=True)),
                ('weight', models.PositiveSmallIntegerField(default=0, null=True)),
                ('game', models.PositiveSmallIntegerField(default=0)),
                ('point', models.PositiveIntegerField(default=0)),
                ('mp', models.TimeField(default=datetime.timedelta(0))),
                ('tp', models.PositiveIntegerField(default=0)),
                ('tpa', models.PositiveIntegerField(default=0)),
                ('dp', models.PositiveIntegerField(default=0)),
                ('dpa', models.PositiveIntegerField(default=0)),
                ('ft', models.PositiveIntegerField(default=0)),
                ('fta', models.PositiveIntegerField(default=0)),
                ('orb', models.PositiveIntegerField(default=0)),
                ('drb', models.PositiveIntegerField(default=0)),
                ('ast', models.PositiveIntegerField(default=0)),
                ('stl', models.PositiveIntegerField(default=0)),
                ('blk', models.PositiveIntegerField(default=0)),
                ('tov', models.PositiveIntegerField(default=0)),
                ('foul', models.PositiveIntegerField(default=0)),
                ('drw', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'player',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=7)),
            ],
            options={
                'db_table': 'season',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(default=None, null=True, upload_to='teams')),
                ('conference', models.CharField(choices=[('E', 'Eastern'), ('W', 'Western')], max_length=1, null=True)),
                ('division', models.CharField(choices=[('AT', 'Atlantic'), ('CE', 'Central'), ('SE', 'Southeast'), ('NW', 'Northwest'), ('PA', 'Pacific'), ('SW', 'Southwest')], max_length=2, null=True)),
                ('coach', models.CharField(blank=True, max_length=50, null=True)),
                ('arena', models.CharField(blank=True, max_length=50, null=True)),
                ('game', models.PositiveSmallIntegerField(default=0)),
                ('point', models.PositiveIntegerField(default=0)),
                ('tp', models.PositiveIntegerField(default=0)),
                ('tpa', models.PositiveIntegerField(default=0)),
                ('dp', models.PositiveIntegerField(default=0)),
                ('dpa', models.PositiveIntegerField(default=0)),
                ('ft', models.PositiveIntegerField(default=0)),
                ('fta', models.PositiveIntegerField(default=0)),
                ('orb', models.PositiveIntegerField(default=0)),
                ('drb', models.PositiveIntegerField(default=0)),
                ('ast', models.PositiveIntegerField(default=0)),
                ('stl', models.PositiveIntegerField(default=0)),
                ('blk', models.PositiveIntegerField(default=0)),
                ('tov', models.PositiveIntegerField(default=0)),
                ('foul', models.PositiveIntegerField(default=0)),
                ('drw', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'team',
            },
        ),
        migrations.CreateModel(
            name='TwoPointerPlay',
            fields=[
                ('id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('quarter', models.PositiveSmallIntegerField(default=1)),
                ('time', models.TimeField(default=datetime.time(0, 0))),
                ('text', models.TextField(default='')),
                ('distance', models.PositiveSmallIntegerField(default=0)),
                ('hit', models.BooleanField(default=False)),
                ('assist', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='twopointerplay_assist', related_query_name='twopointerplay_assist', to='nba.player')),
                ('block', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='twopointerplay_block', related_query_name='twopointerplay_block', to='nba.player')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='twopointerplays_game', related_query_name='twopointerplay_game', to='nba.game')),
                ('player', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='twopointerplay_player', related_query_name='twopointerplay_player', to='nba.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='twopointerplays_team', related_query_name='twopointerplay_team', to='nba.team')),
            ],
            options={
                'db_table': 'two_pointer_play',
            },
        ),
        migrations.CreateModel(
            name='TurnoverPlay',
            fields=[
                ('id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('quarter', models.PositiveSmallIntegerField(default=1)),
                ('time', models.TimeField(default=datetime.time(0, 0))),
                ('text', models.TextField(default='')),
                ('type', models.CharField(choices=[('LB', 'Lost Ball'), ('BP', 'Bad Pass'), ('TR', 'Traveling'), ('SB', 'Step Out Of Bounds'), ('OF', 'Offensive Foul'), ('SC', 'Shot Clock'), ('OL', 'Out Of Bounds Lost Ball'), ('PA', 'Palming'), ('DB', 'Dribble'), ('TS', 'Tsec'), ('OG', 'Off Goaltending'), ('XX', 'Unknown')], max_length=2)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turnoverplays_game', related_query_name='turnoverplay_game', to='nba.game')),
                ('player', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='turnoverplay_player', related_query_name='turnoverplay_player', to='nba.player')),
                ('steal', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='turnoverplay_steal', related_query_name='turnoverplay_steal', to='nba.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='turnoverplays_team', related_query_name='turnoverplay_team', to='nba.team')),
            ],
            options={
                'db_table': 'turnover_play',
            },
        ),
        migrations.CreateModel(
            name='ThreePointerPlay',
            fields=[
                ('id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('quarter', models.PositiveSmallIntegerField(default=1)),
                ('time', models.TimeField(default=datetime.time(0, 0))),
                ('text', models.TextField(default='')),
                ('distance', models.PositiveSmallIntegerField(default=0)),
                ('hit', models.BooleanField(default=False)),
                ('assist', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='threepointerplay_assist', related_query_name='threepointerplay_assist', to='nba.player')),
                ('block', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='threepointerplay_block', related_query_name='threepointerplay_block', to='nba.player')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threepointerplays_game', related_query_name='threepointerplay_game', to='nba.game')),
                ('player', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='threepointerplay_player', related_query_name='threepointerplay_player', to='nba.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='threepointerplays_team', related_query_name='threepointerplay_team', to='nba.team')),
            ],
            options={
                'db_table': 'three_pointer_play',
            },
        ),
        migrations.CreateModel(
            name='TeamHist',
            fields=[
                ('id', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('game', models.PositiveSmallIntegerField(default=0)),
                ('point', models.PositiveIntegerField(default=0)),
                ('tp', models.PositiveIntegerField(default=0)),
                ('tpa', models.PositiveIntegerField(default=0)),
                ('dp', models.PositiveIntegerField(default=0)),
                ('dpa', models.PositiveIntegerField(default=0)),
                ('ft', models.PositiveIntegerField(default=0)),
                ('fta', models.PositiveIntegerField(default=0)),
                ('orb', models.PositiveIntegerField(default=0)),
                ('drb', models.PositiveIntegerField(default=0)),
                ('ast', models.PositiveIntegerField(default=0)),
                ('stl', models.PositiveIntegerField(default=0)),
                ('blk', models.PositiveIntegerField(default=0)),
                ('tov', models.PositiveIntegerField(default=0)),
                ('foul', models.PositiveIntegerField(default=0)),
                ('drw', models.PositiveIntegerField(default=0)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nba.season')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nba.team')),
            ],
            options={
                'verbose_name_plural': 'Team history',
                'db_table': 'team_hist',
            },
        ),
        migrations.CreateModel(
            name='SubstitutionPlay',
            fields=[
                ('id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('quarter', models.PositiveSmallIntegerField(default=1)),
                ('time', models.TimeField(default=datetime.time(0, 0))),
                ('text', models.TextField(default='')),
                ('enter', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='substitutionplay_enter', related_query_name='substitutionplay_enter', to='nba.player')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='substitutionplays_game', related_query_name='substitutionplay_game', to='nba.game')),
                ('leave', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='substitutionplay_leave', related_query_name='substitutionplay_leave', to='nba.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='substitutionplays_team', related_query_name='substitutionplay_team', to='nba.team')),
            ],
            options={
                'db_table': 'substitution_play',
            },
        ),
        migrations.CreateModel(
            name='SeasonMonth',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('month', models.CharField(max_length=14)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nba.season')),
            ],
            options={
                'db_table': 'season_month',
            },
        ),
        migrations.CreateModel(
            name='ReboundPlay',
            fields=[
                ('id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('quarter', models.PositiveSmallIntegerField(default=1)),
                ('time', models.TimeField(default=datetime.time(0, 0))),
                ('text', models.TextField(default='')),
                ('type', models.CharField(choices=[('O', 'Offensive'), ('D', 'Defensive'), ('X', 'Unknown')], max_length=1)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reboundplays_game', related_query_name='reboundplay_game', to='nba.game')),
                ('player', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reboundplay_player', related_query_name='reboundplay_player', to='nba.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reboundplays_team', related_query_name='reboundplay_team', to='nba.team')),
            ],
            options={
                'db_table': 'rebound_play',
            },
        ),
        migrations.CreateModel(
            name='PlayerHist',
            fields=[
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('game', models.PositiveSmallIntegerField(default=0)),
                ('point', models.PositiveIntegerField(default=0)),
                ('mp', models.TimeField(default=datetime.timedelta(0))),
                ('tp', models.PositiveIntegerField(default=0)),
                ('tpa', models.PositiveIntegerField(default=0)),
                ('dp', models.PositiveIntegerField(default=0)),
                ('dpa', models.PositiveIntegerField(default=0)),
                ('ft', models.PositiveIntegerField(default=0)),
                ('fta', models.PositiveIntegerField(default=0)),
                ('orb', models.PositiveIntegerField(default=0)),
                ('drb', models.PositiveIntegerField(default=0)),
                ('ast', models.PositiveIntegerField(default=0)),
                ('stl', models.PositiveIntegerField(default=0)),
                ('blk', models.PositiveIntegerField(default=0)),
                ('tov', models.PositiveIntegerField(default=0)),
                ('foul', models.PositiveIntegerField(default=0)),
                ('drw', models.PositiveIntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nba.player')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nba.season')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nba.team')),
            ],
            options={
                'verbose_name_plural': 'Player history',
                'db_table': 'player_hist',
            },
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='players_team', related_query_name='player_team', to='nba.team'),
        ),
        migrations.CreateModel(
            name='GameVisitorPlayers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mp', models.TimeField(default=datetime.timedelta(0))),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gamevisitorplayers_game', related_query_name='gamevisitorplayer_game', to='nba.game')),
                ('player', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gamevisitorplayers_player', related_query_name='gamevisitorplayer_player', to='nba.player')),
            ],
            options={
                'db_table': 'game_visitor_players',
            },
        ),
        migrations.CreateModel(
            name='GameHomePlayers',
            fields=[
                ('id', models.CharField(max_length=21, primary_key=True, serialize=False)),
                ('mp', models.TimeField(default=datetime.timedelta(0))),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gamehomeplayers_game', related_query_name='gamehomeplayer_game', to='nba.game')),
                ('player', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gamehomeplayers_player', related_query_name='gamehomeplayer_player', to='nba.player')),
            ],
            options={
                'db_table': 'game_home_players',
            },
        ),
        migrations.AddField(
            model_name='game',
            name='home_players',
            field=models.ManyToManyField(related_name='games_home_players', related_query_name='game_home_players', through='nba.GameHomePlayers', to='nba.player'),
        ),
        migrations.AddField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='games_home_team', related_query_name='game_home_team', to='nba.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='season_month',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='nba.seasonmonth'),
        ),
        migrations.AddField(
            model_name='game',
            name='visitor_players',
            field=models.ManyToManyField(related_name='games_visitor_players', related_query_name='game_visitor_players', through='nba.GameVisitorPlayers', to='nba.player'),
        ),
        migrations.AddField(
            model_name='game',
            name='visitor_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='games_visitor_team', related_query_name='game_visitor_team', to='nba.team'),
        ),
        migrations.CreateModel(
            name='FreeThrowPlay',
            fields=[
                ('id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('quarter', models.PositiveSmallIntegerField(default=1)),
                ('time', models.TimeField(default=datetime.time(0, 0))),
                ('text', models.TextField(default='')),
                ('hit', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='freethrowplays_game', related_query_name='freethrowplay_game', to='nba.game')),
                ('player', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='freethrowplay_player', related_query_name='freethrowplay_player', to='nba.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='freethrowplays_team', related_query_name='freethrowplay_team', to='nba.team')),
            ],
            options={
                'db_table': 'free_throw_play',
            },
        ),
        migrations.CreateModel(
            name='FoulPlay',
            fields=[
                ('id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('quarter', models.PositiveSmallIntegerField(default=1)),
                ('time', models.TimeField(default=datetime.time(0, 0))),
                ('text', models.TextField(default='')),
                ('type', models.CharField(choices=[('SH', 'Shooting'), ('LB', 'Loose Ball'), ('OC', 'Offensive Charge'), ('OF', 'Offensive'), ('TE', 'Technical'), ('AF', 'Away From Play'), ('PE', 'Personal'), ('FL', 'Flagrant'), ('CP', 'Clear Path'), ('XX', 'Unknown')], max_length=2)),
                ('drawn', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='foulplay_drawn', related_query_name='foulplay_drawn', to='nba.player')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foulplays_game', related_query_name='foulplay_game', to='nba.game')),
                ('player', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='foulplay_player', related_query_name='foulplay_player', to='nba.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='foulplays_team', related_query_name='foulplay_team', to='nba.team')),
            ],
            options={
                'db_table': 'foul_play',
            },
        ),
        migrations.AddConstraint(
            model_name='teamhist',
            constraint=models.UniqueConstraint(fields=('team', 'season'), name='unique_team_season_combination'),
        ),
        migrations.AddConstraint(
            model_name='playerhist',
            constraint=models.UniqueConstraint(fields=('player', 'team', 'season'), name='unique_player_team_season_combination'),
        ),
    ]
