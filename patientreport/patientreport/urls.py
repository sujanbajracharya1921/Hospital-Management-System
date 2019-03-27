"""patientreport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from account.views import register
from account.views import user_login,home,user_logout,activate_user_view,profile,doctor_list,cashier_list,medical_list,lab_list,patient_list,receptionist_list,updateadmin,admin_list,delete_users,admin_search,updatedoctor,doc_patient_search,gen_doc_form,doc_lab_test,updatelab,lab_test_result,lab_patient_search,updatemedical,medical_patient_search,medicines,updatereceptionist,recep_patient_form,doc_med_form,updatelab_pass,updateadmin_pass,updatedoctor_pass,updatemedical_pass,updatereceptionist_pass,appointment,createEvent,doc_check_pats_list,lab_check_pats_list,meds_check_pats_list,meds_bill,pdf,gen_lab_form,lab_test_bill,lab_check_pats_bill_list,doc_check_lab_pats_list,lab_result_pdf,lab_bill_pdf,lab_report_download,admin_details,receptionist_details,medical_details,lab_details,doctor_details,user_details,recep_patient_update_form,pagination,department,depart_search,doc_search,createEvent2,admin_appointment_list,pathology,radiology,urology,plastic_surgery,specialities,hospital_overview

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


# from django.contrib.auth import views as auth_view



urlpatterns = [
    url(r'^$',home,name="home"),
    url(r'^admin/', admin.site.urls),
    url(r'^register/', register,name="register"),
    url(r'^login/',user_login,name='user_login'),
    url(r'^logout/',user_logout,name="logout"),
    url(r'^activate/(?P<code>[a-z0-9].*)/$',activate_user_view),
    # url(r'^logout/',auth_view.logout,{'next_page':'/patientreport/user_login'},name='logout'),
    url(r'^profile/$',profile,name='profile'),


    url(r'^doctor_list/',doctor_list,name='doctor_list'),
    # url(r'^doctor_details/(?P<id>[0-9]+)',doctor_details,name='doctor_details'),
    url(r'^lab_list/',lab_list,name='lab_list'),
    url(r'^medical_list/',medical_list,name='medical_list'),
    url(r'^cashier_list/',cashier_list,name='cashier_list'),
    url(r'^patient_list/',patient_list,name='patient_list'),
    url(r'^receptionist_list/',receptionist_list,name='receptionist_list'),
    url(r'^user_details/(?P<id>[0-9]+)',user_details,name='user_details'),


    url(r'^updateadmin/',updateadmin,name='updateadmin'),
    url(r'^updateadmin_pass/',updateadmin_pass,name='updateadmin_pass'),
    url(r'^admin_list/',admin_list,name='admin_list'),
    url(r'^admin_details/(?P<id>[0-9]+)',admin_details,name='admin_details'),
    url(r'^profile/(?P<id>[0-9]+)/delete/$',delete_users,name='delete_users'),
    url(r'^admin_search/',admin_search,name='admin_search'),
    url(r'^admin_appointment_list/',admin_appointment_list,name='admin_appointment_list'),


    url(r'^updatedoctor/',updatedoctor,name='updatedoctor'),
    url(r'^updatedoctor_pass/',updatedoctor_pass,name='updatedoctor_pass'),
    url(r'^doc_patient_search/',doc_patient_search,name='doc_patient_search'),
    url(r'^gen_doc_form/(?P<id>[0-9]+)',gen_doc_form,name='gen_doc_form'),
    url(r'^doc_lab_test/(?P<id>[0-9]+)',doc_lab_test,name='doc_lab_test'),
    url(r'^doc_med_form/(?P<id>[0-9]+)',doc_med_form,name='doc_med_form'),
    url(r'^doc_check_pats_list/',doc_check_pats_list,name='doc_check_pats_list'),
    url(r'^doctor_details/(?P<id>[0-9]+)',doctor_details,name='doctor_details'),



    url(r'^updatelab/',updatelab,name='updatelab'),
    url(r'^updatelab_pass/',updatelab_pass,name='updatelab_pass'),
    url(r'^gen_lab_form/(?P<id>[0-9]+)',gen_lab_form,name='gen_lab_form'),
    url(r'^lab_patient_search/',lab_patient_search,name='lab_patient_search'),
    url(r'^lab_test_result/(?P<id>[0-9]+)',lab_test_result,name='lab_test_result'),
    url(r'^lab_test_bill/(?P<id>[0-9]+)',lab_test_bill,name='lab_test_bill'),
    url(r'^lab_check_pats_list/',lab_check_pats_list,name='lab_check_pats_list'),
    url(r'^lab_check_pats_bill_list/',lab_check_pats_bill_list,name='lab_check_pats_bill_list'),
    url(r'^doc_check_lab_pats_list/',doc_check_lab_pats_list,name='doc_check_lab_pats_list'),
    url(r'^lab_result_pdf/(?P<id>[0-9]+)',lab_result_pdf,name='lab_result_pdf'),
    url(r'^lab_bill_pdf/(?P<id>[0-9]+)',lab_bill_pdf,name='lab_bill_pdf'),
    url(r'^lab_report_download/',lab_report_download,name='lab_report_download'),
    url(r'^lab_details/(?P<id>[0-9]+)',lab_details,name='lab_details'),






    url(r'^updatemedical/',updatemedical,name='updatemedical'),
    url(r'^updatemedical_pass/',updatemedical_pass,name='updatemedical_pass'),
    url(r'^medical_patient_search/',medical_patient_search,name='medical_patient_search'),
    url(r'^medical_patient_search/(?P<id>[0-9]+)',medical_patient_search,name='medical_patient_search'),
    url(r'^medicines/(?P<id>[0-9]+)',medicines,name='medicines'),
    url(r'^meds_check_pats_list/',meds_check_pats_list,name='meds_check_pats_list'),
    url(r'^meds_bill/(?P<id>[0-9]+)',meds_bill,name='meds_bill'),
    url(r'^medical_details/(?P<id>[0-9]+)',medical_details,name='medical_details'),





    url(r'^updatereceptionist/',updatereceptionist,name='updatereceptionist'),
    url(r'^updatereceptionist_pass/',updatereceptionist_pass,name='updatereceptionist_pass'),
    url(r'^recep_patient_form/',recep_patient_form,name='recep_patient_form'),
    url(r'^receptionist_details/(?P<id>[0-9]+)',receptionist_details,name='receptionist_details'),
    url(r'^recep_patient_update_form/',recep_patient_update_form,name='recep_patient_update_form'),




    url(r'^appointment/',appointment,name='appointment'),
    url(r'^createEvent/',createEvent,name='createEvent'),
    url(r'^createEvent2/',createEvent2,name='createEvent2'),



    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^pdf/(?P<id>[0-9]+)/$',pdf,name='pdf'),



    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),


    url(r'^pagination/',pagination,name='pagination'),
    url(r'^department/$',department,name='department'),
    url(r'^depart_search/',depart_search,name='depart_search'),
    url(r'^doc_search/',doc_search,name='doc_search'),


    url(r'^pathology/',pathology,name='pathology'),
    url(r'^urology/',urology,name='urology'),
    url(r'^radiology/',radiology,name='radiology'),
    url(r'^plastic_surgery/',plastic_surgery,name='plastic_surgery'),
    url(r'^specialities/',specialities,name='specialities'),
    url(r'^hospital_overview/',hospital_overview,name='hospital_overview'),







]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
