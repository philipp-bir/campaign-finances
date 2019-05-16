from .models import Filer,CommitteeType, Report, Purpose, Office, Municipality, County

import re
from django.utils import timezone
from dateutil.parser import parse as parse_datetime
import dateutil.tz
import os
import traceback
import csv

c=0
FILER_ID=c
c+=1
FILER_NAME=c
c+=1
FILER_TYPE=c
c+=1
STATUS=c
c+=1
COMMITTEE_TYPE=c
c+=1
OFFICE=c
c+=1
DISTRICT=c
c+=1
TREAS_FIRST_NAME=c
c+=1
TREAS_LAST_NAME=c
c+=1
ADDRESS=c
c+=1
CITY=c
c+=1
STATE=c
c+=1
ZIP=c
c+=1
CC_ROW_LENGTH=c

def insert_row(row):
    if len(row)!=CC_ROW_LENGTH:
        raise Exception("Wrong length %d"%len(row))
    row=[w.strip() for w in row]
    ct,__=CommitteeType.objects.get_or_create(name=row[COMMITTEE_TYPE])
    office,__=Office.objects.get_or_create(id=int(row[OFFICE])) if row[OFFICE] else (None,None)
    district=int(row[DISTRICT])if row[DISTRICT] else None
    if row[STATUS].upper()=="ACTIVE":
        status=Filer.FILER_ACTIVE
    elif row[STATUS].upper()=="INACTIVE":
        status=Filer.FILER_INACTIVE
    else:
        status=None
        print("Unknown status %s"%row[STATUS])
    if row[FILER_TYPE].upper()=="COMMITTEE":
        filer_type=Filer.FILER_COMMITTEE
    elif row[FILER_TYPE].upper()=="CANDIDATE":
        filer_type=Filer.FILER_CANDIDATE
    else:
        filer_type=None
        print("Unknown filer type %s"%row[FILER_TYPE])
    Filer.objects.get_or_create(filer_id=row[FILER_ID], name=row[FILER_NAME],
                                         filer_type=filer_type, status=status,
                                         committee_type=ct, office=office, district=district,
                                         treasurer_first_name=row[TREAS_FIRST_NAME], treasurer_last_name=row[TREAS_LAST_NAME],
                                         address=row[ADDRESS],city=row[CITY],state=row[STATE],
                                         zipcode=row[ZIP])
    

def import_commcand_csv(file_name):
    with open(file_name) as csvfile:
        #lines=iter(csvfile)
        leftover=[]
        for i,line in enumerate(csvfile):
            cells=line.strip().split('","')
            if len(cells)==0:
                continue
            if cells[0][:1]=='"':
                cells[0]=cells[0][1:]
            if cells[-1][-1:]=='"':
                cells[-1]=cells[-1][:-1]
            if len(cells)==CC_ROW_LENGTH:
                # normal case
                insert_row(cells)
                if len(leftover)>0:
                    print("Couldn't place line %d."%i)
                    leftover=[]
            elif len(leftover)>0 and len(leftover)+len(cells)==CC_ROW_LENGTH+1:
                cells=leftover[:-1]+[leftover[-1]+" "+cells[0]]+cells[1:]
                insert_row(cells)
                #print("recovered line %d - %s"%(i,str(cells)))
                leftover=[]
            elif len(leftover+cells)>CC_ROW_LENGTH+1:
                print("Couldn't place line %d, length = %d."%(i+1,len(cells)))
            else:
                leftover=cells





def date_or_none(s):
    if len(s)>0:
        return parse_datetime(s).date()
    else:
        return None
        
def datetime_or_none(s):
    if len(s)>0:
        return timezone.make_aware(parse_datetime(s),dateutil.tz.gettz("US/Eastern"))
    else:
        return None
        
def get_purpose(s,purpose_dict):
    if len(s)==0:
        return None
    s=s.upper()
    if s in purpose_dict:
        return purpose_dict[s]
    else:
        s=re.sub("[^A-Z0-9]","",s)
        if s in purpose_dict:
            return purpose_dict[s]
        else:
            p=Purpose(code=s,description="")
            p.save()
            purpose_dict[s]=p
            return p

def prepare_row_report(row,filer_dict,purpose_dict):
    try:
        row=[r.strip() for r in row]
        report_dict={}
        i=0
        report_dict["filer"]=filer_dict[row[i]]
        i+=1
        report_dict["filer_report_id"]=row[i]
        i+=1
        report_dict["transaction_code"]=row[i]
        i+=1
        report_dict["election_year"]=int(row[i]) if len(row[i])>0 else None
        i+=1
        report_dict["transaction_id"]=int(row[i])  if len(row[i])>0 else None
        i+=1
        report_dict["date"]=date_or_none(row[i])
        i+=1
        report_dict["date_original"]=date_or_none(row[i])
        i+=1
        report_dict["contributor_code"]=row[i]
        i+=1
        report_dict["contribution_type"]=row[i]
        i+=1
        report_dict["corporation_name"]=row[i]
        i+=1
        report_dict["contributor_first_name"]=row[i]
        i+=1
        report_dict["contributor_mid_initial"]=row[i]
        i+=1
        report_dict["contributor_last_name"]=row[i]
        i+=1
        report_dict["contributor_address"]=row[i]
        i+=1
        report_dict["contributor_city"]=row[i]
        i+=1
        report_dict["contributor_state"]=row[i]
        i+=1
        report_dict["contributor_zip"]=row[i]
        i+=1
        report_dict["check_number"]=row[i]
        i+=1
        report_dict["check_date"]=date_or_none(row[i])
        i+=1
        report_dict["amount"]=abs(float(row[i])) if len(row[i])>0 else None #amounts are positive values
        i+=1
        report_dict["amount_additional"]=abs(float(row[i])) if len(row[i])>0 else None
        i+=1
        report_dict["description"]=row[i]
        i+=1
        report_dict["other_receipt_code"]=row[i]
        i+=1
        report_dict["purpose_code"]=get_purpose(row[i],purpose_dict)
        i+=1
        report_dict["purpose_code_q"]=get_purpose(row[i],purpose_dict)
        i+=1
        report_dict["explanation"]=row[i]
        i+=1
        report_dict["transfer_type"]=row[i]
        i+=1
        report_dict["checkbox"]=row[i]
        i+=1
        report_dict["user_id"]=row[i]
        i+=1
        report_dict["record_creation_datetime"]=datetime_or_none(row[i])
    except:
        print(traceback.format_exc())
        return None
    return Report.init_from_dict(report_dict)

