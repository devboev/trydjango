from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from search.views import search_view

urlpatterns = [
    path("", include('articles.urls')),
    path("accounts/",include('accounts.urls')),
    path("recipes/",include('recipes.urls')),
    path("search/",search_view, name='search'),
    path("admin/", admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)