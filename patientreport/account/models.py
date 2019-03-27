
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from .utils import code_generator
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from datetime import datetime
from ckeditor.fields import RichTextField


# Create your models here.


USERNAME_REGEX='^[a-zA-z0-9.+-]*$'

class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model """

    def create_user(self,email,name,password=None):
        """Creates a new user profile object """

        if not email:
            raise ValueError("Users must have an email address")
        email=self.normalize_email(email)
        user=self.model(email=email,name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name,password):
        """Creates and saves a new superuser with given details """

        user=self.create_user(email,name,password)
        user.is_superadmin=True
        user.is_staff=True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser):
    """Represents a user profile inside our system"""
    name=models.CharField(max_length=255,validators=[RegexValidator(regex=USERNAME_REGEX,message='Username must be Alphanumeric or contain any of the following:". @ + -" ',code='invalid_username')])
    email=models.EmailField(verbose_name='email address',max_length=255,unique=True)

    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_doctor=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_lab=models.BooleanField(default=False)
    is_receptionist=models.BooleanField(default=False)
    is_cashier=models.BooleanField(default=False)
    is_medical=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    join_date=models.DateField(default=timezone.now)

    # password=models.CharField(max_length=20)
    #
    #
    # def save(self,*args,**kwargs):
    #     self.password=code_generator()
    #     super(UserProfile,self).save(*args,**kwargs)


    objects=UserProfileManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']

    def get_full_name(self):
        """Used to get users full name """

        return self.name

    def get_short_name(self):
        """Used to get users full name """
        return self.name

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_Label):
        return self.is_admin

    # @property
    # def is_staff(self):
    #     return self.is_admin
    # @property
    # def is_staff(self):
    #
    #     "Is the user a member of staff?"
    #     "Simplest possible answer: All admins are staff"
    #     return self.is_admin

    def __str__(self):

        """ Django uses this when it needs to convert the objects a string """
        return self.name


class Admin(models.Model):
    address=models.CharField(max_length=150)
    age=models.IntegerField(blank=True,default=11)

    sex_category=(('Male','Male'),('Female','Female'),('Others','Others'),)
    sex=models.CharField(max_length=50,choices=sex_category,default="Male")
    contact=models.CharField(max_length=20)
    image=models.ImageField(upload_to = 'photo/',blank=True,null=True)
    user  = models.OneToOneField(UserProfile)


    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_Label):
        return self.is_admin

    def __str__(self):
        return self.user.name



class Receptionist(models.Model):
    address=models.CharField(max_length=150)
    age=models.IntegerField(blank=True,default=11)

    sex_category=(('Male','Male'),('Female','Female'),('Others','Others'),)
    sex=models.CharField(max_length=50,choices=sex_category,default="Male")
    contact=models.CharField(max_length=20)
    image=models.ImageField(upload_to = 'photo/',blank=True,null=True)

    # patient=models.ForeignKey(Patient)
    user  = models.OneToOneField(UserProfile)

    def has_perm(self,perm,obj=None):
        return self.is_receptionist

    def has_module_perms(self,app_Label):
        return self.is_receptionist


    def __str__(self):
        return self.user.name

class Patient(models.Model):
    name=models.CharField(max_length=30)
    age=models.IntegerField(blank=True,default=11)

    sex_category=(('Male','Male'),('Female','Female'),('Others','Others'),)
    sex=models.CharField(max_length=50,choices=sex_category,default="Male")
    address=models.CharField(max_length=150)
    contact=models.CharField(max_length=20)
    date=models.DateTimeField(default=datetime.now)
    receptionist=models.ForeignKey(Receptionist)

    def has_perm(self,perm,obj=None):
        return self.is_receptionist

    def has_module_perms(self,app_Label):
        return self.is_receptionist

    def __str__(self):
        return self.name


class Doctor(models.Model):
    address=models.CharField(max_length=150)
    age=models.IntegerField(blank=True,default=11)

    sex_category=(('Male','Male'),('Female','Female'),('Others','Others'),)
    sex=models.CharField(max_length=50,choices=sex_category,default="Male")
    contact=models.CharField(max_length=20)
    image=models.ImageField(upload_to = 'photo/',blank=True,null=True)
    degree=models.CharField(max_length=20,blank=True,null=True)
    specialist=models.CharField(max_length=20,blank=True,null=True)
    # department=models.OneToOneField(Department)
    user  = models.OneToOneField(UserProfile)

    def has_perm(self,perm,obj=None):
        return self.is_doctor

    def has_module_perms(self,app_Label):
        return self.is_doctor

    def __str__(self):
        return self.user.name


class Department(models.Model):
    option=(('OPD','OPD'),('Operation','Operation'),('ENT','ENT'),('Skin','Skin'),('Eye','Eye'),('Heart','Heart'),)
    department=models.CharField(max_length=50,choices=option,default="OPD")
    doctor=models.ForeignKey(Doctor)

    def __str__(self):
        return self.department



class Lab(models.Model):
    address=models.CharField(max_length=150)
    age=models.IntegerField(blank=True,default=11)

    sex_category=(('Male','Male'),('Female','Female'),('Others','Others'),)
    sex=models.CharField(max_length=50,choices=sex_category,default="Male")
    contact=models.CharField(max_length=20)
    image=models.ImageField(upload_to = 'photo/',blank=True,null=True)

    user  = models.OneToOneField(UserProfile)

    # patient=models.ForeignKey(Patient)

    def has_perm(self,perm,obj=None):
        return self.is_lab

    def has_module_perms(self,app_Label):
        return self.is_lab

    def __str__(self):
        return self.user.name

class Medical(models.Model):
    address=models.CharField(max_length=150)
    age=models.IntegerField(blank=True,default=11)

    sex_category=(('Male','Male'),('Female','Female'),('Others','Others'),)
    sex=models.CharField(max_length=50,choices=sex_category,default="Male")
    contact=models.CharField(max_length=20)
    image=models.ImageField(upload_to = 'photo/',blank=True,null=True)
    user  = models.OneToOneField(UserProfile)

    def has_perm(self,perm,obj=None):
        return self.is_medical

    def has_module_perms(self,app_Label):
        return self.is_medical

    def __str__(self):
        return self.user.name


class Cashier(models.Model):
    address=models.CharField(max_length=150,default='Nepal')
    age=models.IntegerField(blank=True,default=11)

    sex_category=(('Male','Male'),('Female','Female'),('Others','Others'),)
    sex=models.CharField(max_length=50,choices=sex_category,default="Male")
    contact=models.CharField(max_length=20)
    image=models.ImageField(upload_to = 'photo/',blank=True,null=True)
    user  = models.OneToOneField(UserProfile)

    def has_perm(self,perm,obj=None):
        return self.is_cashier

    def has_module_perms(self,app_Label):
        return self.is_cashier


    def __str__(self):
        return self.user.name

class Doctor_Patient_Med(models.Model):
    medicines=models.CharField(max_length=1000,blank=False)
    comments=models.TextField(max_length=1000,blank=False)
    follow_up=models.DateField(null=True,blank=True)
    date=models.DateField(default=timezone.now(),null=True,blank=True)
    patient=models.ForeignKey(Patient)
    doctor=models.ForeignKey(Doctor)

    def __str__(self):
        return self.patient.name

class Doctor_Patient_Lab(models.Model):
    lab=models.CharField(max_length=250,blank=False)
    comments=models.TextField(max_length=250,blank=False)
    date=models.DateTimeField(default=datetime.now)
    patient=models.ForeignKey(Patient)
    doctor=models.ForeignKey(Doctor)

    def __str__(self):
        return self.patient.name

class Lab_Test(models.Model):
    test_name=models.CharField(max_length=250,blank=False)
    result=models.TextField(blank=False)
    test_date=models.DateTimeField(default=datetime.now)
    patient=models.ForeignKey(Patient,related_name='labtests')
    lab=models.ForeignKey(Lab)


    def __str__(self):
        return self.patient.name


class Lab_Test_Bill(models.Model):
    sample=models.BooleanField(default=False,blank=False)
    test_name=models.CharField(max_length=250,blank=False)
    status=models.CharField(max_length=250,blank=False,choices=(('Done','Done'),('Pending','Pending')),
                            default='Pending')
    amount=models.IntegerField(default=0)
    test_date=models.DateTimeField(default=datetime.now)
    patient=models.ForeignKey(Patient)
    lab=models.ForeignKey(Lab)



    def save(self, *args, **kwargs):
        for field_name in ['test_name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
                super(Lab_Test_Bill, self).save(*args, **kwargs)


    def __str__(self):
        return self.patient.name


class Medical_Meds(models.Model):

    medicines=models.CharField(max_length=250)
    amount=models.IntegerField(default=0)
    # is_purchase=models.BooleanField(default=False)
    p_date=models.DateTimeField(default=datetime.now)
    patient=models.ForeignKey(Patient)
    medical=models.ForeignKey(Medical)



    def __str__(self):
        return self.patient.name

class Appointment(models.Model):

    patient_name=models.CharField(max_length=250,blank=False)
    address=models.CharField(max_length=250,blank=False)
    Phone_no=models.CharField(max_length=250,blank=False)
    email=models.EmailField(max_length=250,blank=False)

    sex_category=(('Male','Male'),('Female','Female'),('Others','Others'),)
    gender=models.CharField(max_length=50,choices=sex_category,default="Male")

    dep_detail=(('ENT','ENT'),('EYE','EYE'),('BONE','BONE'),('Others','Others'),)
    department=models.CharField(max_length=50,choices=dep_detail,default=None)

    doctor=models.ForeignKey(Doctor,default=None)

    appointment_date=models.DateField(blank=True,null=True)
    preffered_time=models.TimeField(blank=False,null=False,default=None)
    end_time=models.TimeField(blank=True,null=True)


    def __str__(self):
        return self.patient_name

class Feedback(models.Model):
    name=models.CharField(max_length=25)
    contact=models.IntegerField(unique=True)
    email=models.EmailField(verbose_name='email address',max_length=255,unique=True)
    message=models.TextField(blank=False)

    def __str__(self):
        return self.name


class ActivationProfile(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    key=models.CharField(max_length=120,default=code_generator)
    expired=models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        self.key=code_generator()
        super(ActivationProfile,self).save(*args,**kwargs)
    def __str__(self):
        return self.user.name

def post_save_activation_receiver(sender,instance,created,*args,**kwargs):
    if created:
        print('activation created')
post_save.connect(post_save_activation_receiver, sender=ActivationProfile)


def post_save_user_model_receiver(sender,instance,created,*args,**kwargs):
    if created:
        try:
            profile.objects.create(user=instance)
            ActivationProfile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)
