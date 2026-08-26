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

    def validate(self, data):
        horario_inicio = data.get('horario_inicio', getattr(self.instance, 'horario_inicio', None))
        horario_fim = data.get('horario_fim', getattr(self.instance, 'horario_fim', None))
        if horario_inicio and horario_fim and horario_inicio >= horario_fim:
            raise serializers.ValidationError(
                "O horário de início deve ser anterior ao horário de término."
            )
        return data

class HorarioAtendimentoSerializer(serializers.ModelSerializer):
    especialista_nome = serializers.ReadOnlyField(source='especialista.nome')
    
    class Meta:
        model = HorarioAtendimento
        fields = ['id', 'agenda', 'especialista', 'especialista_nome', 'data', 'horario', 'status']

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'
        read_only_fields = ['paciente']  # pra evitar spoofing,  paciente vem sempre do usuário logado

    
    def validate_horario_atendimento(self, value):
        if value.status == 'reservado':
            raise serializers.ValidationError("Este horário já está reservado e não pode ser agendado.")
        return value