from django import forms

from pagedown.widgets import PagedownWidget

from .models import Recipe


class RecipeForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    ingredient = forms.CharField(widget=PagedownWidget(show_preview=False))
    intro = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Recipe
        fields = [
            "title",
            "intro",
            "ingredient",
            "content",
            "image",
            "draft",
            "prep_time",
            "cook_time",
            "publish",
        ]