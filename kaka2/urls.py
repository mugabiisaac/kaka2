"""kaka2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login




urlpatterns = [
    # url(r'^$', 'home.views.index'),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include("posts.urls", namespace='posts')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^login/', TemplateView.as_view(template_name="registration/login.html")),


    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^success/', TemplateView.as_view(template_name="buy.html")),
    url('^accounts/', include('django.contrib.auth.urls'))

    #url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='login')
    #url(r'^accounts/',include('registration.backends.hmac.urls')),
    #url(r'^login/', TemplateView.as_view(template_name="login.html")),
    #url(r'^posts/', TemplateView.as_view(template_name="posts.html"))

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
