import logging
from django.db import models
from passlib.context import CryptContext

# https://github.com/pyca/bcrypt/issues/684
#AttributeError: module 'bcrypt' has no attribute '__about__' with new 4.1.1 version #684
logging.getLogger('passlib').setLevel(logging.ERROR)

# สร้าง CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def VerifyPAssword(password: str, hashPassword: str):
    return pwd_context.verify(password, hashPassword)

class AuthUser(models.Model):
    id_auth = models.IntegerField(primary_key= True)
    user_auth = models.CharField(max_length= 255, null= True, blank= True)
    pass_auth = models.CharField(max_length= 255, null= True, blank= True)
    lastLogin_auth = models.DateField(null= True)
    id_u_auth = models.IntegerField(null= True)
    isActive_auth = models.SmallIntegerField(null= True)
    cDate_auth = models.DateTimeField(null= True)

    def HashPassword(self, password: str):
        self.pass_auth = pwd_context.hash(password)

    class Meta:
        managed = False
        db_table = 'auth_user'