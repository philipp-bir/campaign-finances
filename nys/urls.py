from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('counties', views.counties, name='counties'),
    path('municipalities/<int:municipality_id>/<int:year>/', views.json_municipality_year, name='json_municipality_year'),
    path('municipalities/contributions/<int:municipality_id>/<int:year>/', views.municipality_contributions_year, name='municipality_year'),
    path('json/municipalities/contributions/<int:municipality_id>/<int:year>/', views.json_municipality_contributions_year, name='json_municipality_year'),
    path('filers/contributions/<int:filer_id>/<int:year>/',views.filers_contributions_year,name="filers_contributions_year"),
    path('filers/contributions/<int:filer_id>/<int:year>/<str:t_code>',views.filers_contributions_year,name="filers_contributions_year_type"),
    path('json/filers/contributions/<int:filer_id>/<int:year>/',views.json_filers_contributions_year,name="json_filers_contributions_year"),
    path('json/filers/contributions/<int:filer_id>/<int:year>/<str:t_code>',views.json_filers_contributions_year,name="json_filers_contributions_year_type"),
]
