from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date






class User(AbstractUser):
    USER_ROLE_CHOICES = (
    ("admin", 1),
    ("user", 2),
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    username = None
    role = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES,default=USER_ROLE_CHOICES[1][1])
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        
        

class Biography (models.Model):
     description=models.CharField(max_length=255,null=False,blank=False,default='description')
     email=models.EmailField(max_length=150,default="email",blank=False,null=False)  
     personal_website=models.URLField(max_length=200)
     
     class Meta:
        db_table='Biography'



class social_media (models.Model):
    socialMedia_name=models.CharField(max_length=100,null=False,blank=False,default="linkedin")
    socialMedia_link=models.URLField(max_length=200)
    socialMedia_bio=models.ForeignKey(Biography,on_delete=models.CASCADE)

    class Meta:
        db_table='SocialMedia'
    
    

class Portfolio (models.Model):
    full_name = models.CharField(max_length=100,null=False,blank=False,default='name')    
    occupation = models.CharField(max_length=100,null=False,blank=False,default='occupation')  
    career_summary = models.CharField(max_length=255,null=False,blank=False,default='career_summary')
    philosophy_statement = models.CharField(max_length=200,blank=True,null=True)  
    bio=models.OneToOneField(Biography,on_delete=models.CASCADE)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True, blank=True)

    class Meta:
      db_table='Portfolio'



class professional_accomplishment(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,default="accomplishment_name")
    category = models.CharField(max_length=100,blank=False,default="accomplishment_category")
    accomplishment_portfolio=models.ForeignKey(Portfolio,on_delete=models.CASCADE)
    
    class Meta:
     db_table='Professional_accomplishments'




class award(models.Model):
    title = models.CharField(max_length=100,null=False,blank=False,default="title")
    date = models.DateField(default=date(2000,1,1))
    recognition_level = models.CharField(max_length=100,null=True,blank=True)
    award_portfolio=models.ForeignKey(Portfolio,on_delete=models.CASCADE)

    class Meta:
     db_table='Awards'
     


class justification (models.Model):
    name=models.CharField(max_length=100,null=False,blank=False,default="jutification_name")
    photo=models.ImageField(upload_to='photos/justification',max_length=200,null=True,blank=True)
    file = models.FileField(upload_to='files/justification', max_length=254,blank=False,null=False)
    accomplishment_justification=models.ForeignKey(professional_accomplishment,on_delete=models.CASCADE)
    award_justification=models.ForeignKey(award,on_delete=models.CASCADE)
    
    class Meta:
     db_table='Justifications'



class certification (models.Model):
   title = models.CharField(max_length=100,null=False,blank=False,default="title")
   description=models.CharField(max_length=255,null=False,blank=False,default='description')
   document_link=models.URLField(max_length=200)
   certification_portfolio=models.ForeignKey(Portfolio,on_delete=models.CASCADE)

   class Meta:
    db_table='Certifications'



class community_service (models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,default='name')    
    description = models.CharField(max_length=255,null=False,blank=False,default='description')
    service_portfolio=models.ForeignKey(Portfolio,on_delete=models.CASCADE)
    
    class Meta:
     db_table='Community_services'


class reference (models.Model):
    title = models.CharField(max_length=100,null=False,blank=False,default='title')
    job_title=  models.CharField(max_length=100,null=False,blank=False,default='jobtitle')  
    email=models.EmailField(max_length=150,default="email",blank=False,null=False) 
    phone_number=models.PositiveIntegerField(default=11111111,blank=False,null=False)
    reference_portfolio=models.ForeignKey(Portfolio,on_delete=models.CASCADE)
    
    class Meta:
        db_table='References'


        