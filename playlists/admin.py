from django.contrib import admin
from .models import *

# Register your models here.
class PlayListAdmin(admin.ModelAdmin):
	list_display = ('track', 'user', 'order')
	

	# fieldsets = (
    #     ('트랙 정보', {'fields': ('title', 'slug', 'tape_info', 'lyrics', 'hashtag', 'user', 'is_deleted')}),
    #     ('사운드 클라우드 트랙 정보', {'fields': ('track_id', 'genre', 'image_url', 'download_url', 'waveform_url')}),
    #     ('집계', {'fields': ('view_count', 'comments', 'likes', 'clips', 'track_score', 'on_stage')})
    # )

	# readonly_fields = ('track_id', 'view_count', 'comments','clips', 'likes', 'image_url', 'download_url', 'waveform_url', 'genre')
	# prepopulated_fields = {'slug': ('title',)}
	list_per_page = 10

admin.site.register(PlayList, PlayListAdmin)