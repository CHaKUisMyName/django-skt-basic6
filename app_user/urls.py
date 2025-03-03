from django.urls import path

from app_user import views


urlpatterns = [
    path('', views.index, name='indexUser'),
    path('adduser/', views.AddUser, name='addUser'),
    path('edituser/<iduser>', views.EditUser, name='editUser'),
    path('deleteuser/<iduser>', views.Delete, name='deleteUser'),
    path('super', views.AddSuperUser, name='addSuperUser'),
    path('regisuser/<iduser>', views.regisUser, name='regisUser'),
    path('repass/<iduser>', views.Changepassword, name='repassUser'),
    path('userrole/<iduser>', views.GetUserRole, name='getUserRole'),
]
