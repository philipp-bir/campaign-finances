import json

from django.shortcuts import render
from django.http import HttpResponse

from .models import Municipality, Filer, Report


# Create your views here.




def index(request):
    return HttpResponse("Hello, world. You're at the index.")

def counties(request):
    return HttpResponse("")

#def municipality

#def filer(request,filer_id):


def json_municipality_year(request,municipality_id,year):
    filers=Filer.objects.filter(municipality_id=municipality_id)
    #print(list(filers))
    reports=Report.objects.filter(filer_id__in=filers).filter(election_year=year).select_related("filer").select_related("purpose_code")
    return HttpResponse("<body>"+json.dumps([r.to_dict() for r in reports])+"</body>")

def municipality_contributions_year(request,municipality_id,year):
    context={"municipality":municipality_id,"year":year}
    return render(request, 'nys/chart.html', context)

def json_municipality_contributions_year(request,municipality_id,year):
    filers=Filer.objects.filter(municipality_id=municipality_id)
    #print(list(filers))
    reports=Report.objects.filter(filer_id__in=filers).filter(election_year=year).filter(transaction_code__in=["A","B","C"]).select_related("filer").select_related("purpose_code")
    d={}
    for r in reports:
        if r.filer_id not in d:
            d[r.filer_id]={"A":0.,"B":0.,"C":0.,"name":r.filer.name}
        d[r.filer_id][r.transaction_code]+=float(r.amount)
    w=[d[k] for k in d]
    return HttpResponse(json.dumps(w))
