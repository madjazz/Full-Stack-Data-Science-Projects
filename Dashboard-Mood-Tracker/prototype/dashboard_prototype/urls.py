from django.contrib import admin
from django.urls import path, include
from home import views

from home.views import LogListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name="home"),
    path('logs/', LogListView.as_view(), name='logs'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
