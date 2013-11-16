from django.forms import widgets
from rest_framework import serializers
from server.models import *
from django.contrib.auth.models import User

# serializadores

class UsuarioSerializer(serializers.ModelSerializer):
	nome = serializers.Field(source='first_name')

	class Meta:
		model = User
		fields = ('username', 'nome', 'amigos', 'posicoes')
		depth = 1

class PosicaoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Posicao
		fields = ('id', 'coordenada', 'lugar', 'datahora')

class NotificacaoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notificacao
		fields = ('tipo', 'usuarios', 'datahora', 'lida')

class LugarSerializer(serializers.ModelSerializer):
	tags = serializers.RelatedField(many=True)

	class Meta:
		model = Lugar
		fields = ('id', 'coordenada', 'nome', 'descricao', 'tags', 'comentarios')
		depth = 1

class ComentarioSerializer(serializers.ModelSerializer):
	username = serializers.Field(source='usuario.username')

	class Meta:
		model = Comentario
		fields = ('id', 'username', 'lugar', 'texto', 'datahora')