from django.urls import path

from app_organization import views

urlpatterns = [
    path('', views.index, name='indexOrg'),
    path('addorg/',views.addOrg, name='addOrg'),
    path('editorg/<idorg>', views.editOrg, name='editOrg'),
    path('deleteorg/<idorg>', views.deleteOrg, name="deleteOrg"),
    path('orgdwn', views.GetOrgDropdown, name='orgdwn'),
]
