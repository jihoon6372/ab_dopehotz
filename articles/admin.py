from django.contrib import admin
from .models import Article

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_per_page = 10

admin.site.register(Article, ArticleAdmin)