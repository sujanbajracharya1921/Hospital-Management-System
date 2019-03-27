from django.contrib.auth import login,get_user_model,logout
from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserCreationForm,UserLoginForm,DoctorForm,AdminForm,AdminUpdateForm,DoctorUpdateForm,Doctor_Patient_Med_Form,Doctor_Patient_Lab_Form,LabForm,LabUpdateForm,Lab_Test_Result_Form,MedicalForm,MedicalUpdateForm,ReceptionistUpdateForm,ReceptionistForm,PatientForm,UserChangeForm,Medical_Meds_Forms,AppointmentForm,Lab_Test_Bill_Form,FeedbackForm,DepartmentForm
from .models import Doctor,Lab,Medical,Cashier,UserProfile,Receptionist,Patient,Admin,Doctor_Patient_Lab,Doctor_Patient_Med,Lab_Test,Appointment,Medical_Meds,Lab_Test_Bill,Department
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .utils import render_to_pdf
import datetime
from django.db.models import Count
import types
from datetime import date
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def admin_appointment_list(request):
    if request.user.is_admin or request.user.is_superadmin:
        appt=Appointment.objects.all()
        return render (request,'admin_appointment_list.html',{'appt':appt})


def createEvent2(request):
    if request.method == "POST":
        department= request.GET.get('department','').split(',')

        Department.objects.create(
        department=department,
        )
        return HttpResponse('')

def doc_search(request):
    form=DepartmentForm(request.POST or None,request.FILES or None)
    doc1=Department.objects.all()
    return render (request,'doc_search.html',{'form':form,'doc1':doc1})


def depart_search(request):
    if request.method=="POST":
        srch=request.POST.get('srh')
        print(srch)

        if srch:
            match=Department.objects.filter(Q(doctor__user__name__icontains=srch)|Q(department__icontains=srch))

            if match:
                return render(request,'depart_search.html',{'sr':match})

            else:
                messages.error(request,'no result found')
        else:
            return HttpResponseRedirect('search')
    return render(request,'depart_search.html')


def department(request):
    if request.user.is_admin or request.user.is_superadmin :
        form=DepartmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('department')

        return render(request,'department.html',{'form':form})


def pagination(request):
    user_list = Doctor.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 3)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'user_list.html', { 'users': users })


User=get_user_model()

def home(request):
    feedback_form=FeedbackForm(request.POST or None)
    if feedback_form.is_valid():
        name=feedback_form.cleaned_data.get('name')
        email=feedback_form.cleaned_data.get('email')
        contact=feedback_form.cleaned_data.get('contact')
        message=feedback_form.cleaned_data.get('message')

        subject='Feedback'
        from_email=email
        to_email=settings.EMAIL_HOST_USER
        your_message="%s : Feedback message is (%s) via %s and contact is (%s)"%(name, message, email,contact)
        send_mail(
        subject,
        your_message,
        from_email,
        [to_email,],
        fail_silently=False
        )
        feedback_form.save()
        messages.success(request, 'Thank you for your feedback!')
        return redirect("/")

    return render(request,"base.html",{"feedback_form":feedback_form})

def register(request,*args,**kwargs):
    if (request.user.is_authenticated and request.user.is_admin or request.user.is_superadmin):
        form=UserCreationForm(request.POST or None)

        if form.is_valid():
            name=form.cleaned_data.get('name')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            subject='User Password'
            from_email=settings.EMAIL_HOST_USER
            to_email= email
            your_message="%s : Your Password is (%s) via %s"%(name, password, email)
            send_mail(
            subject,
            your_message,
            from_email,
            [to_email,],
            fail_silently=False
            )
            form.save()


            latest_id=UserProfile.objects.latest('id')

            if(form.cleaned_data.get("is_doctor")==True):
                doctor=Doctor(user=latest_id)
                doctor.save()

            elif(form.cleaned_data.get("is_admin")==True):
                adm=Admin(user=latest_id)
                adm.save()

            elif(form.cleaned_data.get("is_lab")==True):
                lab=Lab(user=latest_id)
                lab.save()

            elif (form.cleaned_data.get("is_cashier")==True):
                cash=Cashier(user=latest_id)
                cash.save()

            elif (form.cleaned_data.get("is_medical")==True):
                med=Medical(user=latest_id)
                med.save()
            elif (form.cleaned_data.get('is_receptionist')==True):
                recep=Receptionist(user=latest_id)
                recep.save()

            messages.success(request, 'New user has been registered successfully!')
            return redirect("register")

    else:
        return render(request,"cantaccess.html")
    return render(request,'register.html',{"form":form})


