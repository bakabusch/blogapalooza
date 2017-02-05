from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from .utils import get_read_time
from markdown_deux import markdown
from comments.models import Comment

class PostManager(models.Manager): #model manager -- controls how models work like Post.objects.all()
    def active(self, *args, **kwargs): #overriding the default all so that objects.all doesn't include draft & published in future
        #so: Post.objects.all() now is super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. Must use this method bc model is defined below. Then create queryset ordered by the "ids"
    of each object. Then get last object in the queryset with '.last()'. Which will give us most recently created model instance. 
    Add 1 to it to get what should be the same id as post we're creating.
    """
    return "%s/%s" %(new_id, filename)

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True) #creates url based on title of model rather than pk -- delete all media files and db as well
    image = models.ImageField(upload_to=upload_location,
            null=True,
            blank=True,
            width_field="width_field",
            height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    read_time = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager() #instantiating PostManager into model

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug}) #should be slug not "id"

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property   #decorator indicating a property not a method
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property   
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

"""




"""
def create_slug(instance, new_slug=None): #recursive function
    slug = slugify(instance.title) #slugify the title
    if new_slug is not None: #if slug is new
        slug = new_slug #then slug = new slug
    qs = Post.objects.filter(slug=slug).order_by("-id") #check if slug exists
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id) #if slug exists we add to it
        return create_slug(instance, new_slug=new_slug)
    return slug #otherwise just return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=Post)
