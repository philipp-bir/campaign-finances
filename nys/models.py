from django.db import models

# Create your models here.

class CommitteeType(models.Model):
    name=models.TextField(unique=True)
    
    def __str__(self):
        return str(self.name)
        
class Office(models.Model):
    
    name = models.TextField()

class County(models.Model):
    
    name = models.TextField()
    

class Municipality(models.Model):
    
    name = models.TextField(blank=True)
    county = models.ForeignKey(County,on_delete=models.CASCADE)
    subdivision = models.TextField(blank=True)

class Filer(models.Model):
    
    filer_id = models.CharField(max_length=8)
    name = models.TextField()
    FILER_COMMITTEE="O"
    FILER_CANDIDATE="A"
    filer_type = models.CharField(max_length=1,choices=((FILER_COMMITTEE,"Committee"),(FILER_CANDIDATE,"Candidate")))
    FILER_INACTIVE="I"
    FILER_ACTIVE="A"
    status = models.CharField(max_length=1,choices=((FILER_INACTIVE,"Inactive"),(FILER_ACTIVE,"Active")))
    committee_type = models.ForeignKey(CommitteeType,null=True,on_delete=models.CASCADE)
   # office_id_lk = models.IntegerField(null=True)
    office = models.ForeignKey(Office,null=True,on_delete = models.CASCADE)
    district = models.IntegerField(null=True)
    treasurer_first_name = models.TextField(blank=True)
    treasurer_last_name = models.TextField(blank=True)
    address = models.TextField(blank=True)
    city = models.TextField(blank=True)
    state = models.TextField(blank=True)
    zipcode = models.TextField(blank=True)
    municipality = municipality = models.ForeignKey(Municipality,null=True,on_delete=models.CASCADE)

 

    

    
#class CountyFiler(Filer):
    
    #county = models.ForeignKey(County,on_delete=models.CASCADE)
#    municipality = models.ForeignKey(Municipality,on_delete=models.CASCADE)
    #district = models.IntegerField(null=True)
    
    
class Purpose(models.Model):
    
    code = models.CharField(max_length=5)
    description = models.TextField(blank=True)
    


class Report(models.Model):
    
    filer = models.ForeignKey(Filer,on_delete=models.CASCADE) # filer_ID
    filer_report_id = models.CharField(max_length=1) # FREPORT_ID (A-L)
    transaction_code = models.CharField(max_length=1, blank=True) #
    election_year = models.IntegerField(null=True)
    transaction_id = models.BigIntegerField(null=True)
    date = models.DateField(null=True)
    date_original = models.DateField(null=True)
    contributor_code = models.CharField(max_length=6,blank=True)
    contribution_type = models.CharField(max_length=1, blank=True)
    corporation_name = models.TextField(blank=True)
    contributor_first_name = models.TextField(blank=True)
    contributor_mid_initial = models.CharField(max_length=1, blank=True)
    contributor_last_name = models.TextField(blank=True)
    contributor_address = models.TextField(blank=True)
    contributor_city = models.TextField(blank=True)
    contributor_state = models.CharField(max_length=2,blank=True)
    contributor_zip = models.CharField(max_length=10,blank=True)
    check_number = models.TextField(blank=True)
    check_date = models.DateField(null=True)
    amount = models.DecimalField(null=True,max_digits=12,decimal_places=2)
    amount_additional = models.DecimalField(null=True,max_digits=12,decimal_places=2)
    description = models.TextField(blank=True)
    other_receipt_code = models.TextField(blank=True)
    purpose_code = models.ForeignKey(Purpose,null=True,on_delete=models.CASCADE)
    purpose_code_q = models.ForeignKey(Purpose,null=True,on_delete=models.CASCADE,related_name="q_report")
    explanation = models.TextField(blank=True)
    transfer_type = models.CharField(max_length=1,blank=True)
    checkbox = models.CharField(max_length=1,blank=True)
    user_id = models.CharField(max_length=8, blank=True)
    record_creation_datetime = models.DateTimeField(null=True)
    
    def contributor_full_name(self):
        if self.corporation_name!="":
            return self.corporation_name
        else:
            return "%s %s %s"%(self.contributor_first_name,self.contributor_mid_initial,self.contributor_last_name)
    
    def to_dict(self):
        d={}
        d["filer_id"] = self.filer.filer_id
        d["filer_report_id"] = self.filer_report_id
        d["transaction_code"] = self.transaction_code
        d["election_year"] = self.election_year
        d["transaction_id"] = self.transaction_id
        #d["date"] = self.date
        #d["date_original"] = self.date_original
        d["contributor_code"] = self.contributor_code
        d["contribution_type"] = self.contribution_type
        d["corporation_name"] = self.corporation_name
        d["contributor_first_name"] = self.contributor_first_name
        d["contributor_mid_initial"] = self.contributor_mid_initial
        d["contributor_last_name"] = self.contributor_last_name
        d["contributor_address"] = self.contributor_address
        d["contributor_city"] = self.contributor_city
        d["contributor_state"] = self.contributor_state
        d["contributor_zip"] = self.contributor_zip
        d["check_number"] = self.check_number
        # d["check_date"] = self.check_date
        #d["amount"] = self.amount
        #d["amount_additional"] = self.amount_additional
        d["description"] = self.description
        d["other_receipt_code"] = self.other_receipt_code
        d["purpose_code"] = self.purpose_code.code if self.purpose_code else None
      #  d["purpose_code_q"] = self.purpose_code_q.code if self.purpose_code_q else None
        d["explanation"] = self.explanation
        d["transfer_type"] = self.transfer_type
        d["checkbox"] = self.checkbox
        d["user_id"] = self.user_id
       # d["record_creation_datetime"] = self.record_creation_datetime
        return d
        
    
    @staticmethod
    def init_from_dict(d):
        return Report(filer = d["filer"],
                    filer_report_id = d["filer_report_id"],
                    transaction_code = d["transaction_code"],
                    election_year = d["election_year"],
                    transaction_id = d["transaction_id"],
                    date = d["date"],
                    date_original = d["date_original"],
                    contributor_code = d["contributor_code"],
                    contribution_type = d["contribution_type"],
                    corporation_name = d["corporation_name"],
                    contributor_first_name = d["contributor_first_name"],
                    contributor_mid_initial = d["contributor_mid_initial"],
                    contributor_last_name = d["contributor_last_name"],
                    contributor_address = d["contributor_address"],
                    contributor_city = d["contributor_city"],
                    contributor_state = d["contributor_state"],
                    contributor_zip = d["contributor_zip"],
                    check_number = d["check_number"],
                    check_date = d["check_date"],
                    amount = d["amount"],
                    amount_additional = d["amount_additional"],
                    description = d["description"],
                    other_receipt_code = d["other_receipt_code"],
                    purpose_code = d["purpose_code"],
                    purpose_code_q = d["purpose_code_q"],
                    explanation = d["explanation"],
                    transfer_type = d["transfer_type"],
                    checkbox = d["checkbox"],
                    user_id = d["user_id"],
                    record_creation_datetime = d["record_creation_datetime"]
                )

