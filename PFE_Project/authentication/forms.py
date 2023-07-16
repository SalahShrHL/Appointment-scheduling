from contextlib import nullcontext
from django import forms
from django.contrib.auth import authenticate,get_user_model

class UserLoginForm(forms.Form):
    email=forms.CharField()
    password=forms.CharField()

    def clean(self,*args,**kwargs):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')

        if email and password:
            user=authenticate(email=email,password=password)

            if not user:
                raise forms.ValidationError('User Does Not Exist')
            
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
        
        return super(UserLoginForm, self).clean(*args,**kwargs)

user=get_user_model()

class UserRegisterForm(forms.ModelForm):
    email=forms.EmailField()
    password=forms.CharField()
    num_tel = forms.CharField(required=False)
    nom_cabinet = forms.CharField(required=False)

    class Meta:
        model=user
        fields=[
            'email',
            'password',
            'last_name',
            'first_name',
            'num_tel',
            'nom_cabinet',
        ]

    def clean(self,*args,**kwargs):
        email=self.cleaned_data.get('email')
        email_qs=user.objects.filter(email=email)
        
        if email_qs.exists():
            raise forms.ValidationError("Emails Already In Use")

        return super(UserRegisterForm, self).clean(*args,**kwargs)