from django.contrib import admin
from .models import LogType, PlayListLog

# Register your models here.
class LogTypeAdmin(admin.ModelAdmin):
    pass
    

class PlayListLogAdmin(admin.ModelAdmin):
    pass

# class PlayList
admin.site.register(LogType, LogTypeAdmin)
admin.site.register(PlayListLog, PlayListLogAdmin)