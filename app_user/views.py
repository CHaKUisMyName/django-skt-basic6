from datetime import datetime, timedelta
import hashlib
import json
import os
import pprint
import secrets
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.utils.timezone import now
from django.core import serializers
from app_organization.models import Organization
from app_position.models import Position
from app_user.models.authsession import AuthSession
from app_user.models.authuser import AuthUser, VerifyPAssword
from app_user.models.user import GetNextIdUser, User
from app_user.models.userrole import UserRole
from app_user.utils import requiredLogin

# Create your views here.
@requiredLogin
def index(request: HttpRequest):
    usersList = User.objects.filter(isActive_u = 1)
    users = []
    if usersList.count() > 0:
        authUsers = AuthUser.objects.filter(isActive_auth = 1)
        for user in usersList:
            hasAccount = False
            if authUsers.count() > 0:
                hasAccount = any(authUser.id_u_auth == user.id_u for authUser in authUsers)

            uRoleList = UserRole.objects.filter(id_u_ur = user.id_u)
            uRoles = []
            if uRoleList.count():
                for uRole in uRoleList:
                    org = Organization.objects.filter(id_org = uRole.id_org_ur).first()
                    pst = Position.objects.filter(id_pst = uRole.id_pst_ur).first()
                    if org and pst:
                        uRoles.append({
                            "org": org.nameEN_org,
                            "pst": pst.nameEN_pst,
                        })


            users.append({
                "id_u": user.id_u,
                "fullName": user.fNameEN_u + " " + user.lNameEN_u,
                "code": user.code_u,
                "email": user.email_u,
                "hasAccount": hasAccount,
                "roles": uRoles,
            })

    context = {
        'users': users
    }
    return render(request, 'user/index.html', context)

@requiredLogin
def AddUser(request: HttpRequest):
    if request.method == "POST":
        response = HttpResponseRedirect(reverse('indexUser'))
        # get list data เช่น checkbox multiple
        # print(request.POST.getlist('pst'))
        try:
            currentUser: User = request.currentUser

            dupUser = User.objects.filter(code_u = request.POST.get('code')).first()
            if dupUser:
                messages.error(request, 'Duplicate User code')
                return response
            # format from input
            formatStr = "%d/%m/%Y"
            
            user = User()
            user.code_u = request.POST.get('code')
            user.fNameEN_u = request.POST.get('fnameen')
            user.lNameEN_u = request.POST.get('lnameen')
            if request.POST.get('fnameth'):
                user.fNameTH_u = request.POST.get('fnameth')
            if request.POST.get('lnameth'):
                user.lNameTH_u = request.POST.get('lnameth')
            if request.POST.get('nickname'):
                user.nickName_u = request.POST.get('nickname')
            if request.POST.get('nation'):
                user.nation_u = request.POST.get('nation')
            if request.POST.get('email'):
                user.email_u = request.POST.get('email')
            if request.POST.get('phone'):
                user.phone_u = request.POST.get('phone')
            user.isAdmin_u = 1 if request.POST.get('isadmin') is not None else 0
            user.isActive_u = 1
            user.cById_u = currentUser.id_u
            user.cDate_u = now()
            print(request.POST.get('birthday'))
            if request.POST.get('birthday'):
                user.birthDay_u = datetime.strptime(str(request.POST.get('birthday')),formatStr).date()
            # else:
            #     user.birthDay_u = ""

            user.save(force_insert=True)
            userID = GetNextIdUser()
            print(userID)

            pstList = request.POST.getlist('pst')
            orgList = request.POST.getlist('org')
            if len(pstList) != len(orgList):
                messages.error(request, "Role data is worng")
                return response
            roleData = [{"pst": pst, "org": org} for pst, org in zip(pstList, orgList)]
            
            for role in roleData:
                userRole = UserRole()
                userRole.id_pst_ur = role['pst']
                userRole.id_org_ur = role['org']
                userRole.id_u_ur = userID
                userRole.save()
                
            messages.success(request, "Save Success")
            return response
        except Exception as ex:
            print(str(ex))
            messages.error(request, str(ex))
            return response
    else:
        return render(request, 'user/adduser.html')

