from django.test import TestCase
from django.utils.text import slugify

from articles.models import Article
from .utils import slugify_instance_title

class ArticleTestCase(TestCase):
    
    def setUp(self):
        self.number_of_articles = 500
        for i in range(0,self.number_of_articles):
            Article.objects.create(title= 'hello world',content = 'fsdfsdf efffda sdfsdf')

    def test_queryset_exists(self):
        qs = Article.objects.all()
        # print(qs.count())
        self.assertTrue(qs.exists())
    
    def test_queryset_count(self):
        qs = Article.objects.all()
        # print(qs.count())
        self.assertEqual(qs.count(),self.number_of_articles)    

    def test_helloworld_slug(self):
        obj = Article.objects.all().order_by("id").first()
        slug = obj.slug
        slugified_title = slugify(obj.title) 
        self.assertEqual(slug,slugified_title)    
    
    def test_helloworld_unique_slug(self):
        qs = Article.objects.exclude(slug__iexact='hello-world')
        for obj in qs:
            slug = obj.slug
            slugified_title = slugify(obj.title) 
        self.assertNotEqual(slug,slugified_title)
    
    def test_slugify_instance_title(self):   
        obj = Article.objects.all().last()
        new_slugs = []
        for i in range(0,5):
            instance = slugify_instance_title (obj,save=False)
            new_slugs.append(instance.slug)
            
            
        unique_slugs = list(set(new_slugs))# Set items are unordered, unchangeable, and do not allow duplicate values.

        self.assertEqual(len(new_slugs),len(unique_slugs)) 

    def test_slugify_instance_title_redux(self):   
        slug_list = Article.objects.values_list('slug',flat=True)
        unique_slug_list = list(set(slug_list))
        self.assertEqual(len(slug_list),len(unique_slug_list)) 
    
    def test_user_added_slug_unique(self):
        slug_to_check = 'hello-worldx'
        qs = Article.objects.filter(slug__iexact=slug_to_check)
        self.assertFalse(qs.exists())
        
    #test search 
    def test_article_search_manager(self):
        qs = Article.objects.search(q='hello world')
        self.assertEqual(qs.count(),self.number_of_articles)
        qs = Article.objects.search(q='hello ')
        self.assertEqual(qs.count(),self.number_of_articles)
        qs = Article.objects.search(q=' efffda ')
        self.assertEqual(qs.count(),self.number_of_articles)
       
        
            