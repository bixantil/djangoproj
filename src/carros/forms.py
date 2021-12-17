from django import forms
from django.contrib.auth import get_user_model
from .models import Carr

User = get_user_model()

class RegisterForm(forms.Form):
	username = forms.CharField()
	email = forms.EmailField()
	password1 = forms.CharField(
		widget=forms.PasswordInput(
			attrs = {
				"class":"form-control",
				"id": "user-password"
			}
		)
	)
	password2 = forms.CharField(
		widget=forms.PasswordInput(
			attrs = {
				"class":"form-control",
				"id": "user-password"
			}
		)
	)
	def clean_username(self):
		username = self.cleaned_data.get("username")
		qs = User.objects.filter(username__iexact=username)
		if qs.exists():
			raise forms.ValidationError("este é um usuário invalido")
		return username

	def clean_username(self):
		email = self.cleaned_data.get("email")
		qs = User.objects.filter(email__iexact=email)
		if not qs.exists():
			raise forms.ValidationError("email ja em uso")
		return email			


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs = {
				"class":"form-control",
				"id": "user-password"
			}
		)
	)
	# def clean(self):
	# 	username = self.cleaned_data.get("username")
	# 	password = self.cleaned_data.get("password")

	def clean_username(self):
		username = self.cleaned_data.get("username")
		qs = User.objects.filter(username__iexact=username)
		if not qs.exists():
			raise forms.ValidationError("este é um usuário invalido")
		return username

class CarroForm(forms.ModelForm):
	class Meta:
		model = Carr
		fields = [
			'Marca',
			'Modelo',
			'Motor',
			'Ano',
			'Cambio',
			'Combustivel',
			'Km',
			'Preco',
			'Img_url'
		]