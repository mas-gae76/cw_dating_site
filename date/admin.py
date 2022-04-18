from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'birthday', 'avatar', 'gender', )
    list_display_links = ('email', )
    search_fields = ('first_name', 'last_name', 'email', )


@admin.register(Rating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    search_fields = ('user', )


@admin.register(Sympathy)
class UserSympathyAdmin(admin.ModelAdmin):
    list_display = ('who', 'whom', 'matching')
    search_fields = ('who', 'whom')


@admin.register(UserSettings)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'setting', 'value')
    search_fields = ('user', 'setting')


admin.site.site_header = 'Сайт знакомств GetPair'
