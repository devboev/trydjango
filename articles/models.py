
from django.conf import settings

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save,post_save
from django.utils import timezone
from django.urls import reverse

from articles.utils import slugify_instance_title

User =settings.AUTH_USER_MODEL 

class ArticleQuerySet(models.QuerySet):
    '''
    possible to do objects.filter('t').search('...')
    '''
    def search(self,q=None):
        if q is None or q == '':
            return self.none()
        lookup =  Q(title__icontains=q) | Q(content__icontains=q) 
        return self.filter(lookup)

class ArticleManager(models.Manager):
    
    def get_queryset(self):
        return ArticleQuerySet(self.model,using=self._db)
    
    def search(self,q=None):
        return self.get_queryset().search(q=q)



class Article(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField( unique = True, null=True,blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True)
    
    objects = ArticleManager()
    
    @property
    def name(self):
        return self.title
    
    def save(self, *args,**kwargs):
        super().save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse("articles:detail",kwargs={"slug":self.slug})       
   

def article_pre_save(sender, instance ,*args,**kwargs):
    if instance.slug is None: 
        slugify_instance_title(instance, save=False)
        
    
pre_save.connect(article_pre_save,sender=Article)    

def article_post_save(sender, instance , created, *args,**kwargs):
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save,sender=Article)        