from django.urls import path

from app_level import views

urlpatterns = [
    path('', views.index, name='indexLv'),
    path('addlv/', views.addLevel, name='addLv'),
    path('editlv/<idlv>', views.editLv, name='editLv'),
    path('deletelv/<idlv>', views.deleteLv, name='deleteLv'),
]
