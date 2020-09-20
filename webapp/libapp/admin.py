from django.contrib import admin
from django.utils.html import format_html_join
# Register your models here.
from .models import Asset, Tag



class AssetAdmin(admin.ModelAdmin):
    exclude = ('id',)
    list_display = ('name','pub_notes', 'get_tags')

    def get_tags(self, obj):
        return format_html_join(
            '\n', "{} <br>",
            ((t.name,) for t in obj.tags.all())
        )


class TagAdmin(admin.ModelAdmin):
    exclude = ('id',)
    list_display = ('name', 'popularity')

admin.site.register(Asset, AssetAdmin)
admin.site.register(Tag, TagAdmin)