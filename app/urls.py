from importlib.resources import path
from . import views
from django.urls import path

urlpatterns = [ 
    path('',views.main, name='main'),
    path('quest/',views.cadastro,name='quest'),
    path('login/',views.logar,name='login'),
    path('infosAnun/',views.infos_anunciante,name='infos_anunciante'),
    path('infosEmp/',views.infos_empresa,name='infos_empresa'),
    path('anunciar/',views.anunciar,name='anunciar'),
    path('logout/',views.user_logout,name='logout'),
    path('remover/<int:id>/',views.remover_anuncio,name='remover'),
    path('meus_anuncios',views.meus_anuncios,name='meus_anuncios'),
    path('sobre/',views.sobre,name='sobre'),
    path('plastico/',views.plastico,name='plastico'),
    path('vidro/',views.vidro,name='vidro'),
    path('papel/',views.papel,name='papel'),
    path('metal/',views.metal,name='metal'),
    path('organico/',views.organico,name='organico')
]