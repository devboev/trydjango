from django.urls import path
from .views import (index,
                    article_detail_view, 
                    article_search_view,
                    article_create_view
                )
app_name='articles'
urlpatterns = [
    path("", index, name="home"),
    path("articles/", article_search_view, name="search"),
    path("articles/create/", article_create_view, name="create"),
    path("articles/<slug:slug>/", article_detail_view, name="detail"),
    
]