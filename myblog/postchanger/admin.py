from django.contrib import admin

from .models import*

class ArtPostAdmin(admin.ModelAdmin):
    list_display=('id','title','author','time_create')
    list_display_links=('id','title')
    search_fields=('title','content')
    list_filter=('time_create',)
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','name')
    list_display_links=('id','name')
    search_fields=('name',)
    prepopulated_fields={"slug":("name",)}






admin.site.register(ArtPost, ArtPostAdmin)
admin.site.register(Category, CategoryAdmin)


