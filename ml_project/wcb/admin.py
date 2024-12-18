from django.contrib import admin

from wcb.models import ClaimPrediction


@admin.register(ClaimPrediction)
class PredictionsAdmin(admin.ModelAdmin):
    pass