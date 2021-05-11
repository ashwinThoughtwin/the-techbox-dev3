from django import forms
from .models import Employee,Item,  ItemAssign
from django.forms import DateInput

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name','designation','email','mobile']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = Employee.objects.get(email=email)

        except Employee.DoesNotExist:
            return email
        raise forms.ValidationError('This email is already register.')

    
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['name'].widget.attrs['id'] = 'nameid'

        self.fields['designation'].widget.attrs['class'] = 'form-control p-1'
        self.fields['designation'].widget.attrs['placeholder'] = 'Designation'
        self.fields['designation'].widget.attrs['id'] = 'designationid'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].widget.attrs['id'] = 'emailid'

        self.fields['mobile'].widget.attrs['class'] = 'form-control'
        self.fields['mobile'].widget.attrs['placeholder'] = 'Mobile'
        self.fields['mobile'].widget.attrs['id'] = 'mobileid'

class ItemAdd(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name','status']
    
    def __init__(self, *args, **kwargs):
        super(ItemAdd, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'ItemName'

        self.fields['status'].widget.attrs['class'] = 'form-control float-left'



class AssignItem(forms.ModelForm):
    class Meta:
        model = ItemAssign
        fields = ['assign_to','assign_item']
    
    def __init__(self, *args, **kwargs):
        super(AssignItem, self).__init__(*args, **kwargs)
        self.fields['assign_to'].widget.attrs['class'] = 'form-control'

        self.fields['assign_item'].widget.attrs['class'] = 'form-control'