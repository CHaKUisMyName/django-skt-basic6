"""
URL configuration for skt_center project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from app_user import views as userViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('add_dashboard.urls')),
    path('user/',include('app_user.urls')),
    path('login/', userViews.login, name='login'),
    path('logout', userViews.logout, name='logout'),
    path('org/', include('app_organization.urls')),
    path('lv/', include('app_level.urls')),
    path('pst/', include('app_position.urls')),
]
