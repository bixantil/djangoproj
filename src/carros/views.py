from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Carr

from .forms import CarroForm, LoginForm, RegisterForm

def register_view(request):
	form = RegisterForm(request.POST or None)
	username = request.POST.get('username')
	email = request.POST.get('email')
	password = request.POST.get('password')
	print(username, password, email)

	flag = 0
	try:
		user = User.objects.get(username = username)
	except:
		flag = 1

	if flag == 0:
		print('usuario ja existe')
		return redirect('/login')

	try:
		user = User.objects.create_user(username = username, email = email, password = password)
		user = authenticate(request, username = user)
	except Exception as e:
		print(e)
		print('couldnt register user')
		user = None

	return render(request, "new-users.html", {})

def logout_view(request):
	logout(request)
	return redirect('/login')

def login_view(request):
	print(request.POST)
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		qs = User.objects.filter(username__iexact=username)
		if not qs.exists():
			print("este é um usuário invalido")

		user = authenticate(request, username = username, password=password)
		if user != None:
			login(request, user)
			return redirect('/vender')
		else:
			print('user doesnt exist')
			return redirect('/login_existe')
	else:
		return render(request, "login.html", {})

def login_existe(request):
	print(request.POST)
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		qs = User.objects.filter(username__iexact=username)
		if not qs.exists():
			print("este é um usuário invalido")

		user = authenticate(request, username = username, password=password)
		if user != None:
			login(request, user)
			return redirect('/vender')
		else:
			print('user doesnt exist')
			return redirect('/login_existe')
	else:
		return render(request, "login_existe.html", {})

def all_cars(request, *args, **kwargs):
	all_obj = Carr.objects.all()
	return render(request, "all_cars.html", {'my_list': all_obj})

@login_required
def user_cars(request):
	u_id = request.user.id
	objs = Carr.objects.filter(User = f'{u_id}')
	return render(request, "user_cars.html", {'my_list': objs})

@login_required
def vender(request):
	#print(request.POST)
	if request.method == 'POST' and request.FILES['upload']:
		print(request.POST)
		print(request.user.id)
		username_id = request.user.id
		upload = request.FILES['upload']
		fss = FileSystemStorage()
		file = fss.save(upload.name, upload)
		file_url = fss.url(file)
		Carr.objects.create(Marca = request.POST.get('Marca'),
							Modelo = request.POST.get('Modelo'),
							Motor = request.POST.get('Motor'),
							Ano = request.POST.get('Ano'),
							Cambio = request.POST.get('Cambio'),
							Combustivel = request.POST.get('Combustivel'),
							Km = request.POST.get('Km'),
							Preco = request.POST.get('Preco'),
							Img_url = file_url,
							User = username_id
							)

		return redirect(f"""/carro/{Carr.objects.latest('id').id}""")
	else:
		return render(request, 'vender.html', {})

def new_user(request):
	return render(request, 'new-users.html', {})

def carro_detail_view(request, id):
	obj = get_object_or_404(Carr, id = id)
	context = {
		'Marca': obj.Marca,
		'Modelo': obj.Modelo,
		'Motor': obj.Motor,
		'Ano': obj.Ano,
		'Cambio': obj.Cambio,
		'Combustivel': obj.Combustivel,
		'Km': obj.Km,
		'Img_url': obj.Img_url,
		'Preco': obj.Preco		
	}
	return render(request, "carro_detail_view.html", context)

@login_required
def carro_user_edit_view(request, id):
	u_id = request.user.id
	query_set = Carr.objects.filter(User = f'{u_id}')
	ids_found = []
	for car in query_set:
		car_id = car.id
		ids_found.append(car_id)
	if id in ids_found:	

		obj = get_object_or_404(Carr, id = id)
		context = {
			'ID': obj.id,
			'Marca': obj.Marca,
			'Modelo': obj.Modelo,
			'Motor': obj.Motor,
			'Ano': obj.Ano,
			'Cambio': obj.Cambio,
			'Combustivel': obj.Combustivel,
			'Km': obj.Km,
			'Img_url': obj.Img_url,
			'Preco': obj.Preco
		}
		return render(request, "carro_user_edit_view.html", context)
	else:
		return redirect('/home')

@login_required
def deletar(request, id):
	u_id = request.user.id
	query_set = Carr.objects.filter(User = f'{u_id}')

	ids_found = []
	for car in query_set:
		car_id = car.id
		ids_found.append(car_id)

	if id in ids_found:	
		if request.POST.get('deletar') == 'DELETAR':
			Carr.objects.filter(id=id).delete()
			return redirect('/home')
	else:
		return redirect('/home')

	return render(request, 'deletar.html', {})

@login_required
def editar(request, id):

	u_id = request.user.id
	query_set = Carr.objects.filter(User = f'{u_id}')

	ids_found = []
	for car in query_set:
		car_id = car.id
		ids_found.append(car_id)

	# if id in ids_found:
	if request.method == 'POST' and request.FILES['upload']:
		if id in ids_found:
			username_id = request.user.id
			upload = request.FILES['upload']
			fss = FileSystemStorage()
			file = fss.save(upload.name, upload)
			file_url = fss.url(file)
			Carr.objects.filter(id=id).delete()
			Carr.objects.create(Marca = request.POST.get('Marca'),
								Modelo = request.POST.get('Modelo'),
								Motor = request.POST.get('Motor'),
								Ano = request.POST.get('Ano'),
								Cambio = request.POST.get('Cambio'),
								Combustivel = request.POST.get('Combustivel'),
								Km = request.POST.get('Km'),
								Preco = request.POST.get('Preco'),
								Img_url = file_url,
								User = username_id
								)

		return redirect(f"""/carro/{Carr.objects.latest('id').id}""")
	else:
		return render(request, 'editar.html', {})


