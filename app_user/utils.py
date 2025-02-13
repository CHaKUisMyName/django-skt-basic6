from django.http import HttpRequest, HttpResponseRedirect
from django.contrib import messages
from django.utils.timezone import now

from app_user.models.authsession import AuthSession


def requiredLogin(view_func):
    def wrapper(request: HttpRequest, *args,**kwargs):
        # try:
        clientSession = request.COOKIES.get("session")

        # ลบข้อมูล session ที่เกินเวลาทั้งหมดแแกจาก DB
        expireSeession = AuthSession.objects.filter(expireDate_ss__lt = now())
        if expireSeession.exists():
            expireSeession.delete()

        # หา session
        session = AuthSession.objects.filter(session_ss = clientSession).first()
        if session is None:
            response = HttpResponseRedirect('/login')
            return response
            
        # ถ้า sesion expire
        if session.IsExpire():
            session.DeleteSessionData()
            response = HttpResponseRedirect('/login')
            response.delete_cookie('session')
            return response
            
        return view_func(request, *args, **kwargs)
        
        # except Exception as ex:
        #     print(str(ex))
            
        #     response = HttpResponseRedirect('/login')
        #     return response
        
    return wrapper