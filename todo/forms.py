from django import forms

class UserNameForm(forms.Form):
    username = forms.CharField(label='Enter your ID', max_length=50)