@login_required(login_url='/login/')
def profile(request,id=None):
    if request.user.is_doctor:
        return render(request,'doctor_dashboard.html')

    elif request.user.is_admin or request.user.is_superadmin:
        ash=UserProfile.objects.all()
        context={
        "ash":ash
        }
        return render(request,'admin_dashboard.html',context)

    elif request.user.is_lab:
        user=Lab.objects.get(user_id=request.user.id)
        return render(request,'lab_dashboard.html')

    elif request.user.is_medical:
        # user=Medical.objects.get(user_id=request.user.id)
        return render(request,'medical_dashboard.html')

    elif request.user.is_cashier:
        user=Cashier.objects.get(user_id=request.user.id)
        return render(request,'cashier_dashboard.html')

    elif request.user.is_receptionist:
        user=Receptionist.objects.get(user_id=request.user.id)
        pats=Patient.objects.all()
        return render(request,'receptionist_dashboard.html',{"pats":pats})

    else:
        return render (request,"cantaccess.html")


@login_required(login_url='/login/')
def admin_details(request,id):
    if request.user.is_admin or request.user.is_superadmin:

        details=Admin.objects.get(id=id)

        return render(request,'admin_details.html',{'details':details})

@login_required(login_url='/login/')
def doctor_details(request,id):
    if request.user.is_admin or request.user.is_superadmin:

        details=Doctor.objects.get(id=id)

        return render(request,'doctor_details.html',{'details':details})

@login_required(login_url='/login/')
def medical_details(request,id):
    if request.user.is_admin or request.user.is_superadmin:

        details=Medical.objects.get(id=id)

        return render(request,'medical_details.html',{'details':details})

@login_required(login_url='/login/')
def lab_details(request,id):
    if request.user.is_admin or request.user.is_superadmin:

        details=Lab.objects.get(id=id)

        return render(request,'lab_details.html',{'details':details})

@login_required(login_url='/login/')
def receptionist_details(request,id):
    if request.user.is_admin or request.user.is_superadmin:

        details=Receptionist.objects.get(id=id)

        return render(request,'receptionist_details.html',{'details':details})

@login_required(login_url='/login/')
def user_details(request,id):
    if request.user.is_admin or request.user.is_superadmin:
        details=UserProfile.objects.get(id=id)

        return render(request,'user_details.html',{'details':details})


def doctor_list(request,*args,**kwargs):
    if (request.user.is_admin or request.user.is_superadmin and request.user.is_authenticated):

        doc=UserProfile.objects.filter(is_doctor=True)
        docs=Doctor.objects.all()
        context={

        "ab":zip(docs,doc)
        }
        return render(request,"doctor_list.html",context)
    else:
        return render (request,"cantaccess.html")


def medical_list(request,*args,**kwargs):
    if (request.user.is_admin or request.user.is_superadmin and request.user.is_authenticated):
        med=UserProfile.objects.filter(is_medical=True)
        meds=Medical.objects.all()
        context={
        "ab":zip(meds,med)
        }
        return render(request,"medical_list.html",context)
    else:
        return render (request,"cantaccess.html")

def lab_list(request,*args,**kwargs):
    if (request.user.is_admin or request.user.is_superadmin and request.user.is_authenticated):

        lab=UserProfile.objects.filter(is_lab=True)
        labs=Lab.objects.all()
        context={
       "ab":zip(labs,lab)
        }
        return render(request,"lab_list.html",context)
    else:
        return render (request,"cantaccess.html")

def cashier_list(request,*args,**kwargs):
    if (request.user.is_admin or request.user.is_superadmin and request.user.is_authenticated):
        cash=UserProfile.objects.filter(is_cashier=True)
        cashs=Cashier.objects.all()
        context={
        "ab":zip(cashs,cash)
        }
        return render(request,"cashier_list.html",context)
    else:
        return render (request,"cantaccess.html")

