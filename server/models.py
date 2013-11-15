from django.contrib.gis.db import models
from django.dispatch import receiver
from django.db.models.signals import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Tag(models.Model):
	tag = models.TextField()

	def __unicode__(self):
		return '%s' % self.tag

class Lugar(models.Model):
	usuario = models.ForeignKey(User, related_name='lugares')
	coordenada = models.PointField()
	nome = models.TextField()
	descricao = models.TextField()
	tags = models.ManyToManyField(Tag, related_name='lugares')
	objects = models.GeoManager()

class Posicao(models.Model):
	usuario = models.ForeignKey(User, related_name='posicoes')
	coordenada = models.PointField()
	lugar = models.ForeignKey(Lugar, related_name='posicao_usuario')
	datahora = models.DateTimeField()
	objects = models.GeoManager()

	class Meta:
		ordering = ('datahora',)

class Notificacao(models.Model):
	usuario = models.ForeignKey(User, related_name='notificacoes')
	tipo = models.TextField()
	usuarios = models.ManyToManyField(User, related_name='envolvido')
	datahora = models.DateTimeField()
	lida = models.BooleanField()

class Comentario(models.Model):
	usuario = models.ForeignKey(User, related_name='comentarios')
	lugar = models.ForeignKey(Lugar, related_name='comentarios')
	texto = models.TextField()
	datahora = models.DateTimeField()

class Amizade(models.Model):
	usuario = models.ForeignKey(User, related_name='amigos')
	amigo = models.ForeignKey(User)
	aprovada = models.BooleanField()