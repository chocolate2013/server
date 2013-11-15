from server.models import *
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from server.serializers import *
from rest_framework import generics, permissions, authentication, renderers
from server.permissions import IsOwnerOrReadOnly, IsOwner, IsAdminOrWriteOnly
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from django.http import HttpResponse
from server.models import *
from django.contrib.auth.models import User
from rest_framework.views import APIView

@api_view(('GET',))
def deslogar(request, format=None):
	logout(request)
	return Response({"logoff": 1})



class CriaListaUsuario(APIView):
	authentication_classes = (authentication.TokenAuthentication,)

	def get(self, request, format=None):
		if request.user.is_staff:
			usuarios = [UsuarioSerializer(user).data for user in User.objects.all()]
			return Response(usuarios)
		return HttpResponse(status=403)

	def post(self, request, format=None):
		print request.DATA
		novo_user = User.objects.create_user(username=request.DATA["username"], password=request.DATA["password"], first_name=request.DATA["nome"])
		login(novo_user)
		return HttpResponse(status=200)

class PerfilUsuario(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UsuarioSerializer
	permission_classes = (IsOwnerOrReadOnly,)
	authentication_classes = (authentication.TokenAuthentication,)
	lookup_field = 'username'

	def pre_save(self, obj):
		obj.usuario = self.request.user

class ListaNotificacoes(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = NotificacaoSerializer
	permission_classes = (IsOwner,)
	authentication_classes = (authentication.TokenAuthentication,)
	lookup_field = 'username'

	def pre_save(self, obj):
		obj.usuario = self.request.user

class LugarInfo(generics.RetrieveUpdateDestroyAPIView):
	queryset = Lugar.objects.all()
	serializer_class = LugarSerializer
	permission_classes = (IsOwnerOrReadOnly,)
	authentication_classes = (authentication.TokenAuthentication,)

	def pre_save(self, obj):
		obj.usuario = self.request.user

class ListaLugar(generics.ListCreateAPIView):
	queryset = Lugar.objects.all()
	serializer_class = LugarSerializer
	authentication_classes = (authentication.TokenAuthentication,)

	def pre_save(self, obj):
		obj.usuario = self.request.user

class ComentarioInfo(generics.ListCreateAPIView):
	queryset = Comentario.objects.all()
	serializer_class = NotificacaoSerializer
	permission_classes = (IsOwner,)
	authentication_classes = (authentication.TokenAuthentication,)
	lookup_field = 'lugar'

	def pre_save(self, obj):
		obj.usuario = self.request.user

class BuscaLugar(APIView):
	authentication_classes = (authentication.TokenAuthentication,)

	def post(self, request, format=None):
		if request.DATA.contains_key("coordenada"):
			lat = float(request.DATA["coordenada"]["lat"])
			lon = float(request.DATA["coordenada"]["lon"])
			queryset = Lugar.objects.filter()
		else if request.DATA.contains_key("nome"):
			queryset = Lugar.objects.filter()
		else if request.DATA.contains_key("tag"):
			queryset = Lugar.objects.filter(tag=request.DATA["tag"])

		return Response(queryset)

# @api_view(('POST',))
# @authentication_classes((authentication.TokenAuthentication,))
# def buscaLugar(request, format=None):
# 	# if request.DATA.contains_key('coordenada'):
# 	# 	queryset = Lugar.objects.filter()
# 	# else if request.DATA.contains_key('nome'):
# 	# 	queryset = Lugar.objects.filter()
# 	# else if request.DATA.contains_key('tag'):
# 	# 	queryset = Lugar.objects.filter()
# 	# else
# 	# 	return HttpResponse(status=400)

# 	return HttpResponse(status=200)
