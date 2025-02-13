import base64
import json
import os
from django.db import models
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from django.utils.timezone import now

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
cipher = Fernet(SECRET_KEY.encode())

class AuthSession(models.Model):
    session_ss = models.CharField(primary_key=True,max_length=255)
    token_ss = models.TextField()
    expireDate_ss = models.DateTimeField()

    def SaveSessionData(self, data):
        """
        เข้ารหัสและบันทึก session_data
        param data: Dictionary ที่ต้องการเก็บใน session -> {"test": ...}
        """
        serialized_data = json.dumps(data) # แปลงเป็น json
        encrypted_data = cipher.encrypt(serialized_data.encode()) # เข้ารหัส
        self.token_ss = base64.urlsafe_b64encode(encrypted_data).decode() # แปลงเป็น base 64 string for save to DB

    def GetSessionData(self):
        """
        ถอดรหัสและดึงข้อมูล session_data
        """
        # {'user_id': authUser.id_u_auth}
        try:
            encryptedData = base64.urlsafe_b64decode(self.token_ss.encode())
            decryptedData = cipher.decrypt(encryptedData).decode()
            
            return json.loads(decryptedData)
        except Exception as ex:
            print(str(ex))
            return {}
        
    def DeleteSessionData(self):
        self.delete()

    def IsExpire(self):
        """
        ตรวจสอบว่า session หมดอายุหรือไม่
        return: True ถ้า session หมดอายุ
        """
        return now() > self.expireDate_ss

    class Meta:
        managed = False
        db_table = 'auth_session'