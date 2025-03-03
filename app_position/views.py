import json
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.utils.timezone import now
from django.core import serializers

from app_position.models import Position
from app_user.models.user import User
from app_user.utils import requiredLogin

# Create your views here.
@requiredLogin
def index(request: HttpRequest):
    positionList = Position.objects.filter(isActive_pst =  1).order_by('code_pst')
    psts = []
    if positionList.count() > 0:
        psts = positionList

    context = {
        "psts": psts
    }
    return render(request, 'position/index.html', context)

@requiredLogin
def addPst(request: HttpRequest):
    if request.method == "POST":
        response = HttpResponseRedirect(reverse('indexPst'))
        try:
            dupPst = Position.objects.filter(code_pst = request.POST.get('code')).first()
            if dupPst:
                messages.error(request, "Duplicate Position Code.")
                return response
            currentUser: User = request.currentUser
            pst = Position()
            pst.code_pst = request.POST.get('code')
            pst.nameTH_pst = request.POST.get('nameth')
            pst.nameEN_pst = request.POST.get('nameen')
            pst.isActive_pst = 1
            pst.cid_u_pst = currentUser.id_u
            pst.cDate_pst = now()
            pst.save()
            messages.success(request, "Save Success")
        except Exception as ex:
            messages.error(request, str(ex))
        return response
    return render(request, 'position/addpst.html')

@requiredLogin
def editPst(request: HttpRequest, idpst):
    if request.method == "POST":
        response = HttpResponseRedirect(reverse('indexPst'))
        try:
            pstId = request.POST.get('pstid')
            if not pstId:
                messages.error(request, "Not found position id.")
                return response
            
            pst = Position.objects.filter(id_pst = pstId).first()
            if pst is None:
                messages.error(request, "Not found position.")
                return response
            
            currentUser: User = request.currentUser
            pst.code_pst = request.POST.get('code')
            pst.nameTH_pst = request.POST.get('nameth')
            pst.nameEN_pst = request.POST.get('nameen')
            pst.uDate_pst = now()
            pst.uid_u_pst = currentUser.id_u
            pst.save()
            messages.success(request, "Edit Success")
        except Exception as ex:
            messages.error(request, str(ex))

        return response
    else:
        pst = Position.objects.filter(id_pst = idpst).first()
        if pst is None:
            messages.error(request, "Not found position")
            return HttpResponseRedirect(reverse('indexPst'))
        context = {
            "pst": pst
        }
        return render(request, 'position/editpst.html', context)
    

@requiredLogin
def deletePst(request: HttpRequest, idpst):
    pst = Position.objects.filter(id_pst = idpst).first()
    if pst is None:
        data = {
            "deleted": False,
            "mss": "not found Position"
        }
        return JsonResponse(data)
    try:
        currentUser: User = request.currentUser
        pst.isActive_pst = 0
        pst.uDate_pst = now()
        pst.uid_u_pst = currentUser.id_u
        pst.save()
        data = {
            "deleted": True,
            "mss": "delete success"
        }
        return JsonResponse(data)
    except Exception as ex:
        data = {
            "deleted": False,
            "mss": str(ex)
        }
        return JsonResponse(data)
    
@requiredLogin
def GetPositionDropdown(request: HttpRequest):
    pstList = Position.objects.filter(isActive_pst = 1)
    psts = []
    if pstList.count() > 0:
        psts_json = json.loads(serializers.serialize('json', pstList))
        firstPst = {
            'id_pst': "",
            'code_pst': '-',
            'nameEN_pst': 'select position'
        }
        # ดึงค่าเฉพาะ "fields" ออกจากแต่ละ object ใน psts_json
        # serializers.serialize('json', pstList) แยก id_pst ออกไปไว้ที่ key "pk" แทนที่จะอยู่ใน "fields" ดังนั้น obj['fields'] จะไม่มี id_pst
        # ต้องดึงค่า "pk" แล้วเพิ่มเข้าไปใน "fields" เพื่อให้ id_pst ติดมาด้วย
        psts = [firstPst] + [{"id_pst": obj["pk"], **obj["fields"]} for obj in psts_json]
    return JsonResponse(psts, safe= False)