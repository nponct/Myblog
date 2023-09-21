from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.migrations.state import get_related_models_tuples
from .models import ArtPost,Comment
from django.utils.translation import gettext_lazy as _

class AddPostForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['cat'].empty_label="Категория не выбрана"

    class Meta:
        model=ArtPost
        fields=['title','author','slug','content','cat']
        widgets={
        'title': forms.TextInput(attrs={'class':'form-input'}),
        'author': forms.TextInput(attrs={'class':'form-input'}),
        'content':forms.Textarea(attrs={'cols':60,'rows':10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title



class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ['content', 'parent']
        labels = {
            'content': _(''),
        }
        widgets = {
            'content': forms.TextInput(),
        }
class SearchForm(forms.Form):
    q=forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder':'Поиск'}
        )
    )

class  RegisterUserForm(UserCreationForm):
    username=forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class ': 'form-input'}))
    password1=forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class ': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class ': 'form-input'}))
    class Meta:
        model=User
        fields={'username','email','password1','password2'}
        widgets={
            'username':forms.TextInput(attrs={'class':'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'})
        }

class  LoginUserForm(AuthenticationForm):
    username=forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-input'}))
    password=forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class ': 'form-input'}))

