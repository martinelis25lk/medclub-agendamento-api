from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import time, date, timedelta
from django.contrib.auth import get_user_model
from .models import Especialista, Agenda, HorarioAtendimento, Agendamento
from .serializers import AgendamentoSerializer

User = get_user_model()

class RegraDeNegocioTests(TestCase):
    def setUp(self):
        
        self.paciente = User.objects.create_user(
            username="paciente_teste", 
            email="paciente@teste.com", 
            password="senha123",
            role="cliente"
        )

        self.especialista = Especialista.objects.create(
            nome="Dr. Gregory House",
            especialidade="Diagnóstico",
            registro_conselho="CRM-12345"
        )
        
        hoje = date.today()
        dias_para_segunda = (0 - hoje.weekday()) % 7
        self.proxima_segunda = hoje + timedelta(days=dias_para_segunda)

    def test_geracao_automatica_de_horarios(self):
        agenda = Agenda.objects.create(
            especialista=self.especialista,
            dia_semana=0,
            horario_inicio=time(8, 0),
            horario_fim=time(10, 0),
            vagas_totais_dia=3
        )
        
        horarios = HorarioAtendimento.objects.filter(
            agenda=agenda, 
            data=self.proxima_segunda
        ).order_by('horario')
        
        self.assertEqual(horarios.count(), 3)
        self.assertEqual(horarios[0].horario, time(8, 0))
        self.assertEqual(horarios[1].horario, time(9, 0))
        self.assertEqual(horarios[2].horario, time(10, 0))
        self.assertEqual(horarios[0].status, 'disponivel')

    def test_prevencao_agendamento_duplicado(self):
        agenda = Agenda.objects.create(
            especialista=self.especialista,
            dia_semana=0,
            horario_inicio=time(14, 0),
            horario_fim=time(14, 30),
            vagas_totais_dia=1
        )
        
        slot = HorarioAtendimento.objects.filter(agenda=agenda).first()
        
        # 1º Agendamento
        agendamento1 = Agendamento(paciente=self.paciente, horario_atendimento=slot)
        agendamento1.save()
        
        slot.refresh_from_db()
        self.assertEqual(slot.status, 'reservado')
        
        
        agendamento2 = Agendamento(paciente=self.paciente, horario_atendimento=slot)
        with self.assertRaises(ValidationError):
            agendamento2.save()

    def test_serializer_retorna_detalhes_do_horario(self):
        agenda = Agenda.objects.create(
            especialista=self.especialista,
            dia_semana=0,
            horario_inicio=time(11, 0),
            horario_fim=time(11, 30),
            vagas_totais_dia=1
        )

        slot = HorarioAtendimento.objects.filter(agenda=agenda).first()

        agendamento = Agendamento(paciente=self.paciente, horario_atendimento=slot)
        agendamento.save()

        dados = AgendamentoSerializer(agendamento).data

        self.assertIn('horario_atendimento_detalhes', dados)
        self.assertEqual(dados['horario_atendimento_detalhes']['especialista_nome'], self.especialista.nome)
        self.assertEqual(dados['horario_atendimento_detalhes']['status'], 'reservado')