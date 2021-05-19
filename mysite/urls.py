from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mysite.core import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('drawboxes/',views.drawboxes, name= 'drawboxes'),
    path('makeBoundingBoxesVideo/', views.makeBoundingBoxesVideo, name='makeBoundingBoxesVideo'),
    path('drawPosturePoints/', views.drawPosturePoints, name='drawPosturePoints'),
    path('makePostureVideo/', views.makePostureVideo, name='makePostureVideo'),
    path('makeMergedVideo/', views.makeMergedVideo, name='makeMergedVideo'),
    path('displaySegmentation/', views.displaySegmentation, name='displaySegmentation'),
    path('exportBoundingBoxes/', views.exportBoundingBoxes, name='exportBoundingBoxes'),
    path('exportPosturePoints/', views.exportPosturePoints, name='exportPosturePoints'),
    path('exportSegmentation', views.exportSegmentation, name='exportSegmentation'),
    path('makeBehaviorAnnotationsVideo', views.makeBehaviorAnnotationsVideo, name='makeBehaviorAnnotationsVideo'),
    path('upload/', views.upload, name='upload'),
    path('getListOfVideos', views.getListOfVideos, name='getListOfVideos'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
