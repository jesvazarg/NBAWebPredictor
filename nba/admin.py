from django.contrib import admin
from .models import Season, SeasonMonth, Team, TeamHist, Player, PlayerHist, Game, ThreePointerPlay, TwoPointerPlay, \
    FreeThrowPlay \
    , ReboundPlay, TurnoverPlay, FoulPlay, GameVisitorPlayer, GameHomePlayer, SubstitutionPlay

# Register your models here.
admin.site.register(Season)
admin.site.register(SeasonMonth)
admin.site.register(Team)
admin.site.register(TeamHist)
admin.site.register(Player)
admin.site.register(PlayerHist)
admin.site.register(Game)
admin.site.register(GameVisitorPlayer)
admin.site.register(GameHomePlayer)
admin.site.register(ThreePointerPlay)
admin.site.register(TwoPointerPlay)
admin.site.register(FreeThrowPlay)
admin.site.register(ReboundPlay)
admin.site.register(TurnoverPlay)
admin.site.register(FoulPlay)
admin.site.register(SubstitutionPlay)
