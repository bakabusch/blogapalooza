from __future__ import unicode_literals
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

class PostManager(models.Manager): #model manager -- controls how models work like Post.objects.all()
    def active(self, *args, **kwargs): #overriding the default all so that objects.all doesn't include draft & published in future
        #so: Post.objects.all() now is super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

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
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager() #instantiating PostManager into model

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]

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



pre_save.connect(pre_save_post_receiver, sender=Post)