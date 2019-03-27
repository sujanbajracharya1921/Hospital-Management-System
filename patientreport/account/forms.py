from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from .models import UserProfile,Admin,Receptionist,Patient,Doctor,Lab,Cashier,Medical,Doctor_Patient_Lab,Doctor_Patient_Med,Lab_Test,Appointment,Medical_Meds,Lab_Test_Bill,Feedback,Department


class UserLoginForm(forms.Form):
    email = forms.CharField(label='',widget=forms.EmailInput(attrs={'class':'form-control login_email','placeholder':'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control login_pass','placeholder':'Password'}))


    def clean(self,*args,**kwargs):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        # the_user = authenticate(name=name,password=password)
        # if not the_user:
        #     raise forms.ValidationError('invalid credentials')
        user_obj=UserProfile.objects.filter(email=email).first()
        if not user_obj:
            raise forms.ValidationError('invalid Email')
        else:
            if not user_obj.check_password(password):
                raise forms.ValidationError('invalid Password')

        # return super(UserLoginForm,self).clean(*args, **kwargs)

    # def clean_username(self):
    #     name=self.cleaned_data.get('name')
    #     user_qs=User.objects.filter(name=name).exist()
    #     if not user_qs:
    #         raise forms.ValidationError('invalid credentials')
    #     return name


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    is_lab= forms.BooleanField(label='Is_lab',required=False)
    is_doctor=forms.BooleanField(label='Is_doctor',required=False)
    is_medical=forms.BooleanField(label='Is_medical',required=False)
    is_receptionist=forms.BooleanField(label='is_receptionist',required=False)
    is_admin=forms.BooleanField(label='Is_admin',required=False)
    is_cashier=forms.BooleanField(label='Is_cashier',required=False)
    # join_date = forms.DateField(label='Join-Date', widget=forms.SelectDateWidget)




    class Meta:
        model = UserProfile
        fields = ('email', 'name', 'is_receptionist','is_doctor', 'is_medical','is_lab', 'is_admin','is_cashier','join_date')

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AdminForm(forms.ModelForm):
    address = forms.CharField(label='Address',widget=forms.TextInput(attrs={'class':'form-control'}))
    age= forms.IntegerField(label='Age',required=True,initial=20,widget=forms.NumberInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label="Sex",choices=(('Male','Male'),('Female','Female'),('Others','Others')),
                                initial='Others',
                                widget=forms.Select(attrs={'class':'form-control'}),
                                required=True)
    contact = forms.CharField(label='Contact', widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=Admin
        exclude=['user']


class AdminUpdateForm(forms.ModelForm):
    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=UserProfile
        fields=('name','email')

class DoctorUpdateForm(forms.ModelForm):
    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=UserProfile
        fields=('name','email')


class LabUpdateForm(forms.ModelForm):
    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=UserProfile
        fields=('name','email')


class ReceptionistForm(forms.ModelForm):
    address = forms.CharField(label='Address',widget=forms.TextInput(attrs={'class':'form-control'}))
    age= forms.IntegerField(label='Age',required=True,initial=20,widget=forms.NumberInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label="Sex",choices=(('Male','Male'),('Female','Female'),('Others','Others')),
                                initial='Others',
                                widget=forms.Select(attrs={'class':'form-control'}),
                                required=True)
    contact = forms.CharField(label='Contact', widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=Receptionist
        exclude=['user']

class ReceptionistUpdateForm(forms.ModelForm):
    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=UserProfile
        fields=('name','email')




class PatientForm(forms.ModelForm):
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(label='Address',widget=forms.TextInput(attrs={'class':'form-control'}))
    age= forms.IntegerField(label='Age',required=True,initial=20,widget=forms.NumberInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label="Sex",choices=(('Male','Male'),('Female','Female'),('Others','Others')),
                                initial='Others',
                                widget=forms.Select(attrs={'class':'form-control'}),
                                required=True)
    contact = forms.CharField(label='Contact', widget=forms.TextInput(attrs={'class':'form-control'}))
    # date = forms.DateField(label='Date', widget=forms.SelectDateWidget)

    class Meta:
        model=Patient
        exclude=["user","receptionist"]

class DoctorForm(forms.ModelForm):
    address = forms.CharField(label='Address',widget=forms.TextInput(attrs={'class':'form-control'}))
    age= forms.IntegerField(label='Age',required=True,initial=20,widget=forms.NumberInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label="Sex",choices=(('Male','Male'),('Female','Female'),('Others','Others')),
                                initial='Others',
                                widget=forms.Select(attrs={'class':'form-control'}),
                                required=True)
    contact = forms.CharField(label='Contact', widget=forms.TextInput(attrs={'class':'form-control'}))
    degree = forms.CharField(label='Degree', widget=forms.TextInput(attrs={'class':'form-control'}))
    specialist = forms.CharField(label='Specialist', widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=Doctor
        exclude=['user']

class LabForm(forms.ModelForm):
    address = forms.CharField(label='Address',widget=forms.TextInput(attrs={'class':'form-control'}))
    age= forms.IntegerField(label='Age',required=True,initial=20,widget=forms.NumberInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label="Sex",choices=(('Male','Male'),('Female','Female'),('Others','Others')),
                                initial='Others',
                                widget=forms.Select(attrs={'class':'form-control'}),
                                required=True)
    contact = forms.CharField(label='Contact', widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=Lab
        exclude=['user']

class Lab_Test_Result_Form(forms.ModelForm):
    test_name= forms.CharField(label='Test-Name',widget=forms.TextInput(attrs={'class':'form-control'}))

    # result = forms.CharField(label='Result', widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model=Lab_Test
        exclude=['patient','lab']

class Lab_Test_Bill_Form(forms.ModelForm):
    sample= forms.BooleanField(label='Sample-Collected')
    test_name= forms.CharField(label='Test-Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    status = forms.ChoiceField(label="Status",choices=(('Done','Done'),('Pending','Pending')),
                        initial='Pending',widget=forms.Select(attrs={'class':'form-control'}),
                        required=True)
    amount=forms.IntegerField(label='Amount',initial="0",required=True,widget=forms.NumberInput(attrs={'class':'form-control '}))


    class Meta:
        model=Lab_Test_Bill
        exclude=['patient','lab']

class Medical_Meds_Forms(forms.ModelForm):
    opt = []
    my = Doctor_Patient_Med.objects.all()
    for x in my:
        opt.append([x.medicines,x.medicines])

    medicines =forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=opt)
    amount=forms.IntegerField(label='Amount',initial="0",required=True,widget=forms.NumberInput(attrs={'class':'form-control '}))
    p_date=forms.widgets.DateTimeInput(attrs={'type':'date'})
    # p_date = forms.DateTimeField(label='Purchase-Date', widget=forms.DateTimeInput(attrs={'type':'date'}))
    print(medicines)

    class Meta:
        model=Medical_Meds
        exclude=['patient','doctor','medical']


class MedicalForm(forms.ModelForm):
    address = forms.CharField(label='Address',widget=forms.TextInput(attrs={'class':'form-control'}))
    age= forms.IntegerField(label='Age',required=True,initial=20,widget=forms.NumberInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label="Sex",choices=(('Male','Male'),('Female','Female'),('Others','Others')),
                                initial='Others',
                                widget=forms.Select(attrs={'class':'form-control'}),
                                required=True)
    contact = forms.CharField(label='Contact', widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=Medical
        exclude=['user']

class MedicalUpdateForm(forms.ModelForm):
    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=UserProfile
        fields=('name','email')

class cashierForm(forms.ModelForm):
    class Meta:
        model=Cashier
        exclude=['user']



class Doctor_Patient_Med_Form(forms.ModelForm):
    medicines=forms.CharField(label='Medicine',widget=forms.TextInput(attrs={'class':'form-control'}))
    comments=forms.CharField(label='Comments',widget=forms.TextInput(attrs={'class':'form-control'}))
    follow_up = forms.DateTimeField(label='Follow-up-Date', widget=forms.DateTimeInput(attrs={'type':'date'}),required=False)

    class Meta:
        model=Doctor_Patient_Med
        exclude=['patient','doctor']



class Doctor_Patient_Lab_Form(forms.ModelForm):
    opt=(('Blood-Test','Blood-Test'),('Cholestrol-Level','Cholestrol-Level'),('RBC','RBC'),('Sugar-Level','Sugar-Level'),('WBC','WBC'),('Uric-Acid','Uric-Acid'),('Blood-Culture','Blood-Culture'),('Vitamin-Test','Vitamin-Test'))
    lab=forms.MultipleChoiceField(label='Tests',widget=forms.CheckboxSelectMultiple, choices=opt)
    comments=forms.CharField(label='Comments',widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=Doctor_Patient_Lab
        exclude=['patient','doctor']

class ReceptionistUpdateForm(forms.ModelForm):
    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))


    class Meta:
        model=UserProfile
        fields=('name','email')

class AppointmentForm(forms.ModelForm):
    patient_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control name','placeholder':'Patient-Name'}))
    address = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control address','placeholder':'Address'}))
    Phone_no = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control cell','placeholder':'Contact-Number'}))
    email= forms.EmailField(label='',widget=forms.EmailInput(attrs={'class':'form-control appointment_email','placeholder':'Email Address'}))
    gender= forms.ChoiceField(label="",choices=(('Male','Male'),('Female','Female'),('Others','Others'),('Gender','Gender')),
                                initial='Gender',
                                widget=forms.Select(attrs={'class':'form-control appointment_gender_choice'}),
                                required=True)

    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(),label = 'Doctor', widget=forms.Select(attrs={'class':'form-control department'}))

    department = forms.ChoiceField(label="",choices=(('ENT','ENT'),('EYE','EYE'),('BONE','BONE'),('Others','Others'),('Choose Department','Choose Department')),initial='Choose Department',
                                widget=forms.Select(attrs={'class':'form-control department'}),required=True)
    appointment_date= forms.DateField(label='Appointment Date', widget=forms.SelectDateWidget(attrs={'class':'form-control department'}))
    preffered_time = forms.TimeField(label='',widget=forms.TimeInput(format='%H:%M',attrs={'class':'form-control department','placeholder':'Preffered_Time'}))

    class Meta:
        model=Appointment
        exclude=['end_time']

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user','')
    #     super(AppointmentForm, self).__init__(*args, **kwargs)
    #     self.fields['doctor']=forms.ModelChoiceField(queryset=Doctor.objects.all())

class FeedbackForm(forms.ModelForm):
    name= forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control name','placeholder':'Name'}))
    contact= forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control name','placeholder':'Contact'}))
    email= forms.EmailField(label='',widget=forms.EmailInput(attrs={'class':'form-control appointment_email','placeholder':'Email Address'}))
    message = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control appointment_email','placeholder':'Message'}))

    class Meta:
        model=Feedback
        fields=('__all__')


class DepartmentForm(forms.ModelForm):

    department= forms.ChoiceField(label="Department",choices=(('OPD','OPD'),('Operation','Operation'),('ENT','ENT'),('Skin','Skin'),('Eye','Eye'),('Heart','Heart'),),
                            initial='OPD',
                            widget=forms.Select(attrs={'class':'form-control name'}),
                            required=True)
    # doctor= forms.ModelChoiceField(label='Doctor',widget=forms.Select(attrs={'class':'form-control name'}))

    class Meta:
        model=Department
        fields=('__all__')

    def __init__(self, *args, **kwargs):
        queryset=Doctor.objects.all()
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor']=forms.ModelChoiceField(queryset=Doctor.objects.all(),widget=forms.Select(attrs={'class':'form-control name'}))



class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    Previous_Password=forms.CharField(label='Previous Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='New Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = UserProfile
        fields = ('password',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        password = self.cleaned_data.get("password")
        Previous_Password = self.cleaned_data.get("Previous_Password")
        if password and Previous_Password and password != Previous_Password:
            raise forms.ValidationError("Passwords doesn't match")

        return self.initial["password"]

    def clean_password2(self):
        # Check that the two password entries match

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords doesn't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
