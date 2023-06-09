from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('all/', views.all),
    path('all/export/', views.export),
    path('all/?start=<str:from>&end=<str:end>&order_by=<str:order>&min_temp=<int:min_temp>&max_temp=<int:max_temp>&min_press=<int:min_press>&max_press=<int:max_press>', views.all),
    path('all/export/?start=<str:from>&end=<str:end>&order_by=<str:order>&min_temp=<int:min_temp>&max_temp=<int:max_temp>&min_press=<int:min_press>&max_press=<int:max_press>', views.export),
    path('about/', views.about),
    path('graphs/', views.graphs),
    path('graphs/?start=<str:from>&end=<str:end>&type=<str:type>', views.graphs),
    path('graphs?from=<str:from>', views.graphs),
]