from django.contrib import admin
from .models import *

# Register your models here.
class TacksAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'is_deleted', 'create_date', 'update_date')
	list_filter = ('user', 'is_deleted')

	fieldsets = (
        ('트랙 정보', {'fields': ('title', 'slug', 'tape_info', 'lyrics', 'hashtag', 'user', 'is_deleted')}),
        ('사운드 클라우드 트랙 정보', {'fields': ('track_id', 'genre', 'image_url', 'download_url', 'waveform_url')}),
        ('집계', {'fields': ('view_count', 'comments', 'likes', 'clips', 'track_score', 'on_stage')})
    )

	# readonly_fields = ('track_id', 'view_count', 'comments','clips', 'likes', 'image_url', 'download_url', 'waveform_url', 'genre')
	prepopulated_fields = {'slug': ('title',)}
	list_per_page = 10



# class DeleteTrackAdmin(admin.ModelAdmin):
# 	list_display = ('track_id', 'title', 'user', 'delete_date')
# 	list_filter = ('user', 'delete_date')

# 	fieldsets = (
#         ('트랙 정보', {'fields': ('track_id', 'title', 'slug', 'tape_info', 'lyrics', 'hashtag', 'user')}),
#         ('사운드 클라우드 트랙 정보', {'fields': ('genre', 'image_url', 'download_url', 'waveform_url')}),
#         ('집계', {'fields': ('view_count', 'comments', 'likes', 'clips', 'track_score', 'on_stage')})
#     )
# 	list_per_page = 10

# 	def get_readonly_fields(self, request, obj=None):
# 		if obj:
# 			self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
# 		return self.readonly_fields

# 	def change_view(self, request, object_id, extra_context=None):
# 		extra_context = extra_context or {}
# 		extra_context['show_save_and_continue'] = False
# 		extra_context['show_save'] = False

# 		return super(DeleteTrackAdmin, self).change_view(request, object_id, extra_context=extra_context)

# 	def has_add_permission(self, request):
# 		return False

# 	def has_change_permission(self, request, obj=None):
# 		return (request.method in ['GET', 'HEAD'] and super().has_change_permission(request, obj))

# 	def has_delete_permission(self, request, obj=None):
# 		return False


class TrackCommentAdmin(admin.ModelAdmin):
	list_display = ('contents', 'track', 'parent', 'user', 'is_deleted', 'create_date')
	list_filter = ('is_deleted',)
	list_per_page = 10
	
class TrackLikeTypeAdmin(admin.ModelAdmin):
	list_display = ('like_type',)
	list_per_page = 10

class TrackLikeLogAdmin(admin.ModelAdmin):
	list_display = ('track_like_type', 'track', 'user', 'create_date')
	list_per_page = 10


admin.site.register(Track, TacksAdmin)
# admin.site.register(DeleteTrack, DeleteTrackAdmin)
admin.site.register(TrackComment, TrackCommentAdmin)
admin.site.register(TrackLikeType, TrackLikeTypeAdmin)
admin.site.register(TrackLikeLog, TrackLikeLogAdmin)