from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404


from articles.models import Article
from articles.forms import ArticleForm


# Create your views here.

def index(request):
    qs = Article.objects.all()

    if qs:
        return render(request,'articles/home_view.html',{'articles':qs})
    
def article_detail_view(request,slug=None):
    try:
        article = Article.objects.get(slug=slug) 
    except Article.DoesNotExist:
        raise Http404
    except Article.MultipleObjectsReturned:
        article = Article.objects.filter(slug=slug).first()
    except:
        raise Http404
        # article = Article.objects.none()
        
    return render(request,'articles/detail_view.html',{'article':article}) 

@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context={
        "form":form
    }

    if form.is_valid():
        article_object =form.save()
        context['form'] = ArticleForm()
        return redirect(article_object.get_absolute_url())

    return render(request,'articles/create.html',context) 

def article_search_view(request):

    try:
        q = request.GET.get('q')
        search_result = Article.objects.search(q)
    except Article.DoesNotExist:
        search_result = Article.objects.none()
        
    return render(request,'articles/search_view.html',{'articles':search_result}) 