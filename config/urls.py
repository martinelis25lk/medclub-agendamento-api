from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from scheduling.views import EspecialistaViewSet, AgendaViewSet, HorarioAtendimentoViewSet, AgendamentoViewSet

# Importações do Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Medclub Agendamento API",
      default_version='v1',
      description="API para o sistema de agendamento de especialistas.",
      contact=openapi.Contact(email="seu-email@exemplo.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
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
    
    # Rota da Documentação Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]