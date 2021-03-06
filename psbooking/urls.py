"""psbooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('main.urls')),
    path('hotels/', include('hotels.urls')),
    path('accounts/', include('accounts.urls')),
    path('allauth/accounts/', include('allauth.urls')),
    # для проверки!
    path('error404/', views.error_404, name='error404'),
    path('error500/', views.error_404, name='error500'),
]

handler404 = "psbooking.views.page_not_found_view"
handler500 = "psbooking.views.server_error_view"


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]