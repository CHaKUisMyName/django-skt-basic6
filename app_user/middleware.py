from django.http import HttpRequest

from app_user.models.authsession import AuthSession
from app_user.models.user import User


class UserInjectMiddleware:
    def __init__(self, getResponse):
        self.getResponse = getResponse

    def __call__(self, request: HttpRequest):
        session = request.COOKIES.get("session")
        authSession = AuthSession.objects.filter(session_ss = session).first()
        if authSession:
            if not authSession.IsExpire():
                data = authSession.GetSessionData()
                user = User.objects.filter(id_u = data['user_id']).first()
                request.currentUser = user if user else None
            else:
                request.currentUser = None
        else:
            request.currentUser = None
        response = self.getResponse(request)
        return response