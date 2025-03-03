from django.db import models

class UserRole(models.Model):
    id_ur = models.IntegerField(primary_key= True)
    id_u_ur = models.IntegerField(null= True, blank= True)
    id_org_ur = models.IntegerField(null= True, blank= True)
    id_pst_ur = models.IntegerField(null= True, blank= True)

    class Meta:
        managed = False
        db_table = 'user_role'