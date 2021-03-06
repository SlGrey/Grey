from django import forms
from django.utils import timezone
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Логин"
        self.fields["password"].label = "Пароль"

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином не зарегистрирован")
        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError("Неверный пароль")


class RegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password_check",
            "first_name",
            "last_name",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Логин"
        self.fields["password"].label = "Пароль"
        self.fields["password"].help_text = "Введите пароль"
        self.fields["password_check"].label = "Повторите пароль"
        self.fields["first_name"].label = "Ваше имя"
        self.fields["last_name"].label = "Фамилия"
        self.fields["email"].label = "Ваша почта"
        self.fields["email"].help_text = "Пожалуйста укажите реальный адрес"

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        password_check = self.cleaned_data["password_check"]
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином уже зарегистрирован")
        if password != password_check:
            raise forms.ValidationError("Пароли не совпадают!")
        if not first_name:
            raise forms.ValidationError(" Пожалуйста укажите Ваше имя")
        if not last_name:
            raise forms.ValidationError(" Пожалуйста укажите Вашу фамилию")
        if not email:
            raise forms.ValidationError(" Пожалуйста укажите Вашу почту")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email-oм уже зарегистрирован")


class ChangeAccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User

        fields = [
            "username",
            "password",
            "password_check",
            "first_name",
            "last_name",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super(ChangeAccountForm, self).__init__(*args, **kwargs)
        self.current = self.instance
        self.fields["username"].label = "Логин"
        self.fields["password"].label = "Пароль"
        self.fields["password"].help_text = "Введите пароль"
        self.fields["password_check"].label = "Повторите пароль"
        self.fields["first_name"].label = "Ваше имя"
        self.fields["last_name"].label = "Фамилия"
        self.fields["email"].label = "Ваша почта"
        self.fields["email"].help_text = "Пожалуйста укажите реальный адрес"

    def clean(self):
        current_user = str(self.current)
        print(current_user)
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        password_check = self.cleaned_data["password_check"]
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        current_email = User.objects.get(username=current_user).email
        if current_user != username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином уже зарегистрирован")
        if password != password_check:
            raise forms.ValidationError("Пароли не совпадают!")
        if not first_name:
            raise forms.ValidationError("Пожалуйта укжите Ваше имя")
        if not last_name:
            raise forms.ValidationError(" Пожалуйста укажите Вашу фамилию")
        if not email:
            raise forms.ValidationError(" Пожалуйста укажите Вашу почту")
        if current_email != email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email-oм уже зарегистрирован")


class OrderForm(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField(max_length=12)
    buying_type = forms.ChoiceField(
        widget=forms.Select(),
        choices=([("self", "Самовывоз"), ("delivery", "Доставка")]))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = "Имя"
        self.fields["last_name"].label = "Фамилия"
        self.fields["phone"].label = "Номер телефона"
        self.fields["phone"].help_text = "Пожалуйста введите номер в формате: 380ХХХХХХХХХ"
        self.fields["buying_type"].label = "Способ получения"
        self.fields["address"].label = "Адрес доставки"
        self.fields["address"].help_text = "Пожалуйста укажите название перевозчика," \
                                           " населенный пункт и номер отделения"
        self.fields["comments"].label = "Коментарии к заказу"
        self.fields["date"].label = "Дата доставки"
        self.fields["date"].help_text = "Доставка производится на следущий день после заказа"

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        codes = {
            "050",
            "066",
            "095",
            "099",
            "067",
            "068",
            "096",
            "098",
            "063",
            "093",
            "091",
            "092",
            "094",
        }

        if str(phone)[2:5] not in codes or len(phone) != 12:
            raise forms.ValidationError("Был введён некорректный номер телефона")


class ProductFilterForm(forms.Form):
    min_price = forms.IntegerField(label=" Цена  от ", required=False)
    max_price = forms.IntegerField(label=" Цена  до ", required=False)
    choices = [
        ["", " "],
        ["16", "16A"],
        ["20", "20A"],
        ["32", "32A"],
        ["40", "40A"],
        ["50", "50A"],
        ["63", "63A"],
    ]
    min_amp = forms.ChoiceField(label="Сила тока от", required=False, choices=choices)
    max_amp = forms.ChoiceField(label="Сила тока до", required=False, choices=choices)
