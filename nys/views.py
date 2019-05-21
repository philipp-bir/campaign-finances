import json

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

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
    context={"municipality":Municipality.objects.get(pk=municipality_id),"year":year}
    return render(request, 'nys/chart.html', context)

def json_municipality_contributions_year(request,municipality_id,year):
    filers=Filer.objects.filter(municipality_id=municipality_id)
    #print(list(filers))
    reports=(Report.objects.filter(filer_id__in=filers)
                           .filter(election_year=year)
                           .filter(transaction_code__in=["A","B","C"])
                           .select_related("filer")
                           .select_related("purpose_code")
                           .select_related("purpose_code_q")
            )
    d={}
    for r in reports:
        if r.filer_id not in d:
            links={}
            for c in ["A","B","C"]:
                links[c]=reverse("filers_contributions_year_type",kwargs={"filer_id":r.filer_id,"year":year,"t_code":c})
            d[r.filer_id]={"A":0.,"B":0.,"C":0.,"meta":{"name":r.filer.name,"count":{"A":0,"B":0,"C":0},"link":links}}
        d[r.filer_id][r.transaction_code]+=float(r.amount)
        d[r.filer_id]["meta"]["count"][r.transaction_code]+=1
    for k in d:
        d[k]["meta"]["desc"]={c:"$%.02f in %d contributions"%(d[k][c],d[k]["meta"]["count"][c]) for c in "ABC"}
    #w=[d[k] for k in d]
    response={"data":list(d.values()),"meta":{"A":"Individual & Partnerships","B":"Corporate","C":"All Other"}}
    return HttpResponse(json.dumps(response))

def filers_contributions_year(request,filer_id,year,t_code=None):
    filer=Filer.objects.get(pk=filer_id)
    
    reports=Report.objects.filter(filer_id=filer_id).filter(election_year=year)
    if t_code:
        reports=reports.filter(transaction_code=t_code)
    else:
        reports=reports.filter(transaction_code__in=["A","B","C"]) 
    reports=reports.select_related("filer").select_related("purpose_code").select_related("purpose_code_q").order_by("-amount")
    context={"filer":filer,"year":year,"t_code":t_code,"t_code_desc":{"A":"Individual & Partnerships","B":"Corporate","C":"All Other"}[t_code] if t_code else None,"reports":reports}
    return render(request, 'nys/pie_chart.html', context)

def json_filers_contributions_year(request,filer_id,year,t_code=None):
    reports=Report.objects.filter(filer_id=filer_id).filter(election_year=year)
    if t_code:
        reports=reports.filter(transaction_code=t_code)
    else:
        reports=reports.filter(transaction_code__in=["A","B","C"]) #potentially relax to all that are about money received
    reports=reports.select_related("filer").select_related("purpose_code").select_related("purpose_code_q")
    d={}
    for r in reports:
        cc=r.contributor_code
        if cc not in d:
            d[cc]={"value":0,"number":0,"label":cc}
        d[cc]["value"]+=float(r.amount)
        d[cc]["number"]+=1
    for k in d:
        d[k]["desc"]="$%.02f in %d contributions with code '%s'"%(d[k]["value"],d[k]["number"],k)
    return HttpResponse(json.dumps(list(d.values())))
    
    
    
    
    
    
    
