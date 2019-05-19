from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('counties', views.counties, name='counties'),
    path('municipalities/<int:municipality_id>/<int:year>/', views.json_municipality_year, name='json_municipality_year'),
    path('municipalities/contributions/<int:municipality_id>/<int:year>/', views.municipality_contributions_year, name='municipality_year'),
    path('json/municipalities/contributions/<int:municipality_id>/<int:year>/', views.json_municipality_contributions_year, name='json_municipality_year'),
]
