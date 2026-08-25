from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import time, date, timedelta
from .models import Especialista, Agenda, HorarioAtendimento, Agendamento

class RegraDeNegocioTests(TestCase):
    def setUp(self):
        # 1. Criamos um especialista base para os testes
        self.especialista = Especialista.objects.create(
            nome="Dr. Gregory House",
            especialidade="Diagnóstico",
            registro_conselho="CRM-12345"
        )
        
        # Encontramos a próxima segunda-feira (dia_semana = 0) para o teste
        hoje = date.today()
        dias_para_segunda = (0 - hoje.weekday()) % 7
        self.proxima_segunda = hoje + timedelta(days=dias_para_segunda)

    def test_geracao_automatica_de_horarios(self):
        """Valida se a agenda gera os slots igualmente distribuídos"""
        # Criamos uma agenda de 2 horas (08:00 às 10:00) com 3 vagas
        agenda = Agenda.objects.create(
            especialista=self.especialista,
            dia_semana=0, # Segunda-feira
            horario_inicio=time(8, 0),
            horario_fim=time(10, 0),
            vagas_totais_dia=3
        )
        
        # Filtramos os horários gerados para a próxima segunda-feira
        horarios = HorarioAtendimento.objects.filter(
            agenda=agenda, 
            data=self.proxima_segunda
        ).order_by('horario')
        
        # Esperamos 3 horários gerados
        self.assertEqual(horarios.count(), 3)
        
        # A distribuição de 3 vagas em 2 horas deve ser: 08:00, 09:00 e 10:00
        self.assertEqual(horarios[0].horario, time(8, 0))
        self.assertEqual(horarios[1].horario, time(9, 0))
        self.assertEqual(horarios[2].horario, time(10, 0))
        
        # Todos devem nascer como 'disponivel'
        self.assertEqual(horarios[0].status, 'disponivel')

    def test_prevencao_agendamento_duplicado(self):
        """Valida a reserva do slot e impede agendamento duplo"""
        # Criamos agenda simples com 1 vaga
        agenda = Agenda.objects.create(
            especialista=self.especialista,
            dia_semana=0,
            horario_inicio=time(14, 0),
            horario_fim=time(14, 30),
            vagas_totais_dia=1
        )
        
        # Pegamos o primeiro slot gerado
        slot = HorarioAtendimento.objects.filter(agenda=agenda).first()
        self.assertEqual(slot.status, 'disponivel')
        
        # 1. Fazemos o primeiro agendamento
        agendamento1 = Agendamento(
            cliente_nome="Paciente 1",
            cliente_email="pac1@teste.com",
            horario_atendimento=slot
        )
        agendamento1.save()
        
        # Verificamos se o slot atualizou o status para 'reservado'
        slot.refresh_from_db()
        self.assertEqual(slot.status, 'reservado')
        
        # 2. Tentamos fazer um segundo agendamento no MESMO slot
        agendamento2 = Agendamento(
            cliente_nome="Paciente 2",
            cliente_email="pac2@teste.com",
            horario_atendimento=slot
        )
        
        # O sistema DEVE levantar um erro de validação (ValidationError)
        with self.assertRaises(ValidationError):
            agendamento2.save()