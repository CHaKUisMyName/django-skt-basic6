from django.db import models

# Create your models here.
class Organization(models.Model):
    id_org = models.IntegerField(primary_key= True)
    code_org = models.CharField(max_length= 100, null= True, blank= True)
    nameTH_org = models.CharField(max_length= 100, null= True, blank= True)
    nameEN_org = models.CharField(max_length= 100, null= True, blank= True)
    isActive_org = models.SmallIntegerField(null= True)
    cDate_org = models.DateTimeField(null= True)
    uDate_org = models.DateTimeField(null= True)
    cid_u_org = models.IntegerField(null= True)
    uid_u_org = models.IntegerField(null= True)

    class Meta:
        managed = False
        db_table = 'organization'