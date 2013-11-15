from django.conf.urls import include
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from server import views
from django.contrib import admin
from server.models import *

admin.autodiscover()
admin.site.register(Tag)
admin.site.register(Lugar)
admin.site.register(Posicao)
admin.site.register(Notificacao)
admin.site.register(Comentario)

urlpatterns = patterns('',
	url(r'^l/$', views.ListaLugar.as_view()),
    url(r'^l/(?P<pk>\d+)/$', views.LugarInfo.as_view()),
    url(r'^l/(?P<lugar>\d+)/comentario/$', views.ComentarioInfo.as_view()),
    url(r'^l/busca/$', views.BuscaLugar.as_view()),
    url(r'^u/logout/$', views.deslogar),
    url(r'^u/$', views.CriaListaUsuario.as_view()),
    url(r'^u/(?P<username>.+)/$', views.PerfilUsuario.as_view()),
    url(r'^u/(?P<username>.+)/notificacoes/$', views.ListaNotificacoes.as_view()),
    url(r'^u/(?P<username>\w+)/adicionar/$', views.AdicionarAmigo.as_view()),
    url(r'^u/busca/$', views.BuscaUsuario.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^auth/', 'rest_framework.authtoken.views.obtain_auth_token')
)