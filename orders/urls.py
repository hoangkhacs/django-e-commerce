from . import views
from django.urls import path


urlpatterns = [
    path('', views.order, name='orders'),
    path('ordered', views.ordered, name='ordered'),
    path('listorder', views.list_order, name='listorder'),
]
