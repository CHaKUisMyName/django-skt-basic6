from django.db import models

# Create your models here.
class Position(models.Model):
    id_pst = models.IntegerField(primary_key= True)
    code_pst = models.CharField(max_length= 100, null= True, blank= True)
    nameTH_pst = models.CharField(max_length= 100, null= True, blank= True)
    nameEN_pst = models.CharField(max_length= 100, null= True, blank= True)
    isActive_pst = models.SmallIntegerField(null= True)
    cDate_pst = models.DateTimeField(null= True)
    uDate_pst = models.DateTimeField(null= True)
    cid_u_pst = models.IntegerField(null= True)
    uid_u_pst = models.IntegerField(null= True)

    class Meta:
        managed = False
        db_table = 'position'