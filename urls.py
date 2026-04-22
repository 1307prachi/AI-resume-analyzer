from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_page, name='upload_page'),
    path('result/<int:pk>/', views.result_page, name='result_page'),
    path('download/<int:pk>/', views.download_report, name='download_report'),
    path('history/', views.history_page, name='history_page'),
    path('improve/<int:pk>/', views.improve_resume, name='improve_resume'),
    path('download-improved/<int:pk>/', views.download_improved_resume, name='download_improved'),
]