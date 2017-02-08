
try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from comments.forms import CommentForm
from comments.models import Comment
from .forms import RecipeForm #refactor
from .models import Recipe #refactor
#from .utils import get_read_time

def recipe_list(request):
    today = timezone.now().date
    queryset_list = Recipe.objects.active()#filter(draft=False).filter(publish__lte=timezone.now())#all()  # .order_by("-timestamp") --changed in models with class meta instead
    #filtering stuff so that drafts and things to be published in the future don't show but now done as model manager instead
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Recipe.objects.all() #allows all posts (draft and future) to be seen
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 10)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'object_list': queryset,
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "recipe_list.html", context)
"""

"""

def recipe_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = RecipeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successsfully Created")
        return HttpResponseRedirect(instance.get_absolute_url()) 
    context = {
        "form": form,
    }
    return render(request, "recipe_form.html", context)


def recipe_detail(request, slug=None):
    instance = get_object_or_404(Recipe, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    
    initial_data = {
            "content_type": instance.get_content_type, 
            "object_id": instance.id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None #declare parent obj as none
        try:
            parent_id = int(request.POST.get("parent_id")) #make sure we have parent id
        except:
            parent_id = None  
            
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id) #if we have an id, we run queryset to see if id is in db
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()  #if it exists, we'll use it         
        
        new_comment, created = Comment.objects.get_or_create(
                            user = request.user,
                            content_type = content_type,
                            object_id = obj_id,
                            content = content_data,
                            parent = parent_obj,
                        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

        
    comments = instance.comments #Comment.objects.filter_by_instance(instance)
    context = {
        "title": "instance.title",
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form, 
    }
    return render(request, "recipe_detail.html", context)
"""

"""


def recipe_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Recipe, slug=slug)
    form = RecipeForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "instance.title",
        "instance": instance,
        "form": form,
    }
    return render(request, "recipe_form.html", context)


def recipe_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Recipe, slug=slug)
    instance.delete()
    messages.success(request, "Successsfully Deleted")
    return redirect("recipes:list")


