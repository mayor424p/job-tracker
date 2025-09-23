from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import jobApplication, interviewLog

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}
    ))

    class Meta :
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'

        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'password'

        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'confirm password'

        })
        

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model =  jobApplication
        fields = ['company', 'role', 'status', 'source', 'date_applied', 'notes']
        widgets = {
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'date_applied': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'source': forms.Select(attrs={'class': 'form-select' }),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class InterviewForm(forms.ModelForm):
    class Meta:
        model = interviewLog
        fields = ['interview_date', 'interviewer', 'mode', 'notes']
        widgets = {
           'interview_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'interviewer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter interviewer'}),
            'mode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Online / In-person'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Add notes...'}),
        }



class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'id': 'id_username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'id_password'
        })
    )