@requiredLogin
def EditUser(request:HttpRequest, iduser):
    response = HttpResponseRedirect(reverse('indexUser'))
    
    if request.method == "POST":
        try:
            uid = request.POST.get('uid')
            if not uid:
                messages.error(request, "Not Found User id.")
                return response
            user = User.objects.filter(id_u = uid).first()
            if user == None:
                messages.error(request, "Not Found User.")
                return response
            
            currentUser: User = request.currentUser
            # format from input
            formatStr = "%d/%m/%Y"
            
            user.code_u = request.POST.get('code')
            user.fNameEN_u = request.POST.get('fnameen')
            user.lNameEN_u = request.POST.get('lnameen')
            if request.POST.get('fnameth'):
                user.fNameTH_u = request.POST.get('fnameth')
            if request.POST.get('lnameth'):
                user.lNameTH_u = request.POST.get('lnameth')
            if request.POST.get('nickname'):
                user.nickName_u = request.POST.get('nickname')
            if request.POST.get('nation'):
                user.nation_u = request.POST.get('nation')
            if request.POST.get('email'):
                user.email_u = request.POST.get('email')
            if request.POST.get('phone'):
                user.phone_u = request.POST.get('phone')
            user.isAdmin_u = 1 if request.POST.get('isadmin') is not None else 0
            user.isActive_u = 1
            user.uById_u = currentUser.id_u
            # user.uDate_u = now()
            if request.POST.get('birthday'):
                user.birthDay_u = datetime.strptime(str(request.POST.get('birthday')),formatStr).date()
            
            user.save(force_update=True)

            uRole = UserRole.objects.filter(id_u_ur = uid)
            if uRole.count() > 0:
                uRole.delete()

            pstList = request.POST.getlist('pst')
            orgList = request.POST.getlist('org')
            if len(pstList) != len(orgList):
                messages.error(request, "Role data is worng")
                return response
            roleData = [{"pst": pst, "org": org} for pst, org in zip(pstList, orgList)]
            for role in roleData:
                userRole = UserRole()
                userRole.id_pst_ur = role['pst']
                userRole.id_org_ur = role['org']
                userRole.id_u_ur = uid
                userRole.save()
            
            messages.success(request, 'Success')
        except Exception as ex:
            messages.error(request, str(ex))
        return response
    else:
        user = User.objects.filter(id_u = iduser).first()
        if user is None:
            messages.error(request, 'Not Found User.')
            return response
        
        context = {
            'user': user
            }
        return render(request, 'user/edituser.html', context)

@requiredLogin
def Delete(request: HttpRequest, iduser):
    try:
        currentUser: User = request.currentUser
        user = User.objects.filter(id_u = iduser).first()
        if user is None:
            data = {
                "deleted": False,
                "mss": "not found user"
            }
            return JsonResponse(data)
        
        user.isActive_u = 0
        user.uDate_u = now()
        user.uById_u = currentUser.id_u
        user.save()
        
        authUser = AuthUser.objects.filter(id_u_auth = user.id_u).first()
        if authUser:
            authUser.isActive_auth = 0
            authUser.save()

        rData = {
            "deleted": True,
            "mss": "delete success"
        }
        return JsonResponse(rData)
    except Exception as ex:
        data = {
            "deleted": False,
            "mss": str(ex)
        }
        return JsonResponse(data)

def login(request: HttpRequest):
    if request.method == "POST":
        uname = request.POST.get('uname')
        password = request.POST.get('password')

        authUser = AuthUser.objects.filter(user_auth = uname).first()
        if authUser is None:
            # messages.error(request, "Not Found User!")
            return HttpResponseRedirect("/login")
        
        if VerifyPAssword(password,authUser.pass_auth) == False:
            # messages.error(request, "wrong Password")
            return HttpResponseRedirect("/login")
        
        try:
            session = AuthSession()
            session.session_ss = secrets.token_hex(20)
            session.expireDate_ss = now() + timedelta(days=1)
            session.SaveSessionData({'user_id': authUser.id_u_auth})
            session.save()

            # update time stamp login
            authUser.lastLogin_auth = now()
            authUser.save()
        except Exception as ex:
            # messages.error(request, str(ex))
            return HttpResponseRedirect("/login")
        

        response = HttpResponseRedirect("/")
        response.set_cookie('session',session.session_ss,expires=session.expireDate_ss)
        return response
    else:
        return render(request, 'user/login.html')

