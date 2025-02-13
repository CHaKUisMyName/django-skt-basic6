from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.utils.timezone import now

from app_organization.models import Organization
from app_user.models.user import User
from app_user.utils import requiredLogin

# Create your views here.
@requiredLogin
def index(request: HttpRequest):
    orgList = Organization.objects.filter(isActive_org = 1)
    orgs = []
    if orgList.count() > 0:
        orgs = orgList

    context = {
        "orgs": orgs
    }
    return render(request, 'organization/index.html', context)

@requiredLogin
def addOrg(request: HttpRequest):
    if request.method == "POST":
        response = HttpResponseRedirect(reverse('indexOrg'))
        try:
            currentUser: User = request.currentUser
            org = Organization()
            org.code_org = request.POST.get('code')
            org.nameEN_org = request.POST.get('nameen')
            org.nameTH_org = request.POST.get('nameth')
            org.isActive_org = 1
            org.cid_u_org = currentUser.id_u
            org.cDate_org = now()
            org.save()
            messages.success(request, "Save Success")
        except Exception as ex:
            messages.error(request, str(ex))

        return response
    return render(request, 'organization/addorg.html')

@requiredLogin
def editOrg(request: HttpRequest, idorg):
    org = Organization.objects.filter(id_org = idorg).first()

    if org is None:
        messages.error(request, "Not Found Organization.")
        return HttpResponseRedirect(reverse('indexOrg'))
    
    if request.method == "POST":
        try:
            currentUser: User = request.currentUser
            org.code_org = request.POST.get('code')
            org.nameEN_org = request.POST.get('nameen')
            org.nameTH_org = request.POST.get('nameth')
            org.uDate_org = now()
            org.uid_u_org = currentUser.id_u
            org.save()
            messages.success(request, 'Edit Sucess')
        except Exception as ex:
            messages.error(request, str(ex))
        return HttpResponseRedirect(reverse('indexOrg'))
    
    context = {
        "org": org
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