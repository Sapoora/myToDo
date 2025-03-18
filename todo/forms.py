from django import forms

class UserNameForm(forms.Form):
    user = forms.CharField(label='Enter your ID', max_length=50)

