from django import forms
from .models import Developer,Building, Apartment, Buyer, Contract, Order, Land
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = ['name', 'contact_info']

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['land_address', 'building_type','house_number', 'real_estate_number', 'floor', 'area_floor']

class LandForm(forms.ModelForm):
    class Meta:
        model = Land
        fields = ['address', 'area','real_estate_number', 'chimoku']


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['building', 'unit_number', 'bedrooms', 'bathrooms']

    building = forms.ModelChoiceField(
        queryset=Building.objects.all(),
        label='Building',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    unit_number = forms.CharField(
        label='Unit Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    bedrooms = forms.IntegerField(
        label='Bedrooms',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    bathrooms = forms.DecimalField(
        label='Bathrooms',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['first_name', 'last_name', 'email', 'phone']

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label='Phone',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['buyer', 'apartment', 'contract_date', 'status']

    # 필요한 경우 폼 필드를 커스터마이징할 수 있습니다.
    buyer = forms.ModelChoiceField(
        queryset=Buyer.objects.all(),
        label='Buyer',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    apartment = forms.ModelChoiceField(
        queryset=Apartment.objects.all(),
        label='Apartment',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    contract_date = forms.DateField(
        label='Contract Date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    status = forms.ChoiceField(
        choices=[('Pending', 'Pending'), ('Completed', 'Completed')],
        label='Status',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class UserRegisterForm(UserCreationForm):
    name = forms.CharField(label='担当者名')
    company_name = forms.CharField(label='会社名')
    phone_number = forms.CharField(label='電話番号')
    fax_number = forms.CharField(label='FAX')
    address = forms.CharField(label='住所')
    housenumber = forms.CharField(label='屋号')
    email = forms.EmailField(label='E-mail')
    name_leader = forms.CharField(label='代表者名')
    department = forms.CharField(label='担当部署')
    company_number = forms.CharField(label='会社法人等番号【登記簿記載】')
    housing_license = forms.CharField(label='不動産免許番号')

    class Meta:
        model = User
        fields = ['name', 'company_name', 'company_number', 'name_leader','department', 'address', 'housenumber','phone_number', 'fax_number', 'email', 'username', 'password1', 'password2', 'housing_license']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'ID'
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード確認'
        self.fields['username'].help_text = 'ご希望のユーザーIDを入力してください。'
        self.fields['password1'].help_text = '安全なパスワードを設定してください。8文字以上で、数字、大文字、小文字を含めることが推奨されます。'
        self.fields['password2'].help_text = '確認のためもう一度パスワードを入力してください。'

class OrderForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=False)  # 읽기 전용 필드
    company_name = forms.CharField(max_length=100, required=False)  # 읽기 전용 필드

    class Meta:
        model = Order
        fields = ['name', 'company_name',  'land_quantity', 'building_quantity','additional_requirements', 'plan', 'expected_contract_date', 'attachment']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].disabled = True  # 사용자 입력을 받지 않음
        self.fields['company_name'].disabled = True  # 사용자 입력을 받지 않음


class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['additional_requirements', 'plan', 'expected_contract_date', 'attachment']

