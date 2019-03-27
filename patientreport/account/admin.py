from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm,UserCreationForm
from .models import UserProfile,ActivationProfile,Patient,Doctor,Department,Lab,Medical,Cashier,Receptionist,Admin,Doctor_Patient_Lab,Doctor_Patient_Med,Lab_Test,Appointment,Medical_Meds,Feedback,Department
from .import models


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name','email', 'is_admin','is_active','is_lab','is_doctor','is_cashier','is_receptionist','is_medical')
    list_filter = ('is_admin','is_lab','is_active','is_doctor','is_medical','is_cashier','is_receptionist')
    fieldsets = (
        (None, {'fields': ('name','email', 'password')}),
        ('Permissions', {'fields': ('is_admin','is_active','is_doctor','is_lab','is_receptionist','is_cashier','is_medical')}),
        ('Access', {'fields': ('is_active',)}),

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','email','password1', 'password2','is_admin','is_active','is_doctor','is_lab','is_receptionist','is_cashier','is_medical')}
        ),
    )
    search_fields = ('email','name',)
    ordering = ('email','name',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(UserProfile, UserAdmin)
admin.site.register(ActivationProfile)
admin.site.register(Lab)
admin.site.register(Cashier)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Medical)
admin.site.register(Department)
admin.site.register(Receptionist)
admin.site.register(Admin)
admin.site.register(Doctor_Patient_Lab)
admin.site.register(Doctor_Patient_Med)
admin.site.register(Medical_Meds)
admin.site.register(Lab_Test)
admin.site.register(Appointment)
admin.site.register(Feedback)







# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


# Register your models here.
