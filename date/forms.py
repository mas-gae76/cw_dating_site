from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Электронная почта', error_messages={'invalid': 'Неверный формат email!'})
    first_name = forms.CharField(max_length=40, label='Имя')
    last_name = forms.CharField(max_length=40, label='Фамилия')
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата рождения')
    gender = forms.ChoiceField(choices=User.Gender.choices, label='Пол')
    avatar = forms.ImageField(label='Фото', required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль', error_messages={
        'invalid': 'Пароль должен быть не менее 8 символов и не содержать только цифры'}
                                )
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'birthday', 'gender', 'avatar', 'password1', 'password2')

    def clean_password2(self):
        cd  = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!\r\n Попытайтесь снова')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует!')
        return cd['email']
