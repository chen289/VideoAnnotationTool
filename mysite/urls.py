from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mysite.core import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('drawboxes/',views.drawboxes, name= 'drawboxes'),
    path('downloadVideo/', views.downloadVideo, name='downloadVideo'),
    path('drawPosturePoints/', views.drawPosturePoints, name='drawPosturePoints'),
    path('downloadPostureVideo/', views.downloadPostureVideo, name='downloadPostureVideo'),
    path('downloadMergedVideo/', views.downloadMergedVideo, name='downloadMergedVideo'),
    path('displaySegmentation/', views.displaySegmentation, name='displaySegmentation'),
    path('exportBoundingBoxes/', views.exportBoundingBoxes, name='exportBoundingBoxes'),
    path('exportPosturePoints/', views.exportPosturePoints, name='exportPosturePoints'),
    path('exportSegmentation', views.exportSegmentation, name='exportSegmentation'),
    path('upload/', views.upload, name='upload'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
