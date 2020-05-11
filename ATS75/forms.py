from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type='date'

class AddScheduleForm(forms.Form):
    start_date=forms.DateField(required=True,widget=DateInput)
    end_date=forms.DateField(required=True,widget=DateInput)
    percentage_criteria=forms.FloatField(required=True)

class AddSubjectForm(forms.Form):
    subject_code=forms.CharField(max_length=10,required=True)
    subject_name=forms.CharField(max_length=50,required=True)
    teacher_name=forms.CharField(max_length=50,required=True)

class SignUpForm(UserCreationForm):
    institution=forms.CharField(max_length=100,required=True)
    first_name=forms.CharField(max_length=30,required=True)
    last_name=forms.CharField(max_length=30,required=True)
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
            'institution',
            'password1',
            'password2',
        )