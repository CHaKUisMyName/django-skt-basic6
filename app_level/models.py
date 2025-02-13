from django.db import models

# Create your models here.
class Level(models.Model):
    id_lv = models.IntegerField(primary_key= True)
    code_lv = models.CharField(max_length= 45, null= True, blank= True)
    nameTH_lv = models.CharField(max_length= 100, null= True, blank= True)
    nameEN_lv = models.CharField(max_length= 100, null= True, blank= True)
    isActive_lv = models.SmallIntegerField(null= True, blank= True)
    cDate_lv = models.DateTimeField(null= True, blank= True)
    uDate_lv = models.DateTimeField(null= True, blank= True)
    cid_u_lv = models.IntegerField(null= True, blank= True)
    uid_u_lv = models.IntegerField(null= True, blank= True)

    class Meta:
        managed = False
        db_table = "level"