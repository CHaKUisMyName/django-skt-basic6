from django.urls import path

from app_position import views

urlpatterns = [
    path('', views.index, name='indexPst'),
    path('addpst/', views.addPst, name='addPst'),
    path('editpst/<idpst>', views.editPst, name='editPst'),
    path('deletepst/<idpst>', views.deletePst, name='deletePst'),
]
