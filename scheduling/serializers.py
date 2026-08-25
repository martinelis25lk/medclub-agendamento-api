from rest_framework import serializers
from .models import Especialista, Agenda, HorarioAtendimento, Agendamento

class EspecialistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialista
        fields = '__all__'

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = '__all__'

class HorarioAtendimentoSerializer(serializers.ModelSerializer):
    especialista_nome = serializers.ReadOnlyField(source='especialista.nome')
    
    class Meta:
        model = HorarioAtendimento
        fields = ['id', 'agenda', 'especialista', 'especialista_nome', 'data', 'horario', 'status']

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'
    
    def validate_horario_atendimento(self, value):
        if value.status == 'reservado':
            raise serializers.ValidationError("Este horário já está reservado e não pode ser agendado.")
        return value