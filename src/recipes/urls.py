


from django.conf.urls import url
from django.contrib import admin
from .views import (
	recipe_list,
	recipe_create,
	recipe_detail,
	recipe_update,
	recipe_delete,
	)

urlpatterns = [
    url(r'^$', recipe_list, name='list'),
    url(r'^create/$', recipe_create),
    url(r'^(?P<slug>[\w-]+)/$', recipe_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', recipe_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', recipe_delete),
]
 