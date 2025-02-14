from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import now
from django.contrib import messages

from app_level.models import Level
from app_user.models.user import User
from app_user.utils import requiredLogin

# Create your views here.
@requiredLogin
def index(request: HttpRequest):
    lvList = Level.objects.filter(isActive_lv = 1)
    lvs = []
    if lvList.count() > 0:
        lvs = lvList

    context = {
        'lvs': lvs
    }
    return render(request, 'level/index.html',context)

@requiredLogin
def addLevel(request: HttpRequest):
    if request.method == "POST":
        response = HttpResponseRedirect(reverse('indexLv'))
        try:
            currentUser: User = request.currentUser
            lv = Level()
            lv.code_lv = request.POST.get('code')
            lv.nameEN_lv = request.POST.get('nameen')
            lv.nameTH_lv = request.POST.get('nameth')
            lv.isActive_lv = 1
            lv.cDate_lv = now()
            lv.cid_u_lv = currentUser.id_u
            lv.save()
            # print(lv.__dict__)
            messages.success(request, 'Save Success')
        except Exception as ex:
            messages.error(request, str(ex))

        return response
    
    return render(request, 'level/addlv.html')

@requiredLogin
def editLv(request: HttpRequest, idlv):
    
    
    if request.method == "POST":
        try:
            lvid = request.POST.get('lvid')
            if not lvid:
                messages.error(request, 'Not found Level id')
                return HttpResponseRedirect(reverse('indexLv'))
            lv = Level.objects.filter(id_lv = lvid).first()
            if lv == None:
                messages.error(request, 'Not found Level')
                return HttpResponseRedirect(reverse('indexLv'))

            currentUser: User = request.currentUser
            lv.code_lv =  request.POST.get('code')
            lv.nameEN_lv = request.POST.get('nameen')
            lv.nameTH_lv = request.POST.get('nameth')
            lv.uDate_lv = now()
            lv.uid_u_lv = currentUser.id_u
            lv.save()
            messages.success(request, 'Edit Success')
        except Exception as ex:
            messages.error(request, str(ex))
        return HttpResponseRedirect(reverse('indexLv'))
    else:
        lv = Level.objects.filter(id_lv = idlv).first()
        if lv is None:
            messages.error(request, "Not Found Level.")
            return HttpResponseRedirect(reverse('indexLv'))
        context = {
            "lv": lv
            }
        return render(request, 'level/editlv.html',context)

@requiredLogin
def deleteLv(request: HttpRequest, idlv):
    lv = Level.objects.filter(id_lv = idlv).first()
    if lv is None:
        data = {
            'deleted': False,
            'mss': "not found level"
        }
        return JsonResponse(data)
    try:
        currentUser: User = request.currentUser
        lv.isActive_lv = 0
        lv.uDate_lv = now()
        lv.uid_u_lv = currentUser.id_u
        lv.save()
        data = {
            'deleted': True,
            'mss': "delete success"
        }
        return JsonResponse(data)
    except Exception as ex:
        data = {
            'deleted': False,
            'mss': str(ex)
        }
        return JsonResponse(data)