from django.urls import path
from user import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index.html', views.showAll),
    path('add.html', views.adduser),
    path('find', views.finduser),
    path('update', views.update),
    path('', views.showAll, name='index'),
]