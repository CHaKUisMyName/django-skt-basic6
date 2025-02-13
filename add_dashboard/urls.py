from django.urls import path

from add_dashboard import views

urlpatterns = [
    path('', views.index, name='indexDashboard'),
]
