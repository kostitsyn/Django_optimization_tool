"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
import mainapp.views as mainapp

urlpatterns = [
    # path('', mainapp.main, name='main'),
    path('', mainapp.MainListView.as_view(), name='main'),

    # path('about/', mainapp.about, name='about'),
    path('about/', mainapp.AboutTemplateView.as_view(), name='about'),

    # path('service/', mainapp.service, name='service'),
    path('service/', mainapp.ServiceTemplateView.as_view(), name='service'),

    path('gallery/', include('mainapp.urls', namespace='gallery')),

    # path('news/', mainapp.news, name='news'),
    path('news/', mainapp.NewsTemplateView.as_view(), name='news'),

    # path('team/', mainapp.team, name='team'),
    path('team/', mainapp.TeamTemplateView.as_view(), name='team'),

    # path('contacts/', mainapp.contacts, name='contacts'),
    path('contacts/', mainapp.ContactsListView.as_view(), name='contacts'),

    path('basket/', include('basketapp.urls', namespace='basket')),
    path('auth/', include('authapp.urls', namespace='auth')),

    path('', include('social_django.urls', namespace='social')),

    path('order/', include('ordersapp.urls', namespace='order')),

    path('admin/', include('adminapp.urls', namespace='admin')),
    # path('admin/', admin.site.urls),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
