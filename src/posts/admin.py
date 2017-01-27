from django.contrib import admin
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp"]
    list_filter = ["title", "updated", "timestamp"]
    list_editable = ["title"]
    search_fields = ["title", "content"]

    class Meta:
        model = Post


# Register your models here.
admin.site.register(Post, PostModelAdmin)
