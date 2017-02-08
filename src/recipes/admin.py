from django.contrib import admin
from .models import Recipe


class RecipeModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_filter = ["updated", "timestamp"]
    list_editable = ["title"]
    search_fields = ["title", "content"]

    class Meta:
        model = Recipe


# Register your models here.
admin.site.register(Recipe, RecipeModelAdmin)


# Register your models here.
