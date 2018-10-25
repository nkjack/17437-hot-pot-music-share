"""music_share_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

import hot_spot_music_share.views


urlpatterns = [
    path('admin/', admin.site.urls),
]

#
# urlpatterns = [
#     path('hot_spot_music_share/', include('hot_spot_music_share.urls')),
#     path('', hot_spot_music_share.views.global_stream)
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)