REPORT_LEN_ROW=30
BULK_SIZE=10000
def import_reports_csv(file_name,out_file_name=os.devnull,start_with=0):
    filer_dict={}
    purpose_dict={}
    reports=[]
    for f in Filer.objects.all():
        filer_dict[f.filer_id]=f
    for p in Purpose.objects.all():
        purpose_dict[p.code]=p 
    with open(file_name,encoding="latin-1") as csvfile:
        with open(out_file_name,"w") as outf:
            try:
                leftover=[]
                leftover_lines=""
                for i,line in enumerate(csvfile):
                    
                    if i<start_with:
                        continue
                    elif i==start_with:
                        print("Line to start with:")
                        print(line)

                    if (i+1)%BULK_SIZE==0:
                        print("Line #%d."%(i+1))
                        Report.objects.bulk_create(reports)
                        reports=[]
                        print("Insert done.")

                    row=line.strip().split('","')
                    if len(row)==0:
                        continue
                    if row[0][:1]=='"':
                        row[0]=row[0][1:]
                    if row[-1][-1:]=='"':
                        row[-1]=row[-1][:-1]
                    if len(row)==REPORT_LEN_ROW:
                        # normal case
                        report=prepare_row_report(row,filer_dict,purpose_dict)
                        if report:
                            reports+=[report]
                        else:    
                            leftover_lines+=line
                            outf.write(leftover_lines)
                            print("Couldn't place line %d.[1]"%(i+1))
                            leftover=[]
                            leftover_lines=""
                            continue
                        if len(leftover)>0:
                            print("Couldn't place line %d.[2]"%i)
                            outf.write(leftover_lines)
                            leftover=[]
                            leftover_lines=""
                    elif len(leftover)>0 and len(leftover)+len(row)==REPORT_LEN_ROW+1:
                        row=leftover[:-1]+[leftover[-1]+" "+row[0]]+row[1:]
                        report=prepare_row_report(row,filer_dict,purpose_dict)
                        if report:
                            reports+=[report]
                        else:
                            leftover_lines+=line
                            outf.write(leftover_lines)
                            print("Couldn't place line %d.[3]"%(i+1))
                            leftover=[]
                            leftover_lines=""
                            continue
                        print("recovered line %d"%(i))
                        leftover=[]
                        leftover_lines=""
                    elif len(leftover)+len(row)>REPORT_LEN_ROW+1:
                        print("Couldn't place line %d, length = %d."%(i+1,len(row)))
                        outf.write(leftover_lines+line)
                        leftover=[]
                        leftover_lines=""
                    else:
                        leftover+=row
                        leftover_lines+=line
                print("Line #%d (last)."%(i+1))
                Report.objects.bulk_create(reports)
                reports=[]
                print("Insert done.")
            except:
                print(traceback.format_exc())
                print("Line %d"%i)
                
                
                
                
                
def import_county_filers_csv(file_name):
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for i,row in enumerate(reader):
            if i%1000==0:
                print("Row #%d"%i)
            #print(row)
            #return
            try:
                f=Filer.objects.get(filer_id=row["Filer ID"])
                if f.name!=row["Name"].strip():
                    print("Name not the same with filer %s"%row["Filer ID"])
                    print("'%s' - '%s'"%(f.name,row["Name"].strip()) )
                if f.office is not None and len(f.office.name)==0:
                    f.office.name=row["Office"]
                    print("Office #%d is '%s'"%(f.office.id,f.office.name))
                    f.office.save()
                elif (f.office is None and row["Office"]!="N/A") or (f.office is not None and str(f.office.name)!=row["Office"]):
                    print("Office not the same with filer %s"%row["Filer ID"])
                    print("'%s' - '%s'"%(f.office.name,row["Office"]) )
                if (f.district is None and row["District"]!="N/A") or (f.district is not None and str(f.district)!=row["District"]):
                    print("District not the same with filer %s"%row["Filer ID"])
                    print("'%s' - '%s'"%(f.district,row["District"]) )
                county,__=County.objects.get_or_create(name=row["County"])
                if row["Municipality"]=="N/A":
                    row["Municipality"]=""
                if row["Subdivision"]=="N/A":
                    row["Subdivision"]=""
                f.municipality,__ = Municipality.objects.get_or_create(name=row["Municipality"],county=county,subdivision=row["Subdivision"])
                f.save()
            except KeyboardInterrupt:
                return
            except:
                print(traceback.format_exc())
                print(row["Filer ID"])
        
        
pass
        
        
        
        
        
