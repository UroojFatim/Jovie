from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),  # Base page (Login)
    path('home/', views.home, name='home'),  # Home page (after login)
    path('quiz/', views.quiz, name='quiz'),  # Quiz page
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard (results and details)
    path('report/<int:report_id>/', views.report, name='report'),  # Report page (view and save report)
    path('reports/', views.saved_reports, name='saved_reports'),  # Saved reports page
    path('reports/', views.saved_reports, name='saved_reports'), 
]
