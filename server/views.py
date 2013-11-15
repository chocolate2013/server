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
import datetime

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
		if "coordenada" in request.DATA:
			lat = float(request.DATA["coordenada"][0])
			lon = float(request.DATA["coordenada"][1])
			ponto = fromstr("POINT({0} {1})".format(lat, lon))
			queryset = Lugar.objects.filter(coordenada__distance_lte=(ponto, 5000))
		elif "nome" in request.DATA:
			queryset = Lugar.objects.filter(nome__icontains=request.DATA["nome"])
		elif "tag" in request.DATA:
			queryset = Lugar.objects.filter(tag__contains=request.DATA["tag"])
		else:
			return Response({"detail": "Incorrect request."})

		return Response(queryset)


class BuscaUsuario(APIView):
	authentication_classes = (authentication.TokenAuthentication,)

	def post(self, request, format=None):
		queryset = User.objects.filter(username__contains=request.DATA["username"])
		return Response(queryset)


class AdicionarAmigo(APIView):
	authentication_classes = (authentication.TokenAuthentication,)

	def post(self, request, format=None):
		user = request.user
		amigos = [amigo.username for amigo in user.amigos]

		if username not in amigos:
			adicionado = User.objects.get(username=username)
			novo_amigo = Amizade(usuario=user, amigo=adicionado, aprovada=false)
			novo_amigo.save()

			notificacao = Notificacao(usuario=adicionado, tipo="A", usuarios=[user], datahora=datetime.datetime, lida=false)
			notificacao.save()
		else:
			outra_pessoa = User.objects.get(username=username)
			amizade = Amizade.objects.get(usuario=user, amigo=outra_pessoa)
			amizade.aprovada = true
			amizade.save()

			amizade_reciproca = Amizade(usuario=outra_pessoa, amigo=user, aprovada=true)
			amizade_reciproca.save()

		return HttpResponse(status=200)