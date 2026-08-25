from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Especialista, Agenda, HorarioAtendimento, Agendamento
from .serializers import (
    EspecialistaSerializer, 
    AgendaSerializer, 
    HorarioAtendimentoSerializer, 
    AgendamentoSerializer
)
from .permissions import IsInternoOrReadOnly

class EspecialistaViewSet(viewsets.ModelViewSet):
    queryset = Especialista.objects.all()
    serializer_class = EspecialistaSerializer
    permission_classes = [IsInternoOrReadOnly] # Apenas internos modificam, outros apenas leem

class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [IsInternoOrReadOnly] # Apenas internos gerenciam agendas

class HorarioAtendimentoViewSet(viewsets.ModelViewSet):
    queryset = HorarioAtendimento.objects.all().order_by('data', 'horario')
    serializer_class = HorarioAtendimentoSerializer
    permission_classes = [AllowAny] # Listagem pública para pacientes buscarem horários
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        especialista = self.request.query_params.get('especialista')
        if status:
            queryset = queryset.filter(status=status)
        if especialista:
            queryset = queryset.filter(especialista_id=especialista)
        return queryset

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated] # Qualquer usuário autenticado (cliente) pode agendar