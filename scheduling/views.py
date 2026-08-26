from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status
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
    permission_classes = [IsInternoOrReadOnly]


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [IsInternoOrReadOnly]


class HorarioAtendimentoViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Somente leitura: os horários nascem da geração automática da Agenda,
    nunca devem ser criados/editados/apagados diretamente pela API.
    """
    queryset = HorarioAtendimento.objects.all().order_by('data', 'horario')
    serializer_class = HorarioAtendimentoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        especialista = self.request.query_params.get('especialista')
        if status_param:
            queryset = queryset.filter(status=status_param)
        if especialista:
            queryset = queryset.filter(especialista_id=especialista)
        return queryset


class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'interno':
            return Agendamento.objects.all()
        return Agendamento.objects.filter(paciente=user)

    def perform_create(self, serializer):
        serializer.save(paciente=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"detail": "Este horário já foi reservado por outro paciente."},
                status=status.HTTP_409_CONFLICT
            )