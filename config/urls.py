from django.contrib import admin
from django.urls import path, include  # <-- Certifique-se de que 'include' está aqui
from rest_framework.routers import DefaultRouter
from scheduling.views import (
    EspecialistaViewSet, 
    AgendaViewSet, 
    HorarioAtendimentoViewSet, 
    AgendamentoViewSet
)

router = DefaultRouter()
router.register(r'especialistas', EspecialistaViewSet)
router.register(r'agendas', AgendaViewSet)
router.register(r'horarios', HorarioAtendimentoViewSet)
router.register(r'agendamentos', AgendamentoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('accounts.urls')),
]