@login_required(login_url='/login/')
def patient_list(request,*args,**kwargs):
    if (request.user.is_admin or request.user.is_doctor or request.user.is_superadmin):
        pats=Patient.objects.all()
        context={

        "pats":pats
        }
        return render(request,"patient_list.html",context)
    else:
        return render (request,"cantaccess.html")

def receptionist_list(request,*args,**kwargs):
    if (request.user.is_admin or request.user.is_superadmin and request.user.is_authenticated):
        recep=UserProfile.objects.filter(is_receptionist=True)
        receps=Receptionist.objects.all()
        context={
        "ab":zip(receps,recep)
        }
        return render(request,"receptionist_list.html",context)
    else:
        return render (request,"cantaccess.html")



def admin_list(request,*args,**kwargs):
    if (request.user.is_admin or request.user.is_superadmin and request.user.is_authenticated):

        admin=UserProfile.objects.filter(is_admin=True)
        print(admin)
        admins=Admin.objects.all()
        print(admins)
        context={

        "ab":zip(admins,admin)
        }
        return render(request,"admin_list.html",context)
    else:
        return render (request,"cantaccess.html")

def user_login(request,*args,**kwargs):
    form=UserLoginForm(request.POST or None)
    messages.warning(request, 'Login form is only for Hospital staff')
    if form.is_valid():
        # username_=form.cleaned_data.get('name')
        # user_obj=User.objects.get(name__iexact=username_)
        emailaddress_=form.cleaned_data.get('email')
        user_obj2=User.objects.get(email__iexact=emailaddress_)
        # login(request,user_obj)
        login(request,user_obj2,backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect("/")
    else:
        return render (request,'login.html',{"form":form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def updateadmin(request):
    if request.user.is_admin:
        admin=UserProfile.objects.get(id=request.user.id)
        adminss=Admin.objects.get(user=admin.id)
        print(adminss.image)
        form=AdminForm(request.POST or None,request.FILES or None,instance=adminss)
        form2=AdminUpdateForm(request.POST or None,request.FILES or None,instance=admin)
        if form.is_valid () and form2.is_valid():
            form.save()
            form2.save()
            return redirect('profile')
        context={
            'x':adminss,
            'form':form,
            'form2':form2,
            }
        return render(request,'updateadmin.html',context)

@login_required(login_url='/login/')
def updateadmin_pass(request):
    if request.user.is_admin:
        admin=UserProfile.objects.get(id=request.user.id)
        adminss=Admin.objects.get(user=admin.id)
        print(adminss.image)
        form=UserChangeForm(request.POST or None,request.FILES or None,instance=admin)
        if form.is_valid ():
            form.save()
            return redirect('profile')
        context={
            'x':adminss,
            'form':form,
            }
        return render(request,'updateadmin_pass.html',context)


@login_required(login_url='/login/')
def delete_users(request,id):
    if request.user.is_admin or not request.user.id==id or request.user.is_superadmin:
    	try:
            user=UserProfile.objects.get(id=id)
            user.delete()
            messages.success(request, 'User has been deleted successfully!')
            return redirect('profile')

    	except:
    		return redirect('profile')
    return render(request,'cantaccess.html')


def admin_search(request):
    if request.method=="POST":
        srch=request.POST['srh']
        if srch:
            match=UserProfile.objects.filter(Q(name__iexact=srch)|
			                             Q(id__iexact=srch))

            if match:
                return render(request,'admin_search.html',{'sr':match})
            else:
                messages.error(request,'no result found')
        else:
            return HttpResponseRedirect('search')
    return render(request,'admin_search.html')


@login_required(login_url='/login/')
def updatedoctor(request):
    if request.user.is_doctor:
        doc=UserProfile.objects.get(id=request.user.id)
        docs=Doctor.objects.get(user=doc.id)
        print(docs.image)
        form=DoctorForm(request.POST or None,request.FILES or None,instance=docs)
        form2=DoctorUpdateForm(request.POST or None,request.FILES or None,instance=doc)
        if form.is_valid () and form2.is_valid():
            form.save()
            form2.save()
            return redirect('profile')
        context={
            'x':docs,
            'form':form,
            'form2':form2,
            }
        return render(request,'updatedoctor.html',context)

@login_required(login_url='/login/')
def updatedoctor_pass(request):
    if request.user.is_doctor:
        doc=UserProfile.objects.get(id=request.user.id)
        docs=Doctor.objects.get(user=doc.id)
        print(docs.image)
        form=UserChangeForm(request.POST or None,request.FILES or None,instance=doc)
        if form.is_valid ():
            form.save()
            return redirect('profile')
        context={
            'x':docs,
            'form':form,
            }
        return render(request,'updatedoctor_pass.html',context)

@login_required(login_url='/login/')
def doc_patient_search(request):
    if request.method=="POST":
        srch=request.POST.get('srh')

        if srch:
            match=Patient.objects.filter(Q(name__iexact=srch)|
			                             Q(id__iexact=srch))


            if match:
                return render(request,'doc_patient_search.html',{'sr':match})

            else:
                messages.error(request,'no result found')
        else:
            return HttpResponseRedirect('search')
    return render(request,'doc_patient_search.html')


@login_required(login_url='/login/')
def gen_doc_form(request,id):
    if request.user.is_doctor:
        pats=Patient.objects.get(id=id)

        return render(request,'gen_doc_form.html',{'pats':pats})


@login_required(login_url='/login/')
def doc_med_form(request,id):
    if request.user.is_doctor:
        form=Doctor_Patient_Med_Form(request.POST or None,request.FILES or None)
        doc=UserProfile.objects.get(id=request.user.id)
        docs=Doctor.objects.get(user=doc.id)
        pats=Patient.objects.get(id=id)

        if form.is_valid():
            value=form.save(commit=False)
            value.patient_id=id
            value.doctor_id=docs.id
            value.save()
            return redirect('doc_med_form',id=id)

        return render(request,'doc_med_form.html',{"form":form,'pats':pats})


@login_required(login_url='/login/')
def doc_check_pats_list(request):
    if request.user.is_doctor:
        doc=UserProfile.objects.get(id=request.user.id)
        docs=Doctor.objects.get(user=doc.id)
        doct=Doctor_Patient_Med.objects.filter(doctor=docs)

        context={
        'doct':doct,
        }
        return render(request,'doc_check_pats_list.html',context)


@login_required(login_url='/login/')
def doc_check_lab_pats_list(request):
    if request.user.is_doctor:
        doc=UserProfile.objects.get(id=request.user.id)
        docs=Doctor.objects.get(user=doc.id)
        doct1=Doctor_Patient_Lab.objects.filter(doctor=docs)

        context={
        'doct1':doct1
        }

        return render(request,'doc_check_lab_pats_list.html',context)


@login_required(login_url='/login/')
def doc_lab_test(request,id):
    if request.user.is_doctor:
        form=Doctor_Patient_Lab_Form(request.POST or None,request.FILES or None)
        pats=Patient.objects.get(id=id)
        doc=UserProfile.objects.get(id=request.user.id)
        docs=Doctor.objects.get(user=doc.id)

        if form.is_valid():
            value=form.save(commit=False)
            value.patient_id=id
            value.doctor_id=docs.id
            value.save()
            return redirect('profile')

        return render(request,'doc_lab_test.html',{"form":form,'pats':pats})


@login_required(login_url='/login/')
def updatelab(request):
    if request.user.is_lab:
        lab=UserProfile.objects.get(id=request.user.id)
        labs=Lab.objects.get(user=lab.id)
        print(labs.image)
        form=LabForm(request.POST or None,request.FILES or None,instance=labs)
        form2=LabUpdateForm(request.POST or None,request.FILES or None,instance=lab)
        if form.is_valid () and form2.is_valid():
            form.save()
            form2.save()
            return redirect('profile')
        context={
            'x':labs,
            'form':form,
            'form2':form2,
            }
        return render(request,'updatelab.html',context)
    else:
        return render(request,'cantaccess.html')



@login_required(login_url='/login/')
def updatelab_pass(request):
    if request.user.is_lab:
        lab=UserProfile.objects.get(id=request.user.id)
        labs=Lab.objects.get(user=lab.id)
        form=UserChangeForm(request.POST or None,request.FILES or None,instance=lab)
        if form.is_valid ():
            form.save()

            return redirect('profile')
        context={
            'x':labs,
            'form':form,

            }
        return render(request,'updatelab_pass.html',context)


@login_required(login_url='/login/')
def lab_patient_search(request):
    if request.method=="POST":
        srch=request.POST.get('srh')

        if srch:
            match=Patient.objects.filter(Q(name__iexact=srch)|
			                             Q(id__iexact=srch))


            if match:
                return render(request,'lab_patient_search.html',{'sr':match})

            else:
                messages.error(request,'no result found')
        else:
            return HttpResponseRedirect('search')
    return render(request,'lab_patient_search.html')


@login_required(login_url='/login/')
def gen_lab_form(request,id):
    if request.user.is_lab:
        pats=Patient.objects.get(id=id)

        return render(request,'gen_lab_form.html',{'pats':pats})



@login_required(login_url='/login/')
def lab_test_result(request,id):
    if request.user.is_lab:
        form=Lab_Test_Result_Form(request.POST or None,request.FILES or None)
        lab=UserProfile.objects.get(id=request.user.id)
        labs=Lab.objects.get(user=lab.id)
        pats=Patient.objects.get(id=id)
        tests=Doctor_Patient_Lab.objects.filter(patient=id)

        if form.is_valid():
            value=form.save(commit=False)
            value.patient_id=id
            value.lab_id=labs.id
            value.save()
            return redirect('profile')

        return render(request,'lab_test_result_form.html',{"form":form,'pats':pats,'tests':tests})

@login_required(login_url='/login/')
def lab_test_bill(request,id):
    if request.user.is_lab:
        form=Lab_Test_Bill_Form(request.POST or None,request.FILES or None)
        lab=UserProfile.objects.get(id=request.user.id)
        labs=Lab.objects.get(user=lab.id)
        pats=Patient.objects.get(id=id)
        tests=Doctor_Patient_Lab.objects.filter(patient=id)

        if form.is_valid():
            value=form.save(commit=False)
            value.patient_id=id
            value.lab_id=labs.id
            value.save()
            return redirect('lab_bill_pdf',id=id)

        return render(request,'lab_test_bill_form.html',{"form":form,'pats':pats,'tests':tests})



@login_required(login_url='/login/')
def lab_check_pats_list(request):
    if request.user.is_lab:
        lab=UserProfile.objects.get(id=request.user.id).lab
        labt=Lab_Test.objects.filter(lab=lab)

        context={
        'labt':labt
        }
        return render(request,'lab_check_pats_list.html',context)

@login_required(login_url='/login/')
def lab_check_pats_bill_list(request):
    if request.user.is_lab:
        lab=UserProfile.objects.get(id=request.user.id).lab
        labt=Lab_Test_Bill.objects.filter(lab=lab)
        print(labt)

        context={
        'labt':labt
        }
        return render(request,'lab_check_pats_bill_list.html',context)


@login_required(login_url='/login/')
def updatemedical(request):
    if request.user.is_medical:
        med=UserProfile.objects.get(id=request.user.id)
        meds=Medical.objects.get(user=med.id)
        print(meds.image)
        form=MedicalForm(request.POST or None,request.FILES or None,instance=meds)
        form2=MedicalUpdateForm(request.POST or None,request.FILES or None,instance=med)


        if form.is_valid () and form2.is_valid():
            form.save()
            form2.save()
            return redirect('profile')
        context={
            'x':meds,
            'form':form,
            'form2':form2,
            }
        return render(request,'updatemedical.html',context)

@login_required(login_url='/login/')
def updatemedical_pass(request):
    if request.user.is_medical:
        med=UserProfile.objects.get(id=request.user.id)
        meds=Medical.objects.get(user=med.id)
        print(meds.image)
        form=UserChangeForm(request.POST or None,request.FILES or None,instance=med)
        if form.is_valid ():
            form.save()
            return redirect('profile')
        context={
            'x':meds,
            'form':form,
            }
        return render(request,'updatemedical_pass.html',context)


@login_required(login_url='/login/')
def medical_patient_search(request):
    if request.method=="POST":
        srch=request.POST.get('srh')

        if srch:
            match=Patient.objects.filter(Q(name__iexact=srch)|
			                             Q(id__iexact=srch))


            if match:
                return render(request,'medical_patient_search.html',{'sr':match})

            else:
                messages.error(request,'no result found')
        else:
            return HttpResponseRedirect('search')
    return render(request,'medical_patient_search.html')


@login_required(login_url='/login/')
def medicines(request,id):
    if request.user.is_medical:
        form=Medical_Meds_Forms(request.POST or None, request.FILES or None)
        pats=Patient.objects.get(id=id)
        med=UserProfile.objects.get(id=request.user.id)
        meds=Medical.objects.get(user=med.id)

        doc=UserProfile.objects.filter(is_doctor=True)
        docs=Doctor.objects.get(user=doc)
        doc1=Doctor_Patient_Med.objects.filter(patient=id)#.filter(date=date.today())
        doc_med=Doctor_Patient_Med.objects.filter(patient=id)

        doc2=doc1.count()
        print(doc2)


        if form.is_valid():
            value=form.save(commit=False)
            value.patient_id=id
            value.medical_id=meds.id
            value.save()
            return redirect('pdf',id=id)

            # if request.POST.get('id') is not None:
            #     tags = form.cleaned_data['medicines'].split(' ')
                # a=Medical_Meds.objects.get(id=request.POST.get('id'))
                # a.is_purchased=True
                # a.amount=request.POST.get('amount')
                # a.save()

        return render(request,'medicines_form.html',{"form":form,'pats':pats,'doc1':doc1,'doc_med':doc_med})#'medical':medical,'all_med':all_medicine})

@login_required(login_url='/login/')
def meds_check_pats_list(request):
    if request.user.is_medical:
        med=UserProfile.objects.get(id=request.user.id)
        meds=Medical.objects.get(user=med.id)
        medit=Medical_Meds.objects.filter(medical_id=meds.id).order_by('-p_date')
        print(medit)

        context={
        'medit':medit
        }
        return render(request,'meds_check_pats_list.html',context)
    else:
        return render(request,'cantaccess.html')

@login_required(login_url='/login/')
def meds_bill(request,id):
    if request.user.is_medical:
        pats=Patient.objects.get(id=id)
        medit=Medical_Meds.objects.filter(patient_id=pats.id)
        context={
        'pats':pats,
        'medit':medit
        }
        pdf=render_to_pdf('meds_bill.html',context)

    return render(request,'cantaccess.html')

def pdf(request,id):
    pats=Patient.objects.get(id=id)
    doc1=Doctor_Patient_Med.objects.filter(patient=id)
    medit=Medical_Meds.objects.filter(patient_id=id).last()

    print(medit)

    context={
    'pats':pats,
    'medit':medit,
    'doc1':doc1,
    }
    pdf=render_to_pdf('meds_bill.html',context)
    if pdf:
        return HttpResponse(pdf,content_type='application/pdf')
    return HttpResponse('Not Found')


def lab_result_pdf(request,id):
    labt=Lab_Test.objects.get(patient_id=id)
    context={
    'labt':labt,
    }
    # html=template.render(context)
    pdf=render_to_pdf('lab_result_report.html',context)
    if pdf:
        return HttpResponse(pdf,content_type='application/pdf')
    return HttpResponse('Not Found')


def lab_report_download(request):
    if request.user.is_authenticated or not request.user.is_authenticated:
        queryset=Patient.objects.all()
        query=request.GET.get('q')

        if query:
            queryset=queryset.filter(Q(id__iexact=query)).distinct()
            pats=get_object_or_404(Patient,id=query)
            labt=Lab_Test.objects.filter(patient_id=pats.id)
            context_dict={
            'pats':pats,
            'labt':labt,
            }
            return render(request,'lab_report_download.html',context_dict)

    return render(request,'lab_report_download.html')



def lab_bill_pdf(request,id):
    # template=get_template('meds_bill.html')
    # form=Medical_Meds_Forms(request.POST or None,request.FILES or None,instance=pats.id)
    pats=Patient.objects.get(id=id)
    labt=Lab_Test_Bill.objects.filter(patient_id=id).last()
    print(labt)

    context={
    'labt':labt,
    'pats':pats

    # 'form':form
    }
    # html=template.render(context)
    pdf=render_to_pdf('lab_bill.html',context)
    if pdf:
        return HttpResponse(pdf,content_type='application/pdf')
    return HttpResponse('Not Found')


@login_required(login_url='/login/')
def createEvent(request):
    if request.method == "POST":
        medicines = request.POST.get('medicines','').split(',')
        amount = request.POST.get('amount','').split(',')

        Medical_Meds.objects.create(
        medicines=medicines,
        amount=amount
        )
        return HttpResponse('')



@login_required(login_url='/login/')
def updatereceptionist(request):
    if request.user.is_receptionist:
        recep=UserProfile.objects.get(id=request.user.id)
        receps=Receptionist.objects.get(user=recep.id)
        print(receps.image)
        form=ReceptionistForm(request.POST or None,request.FILES or None,instance=receps)
        form2=ReceptionistUpdateForm(request.POST or None,request.FILES or None,instance=recep)
        if form.is_valid () and form2.is_valid():
            form.save()
            form2.save()
            return redirect('profile')
        context={
            'x':receps,
            'form':form,
            'form2':form2,
            }
        return render(request,'updatereceptionist.html',context)

@login_required(login_url='/login/')
def updatereceptionist_pass(request):
    if request.user.is_receptionist:
        recep=UserProfile.objects.get(id=request.user.id)
        receps=Receptionist.objects.get(user=recep.id)
        print(receps.image)
        form=UserChangeForm(request.POST or None,request.FILES or None,instance=recep)
        if form.is_valid ():
            form.save()
            return redirect('profile')
        context={
            'x':receps,
            'form':form,
            }
        return render(request,'updatereceptionist_pass.html',context)

@login_required(login_url='/login/')
def recep_patient_form(request):
    if request.user.is_receptionist:
        form=PatientForm(request.POST or None,request.FILES or None,instance=None)
        recep=UserProfile.objects.get(id=request.user.id)
        receps=Receptionist.objects.get(user=recep.id)

        if form.is_valid():
            value=form.save(commit=False)
            value.receptionist_id=receps.id
            value.save()
            messages.success(request, 'New patient has been added successfully!')
            return redirect("recep_patient_form")

        return render(request,'recep_patient_form.html',{'form':form})

def recep_patient_update_form(request):
    if request.user.is_receptionist:
        queryset=Patient.objects.all()
        query=request.GET.get('q')

        if query:
            queryset=queryset.filter(Q(id__iexact=query)).distinct()
            pats=get_object_or_404(Patient,id=query)
            form=PatientForm(request.POST or None,request.FILES or None,instance=pats)
            if form.is_valid():
                print(form)
                form.save()
                return redirect('profile')
            context_dict={
            'pats':pats,
            'form':form,
            }
            return render(request,'recep_patient_update_form.html',context_dict)

    return render(request,'cantaccess.html')


def appointment(request):

    if not request.user.is_authenticated or request.user.is_authenticated():
        appointment=AppointmentForm(request.POST or None,request.FILES or None)

        appointment.preffered_time = datetime.datetime.now()
        print(appointment.preffered_time)

        appointment.end_time =appointment.preffered_time + datetime.timedelta(hours=1)
        print(appointment.end_time)

        time_slot__range=(appointment.preffered_time,appointment.end_time)
        print(time_slot__range)

        if appointment.is_valid():
            appointment.save()
            messages.success(request, 'Your Appointment Time Has Been Reserved')
            return redirect("appointment")

        # elif ((appointment.preffered_time in time_slot__range) and  appointment.is_valid):
        #     return render(request,"staffcant.html")

        return render(request,'appointment.html',{'appointment':appointment})

    else:
        return render(request,'cantaccess.html')


def pathology(request):
    return render (request,'services/pathology.html')

def radiology(request):
    return render (request,'services/radiology.html')

def urology(request):
    return render (request,'services/urology.html')

def plastic_surgery(request):
    return render (request,'services/plastic_surgery.html')

def specialities(request):
    return render (request,'services/specialities.html')


def hospital_overview(request):
    return render (request,'hospital_overview.html')


def activate_user_view(request,code=None,*args,**kwargs):
    if code:
        act_profile_qs=ActivationProfile.ojects.filter(key=code)
        if act_profile_qs.exists() and act_profile_qs.count() == 1:
            act_obj=act_profile_qs.first()
            if not act_obj.expired:
                user_obj=act_obj.user
                user_obj.is_active=True
                user_obj.save()
                user_obj.expired= True
                act_obj.save()
                return HttpResponseRedirect("/login")

    return HttpResponseRedirect("/login")