@requiredLogin
def logout(request: HttpRequest):
    session = request.COOKIES.get("session")
    authSession = AuthSession.objects.filter(session_ss=session).first()
    if authSession:
        authSession.delete()
    response = HttpResponseRedirect('/login')
    response.delete_cookie('session')
    return response

@requiredLogin
def regisUser(request: HttpRequest, iduser):
    user = User.objects.filter(id_u = iduser).first()
    if user is None:
        messages.error(request, "Not Found User!")
        return HttpResponseRedirect(reverse('indexUser'))
    
    if request.method == "POST":
        try:
            authUser = AuthUser()
            authUser.user_auth = request.POST.get('uname')
            authUser.HashPassword(request.POST.get('password'))
            authUser.id_u_auth = user.id_u
            authUser.isActive_auth = 1
            authUser.cDate_auth = now()
            authUser.save()

            messages.success(request, "Register Success")
        except Exception as ex:
            messages.error(request, str(ex))
        return HttpResponseRedirect(reverse('indexUser'))

    return render(request, 'user/regis.html')

@requiredLogin
def Changepassword(request: HttpRequest, iduser):
    if request.method == "POST":
        idAuth = request.POST.get('authid')
        if not idAuth:
            messages.error(request, "Not Found Auth User accout!")
            return HttpResponseRedirect(reverse('indexUser'))
        authUser = AuthUser.objects.filter(id_auth = idAuth).first()
        if authUser is None:
            messages.error(request, "Not Found Auth User Data!")
            return HttpResponseRedirect(reverse('indexUser'))
        passData = request.POST.get('password')
        if not passData:
            messages.error(request, "Not Found Password!")
            return HttpResponseRedirect(reverse('indexUser'))
        
        try:
            authUser.HashPassword(str(passData))
            authUser.save()
            authSesstion = AuthSession.objects.all()
            if authSesstion:
                for authSS in authSesstion:
                    data = authSS.GetSessionData()
                    if data['user_id'] == authUser.id_u_auth:
                        authSS.delete()
            messages.success(request, "Change Password Success")
            return HttpResponseRedirect(reverse('indexUser'))
        except Exception as ex:
            messages.error(request, str(ex))
            return HttpResponseRedirect(reverse('indexUser'))
    else:
        user = User.objects.filter(id_u = iduser).first()
        if user is None:
            messages.error(request, "Not Found User!")
            return HttpResponseRedirect(reverse('indexUser'))
        authUser = AuthUser.objects.filter(id_u_auth = user.id_u).first()
        if authUser is None:
            messages.error(request, "Not Found Auth User Data!")
            return HttpResponseRedirect(reverse('indexUser'))
        context = {
            "authUser": authUser
        }
        return render(request, 'user/changepassword.html', context)

def AddSuperUser(request: HttpRequest):
    if request.method == "POST":
        try:
            user = User()
            user.code_u = '000'
            user.fNameEN_u = 'super'
            user.lNameEN_u = 'user'
            user.isAdmin_u = 1
            user.isActive_u = 1
            user.save()
            userID = GetNextIdUser()

            authUser = AuthUser()
            authUser.user_auth = request.POST.get('uname')
            authUser.HashPassword(request.POST.get('pass'))
            authUser.id_u_auth = userID
            authUser.isActive_auth = 1
            authUser.save()

            return JsonResponse({"success": True})
        except Exception as ex:
            return JsonResponse({'success': False, 'mss': repr(ex)})
    return render(request, 'user/addsuperuser.html')

@requiredLogin
def GetUserRole(request: HttpRequest, iduser):
    userRoles = []
    uRoleList = UserRole.objects.filter(id_u_ur = iduser)
    if uRoleList.count() > 0:
        uRJson = json.loads(serializers.serialize('json', uRoleList))
        # ต้องดึงค่า "pk" แล้วเพิ่มเข้าไปใน "fields" pk คือ id_ur
        userRoles = [{"id_ur": obj["pk"], **obj["fields"]} for obj in uRJson]
        print(userRoles)

    return JsonResponse(userRoles, safe=False)