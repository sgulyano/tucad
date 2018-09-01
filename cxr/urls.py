from django.urls import path

from . import views

app_name = 'cxr'
urlpatterns = [
    path('', views.Upload.as_view(), name='upload'),
    path('<int:pk>/analysis', views.Analysis.as_view(), name='analysis'),
    path('systemview', views.SystemView.as_view(), name='systemview'),
    path('clear', views.clear_database, name='clear_database'),
]
