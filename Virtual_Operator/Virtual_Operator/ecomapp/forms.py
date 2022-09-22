# -*- coding: utf-8 -*-
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным логином не зарегестрирован в системе!')

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль!')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_check',
            'first_name',
            'last_name',
            'email'
        ]


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Придумайте пароль'
        self.fields['password_check'].label = 'Повторите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['email'].label = 'Ваша почта'
        self.fields['email'].help_text = 'Пожалуйста, укажите реальный адрес почтового ящика.'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным логином уже зарегестрирован в системе!')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с данным почтовым адресом уже зарегестрирован в системе!')
        if password != password_check:
            raise forms.ValidationError('Ваши пароли не совпадают! Попробуйте снова!')


class OrderForm(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField()
    third_name = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=([('self', 'В офисе'), ('delivery', 'Доставка')]))
    address = forms.CharField(required=False)
    order_phone = forms.CharField()
    date = forms.DateTimeField(widget=forms.SelectDateWidget(), initial=timezone.now())



    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['third_name'].label = 'Отчество'

        # Т.к. телефон может быть не указан в списках для подключени я услуг
        self.fields['order_phone'].label = 'Телефон для связи'
        self.fields['order_phone'].help_text = 'Пожалуйста, укажите реальный номер телефона, по которому с Вами ' \
                                          'можно связаться.'
        self.fields['buying_type'].label = 'Способ получения'
        self.fields['address'].label = 'Введите польный адрес проживания'
        self.fields['address'].help_text = 'В формате, который прописан в Вашем паспорте.'

        self.fields['date'].label = 'Дата заказа услуги'
        self.fields['date'].help_text = 'Услуга будет подключена в течение дня после заказа.'