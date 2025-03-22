from django import forms

class UserNameForm(forms.Form):
    user = forms.CharField(label='Enter your ID', max_length=50)
    password = forms.CharField(label='Enter your password', max_length=50, widget=forms.PasswordInput)

