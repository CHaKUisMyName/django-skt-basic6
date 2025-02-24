from django.db import models

class User(models.Model):
    id_u = models.IntegerField(primary_key= True)
    code_u = models.CharField(max_length= 45, null= True, blank= True)
    fNameTH_u = models.CharField(max_length= 45, null= True, blank= True)
    lNameTH_u = models.CharField(max_length= 45, null= True, blank= True)
    fNameEN_u = models.CharField(max_length= 45, null= True, blank= True)
    lNameEN_u = models.CharField(max_length= 45, null= True, blank= True)
    nickName_u = models.CharField(max_length= 45, null= True, blank= True, default= "")
    nation_u = models.CharField(max_length= 45, null= True, blank= True, default= "")
    email_u = models.CharField(max_length= 45, null= True, blank= True, default= "")
    phone_u = models.CharField(max_length= 45, null= True, blank= True, default= "")
    birthDay_u = models.DateField(null= True, blank= True)
    isAdmin_u = models.SmallIntegerField(null= True)
    isActive_u = models.SmallIntegerField(null= True)
    cDate_u = models.DateTimeField(null= True)
    uDate_u = models.DateTimeField(null= True)
    cById_u = models.IntegerField(null= True)
    uById_u = models.IntegerField(null= True)

    class Meta:
        managed = False
        db_table = 'user'