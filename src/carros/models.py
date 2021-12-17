from django.db import models

# Create your models here.
# to create an object (instance of class) through the python shell:
# python manage.py shell
# from carros.models import Carro
# Carro.objects.all() -> returns query with all objects
# Carro.objects.create(param1 = xyz, param2 = xzy...) --> Create new object with values filled (in this case, title, description, price..)

class Carr(models.Model):
	Marca = models.TextField(default = 'null')
	Modelo = models.TextField(default = 'null')
	Motor = models.TextField(default = 'null')
	Ano = models.TextField(default = 'null')
	Cambio = models.TextField(default = 'null')
	Combustivel = models.TextField(default = 'null')
	Km = models.TextField(default = 'null')
	Preco = models.TextField(default = 'null')
	Img_url = models.TextField(default = 'null')
	User = models.TextField(default = 'null')