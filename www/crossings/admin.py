from django.contrib import admin

from .models import Comment, Crossing


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'lastUpdate')
    list_filter = ['lastUpdate']
    search_fields = ['text']


class CrossingAdmin(admin.ModelAdmin):
    list_display = ('name', 'countryFrom', 'countryTo')
    list_filter = ['countryFrom', 'countryTo', 'lastUpdate']
    search_fields = ['name', 'otherNames']

admin.site.register(Comment, CommentAdmin)
admin.site.register(Crossing, CrossingAdmin)
