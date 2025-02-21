from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.utils.timezone import now

from app_level.models import Level
from app_organization.models import Organization
from app_user.models.user import User
from app_user.utils import requiredLogin

# Create your views here.
@requiredLogin
def index(request: HttpRequest):
    orgList = Organization.objects.filter(isActive_org = 1)
    orgs = []
    if orgList.count() > 0:
        lvs = Level.objects.filter(isActive_lv = 1)
        lvName = ""
        if lvs is None:
            lvName = "-"
        # ทำ list class object ให้เป็น dict {".":".",...} จะได้ไม่ต้อง Loop อีกครั้ง
        lvDict = {lvl.id_lv:lvl.nameEN_lv for lvl in lvs} 
        for org in orgList:
            lvName = lvDict.get(org.id_lv_org, "-")
            orgs.append({
                "id_org":org.id_org,
                "code":org.code_org,
                "name": org.nameEN_org,
                "level": lvName
            })
        
        orgs.sort(key=lambda x: x["code"])
    context = {
        "orgs": orgs,
    }
    return render(request, 'organization/index.html', context)

@requiredLogin
def addOrg(request: HttpRequest):
    if request.method == "POST":
        response = HttpResponseRedirect(reverse('indexOrg'))
        try:
            dupOrg = Organization.objects.filter(code_org = request.POST.get('code')).first()
            if dupOrg:
                messages.error(request, 'Duplicate Org Code')
                return response
            currentUser: User = request.currentUser
            org = Organization()
            org.code_org = request.POST.get('code')
            org.nameEN_org = request.POST.get('nameen')
            org.nameTH_org = request.POST.get('nameth')
            org.id_lv_org = request.POST.get('level')
            org.isActive_org = 1
            org.cid_u_org = currentUser.id_u
            org.cDate_org = now()
            org.save()
            messages.success(request, "Save Success")
        except Exception as ex:
            messages.error(request, str(ex))

        return response
    else:
        levelList = Level.objects.filter(isActive_lv = 1)
        lvFirstChoice = Level()
        lvFirstChoice.id_lv = 0
        lvFirstChoice.nameEN_lv = "Select Level"
        lvs = []
        if levelList.count() > 0:
            lvs.append(lvFirstChoice)
            for lv in levelList:
                lvs.append(lv)

        context = {
            "lvs": lvs,
        }
        return render(request, 'organization/addorg.html', context)

@requiredLogin
def editOrg(request: HttpRequest, idorg):
    if request.method == "POST":
        try:
            orgid = request.POST.get('orgid')
            if not orgid:
                messages.error(request, "Not Found Organization id.")
                return HttpResponseRedirect(reverse('indexOrg'))
            org = Organization.objects.filter(id_org = orgid).first()
            if org is None:
                messages.error(request, "Not Found Organization.")
                return HttpResponseRedirect(reverse('indexOrg'))

            currentUser: User = request.currentUser
            org.code_org = request.POST.get('code')
            org.nameEN_org = request.POST.get('nameen')
            org.nameTH_org = request.POST.get('nameth')
            org.id_lv_org = request.POST.get('level')
            org.uDate_org = now()
            org.uid_u_org = currentUser.id_u
            org.save()
            messages.success(request, 'Edit Sucess')
        except Exception as ex:
            messages.error(request, str(ex))
        return HttpResponseRedirect(reverse('indexOrg'))
    else:
        org = Organization.objects.filter(id_org = idorg).first()
        if org is None:
            messages.error(request, "Not Found Organization.")
            return HttpResponseRedirect(reverse('indexOrg'))
        
        levelList = Level.objects.filter(isActive_lv = 1)
        lvFirstChoice = Level()
        lvFirstChoice.id_lv = 0
        lvFirstChoice.nameEN_lv = "Select Level"
        lvs = []
        if levelList.count() > 0:
            lvs.append(lvFirstChoice)
            for lv in levelList:
                lvs.append(lv)
        
        context = {
            "org": org,
            "lvs":lvs
            }
        return render(request, 'organization/editorg.html', context)

@requiredLogin
def deleteOrg(request: HttpRequest, idorg):
    org = Organization.objects.filter(id_org = idorg).first()
    if org is None:
        data = {
            "deleted": False,
            "mss": "not found organization"
        }
        return JsonResponse(data)
    try:
        currentUser: User = request.currentUser
        org.isActive_org = 0
        org.uDate_org = now()
        org.uid_u_org = currentUser.id_u
        org.save()
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