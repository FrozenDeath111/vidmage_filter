from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('image_process', views.image_process, name='image_process'),
    path('view', views.show_file, name='view'),
    path('video_process', views.video_process, name='video_process'),
    path('change_background', views.change_background, name='change_bg')
]