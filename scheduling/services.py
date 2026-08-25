from datetime import datetime, timedelta
from .models import HorarioAtendimento

def gerar_horarios_para_agenda(agenda):
    hoje = datetime.now().date()
    dias_a_frente = 30 # Gera horários para o próximo mês
    
    for i in range(dias_a_frente):
        data_atual = hoje + timedelta(days=i)
        
        # 0 = Segunda, 1 = Terça... (bate com o model)
        if data_atual.weekday() == agenda.dia_semana:
            inicio = datetime.combine(data_atual, agenda.horario_inicio)
            fim = datetime.combine(data_atual, agenda.horario_fim)
            
            vagas = agenda.vagas_totais_dia
            if vagas <= 0:
                continue
                
            duracao_total = (fim - inicio).total_seconds()
            intervalo_segundos = duracao_total / (vagas - 1) if vagas > 1 else 0
                
            for v in range(vagas):
                if v == 0:
                    horario_slot = inicio.time()
                elif v == vagas - 1:
                    horario_slot = fim.time()
                else:
                    segundos_deslocados = int(intervalo_segundos * v)
                    horario_slot = (inicio + timedelta(seconds=segundos_deslocados)).time()
                
                HorarioAtendimento.objects.get_or_create(
                    agenda=agenda,
                    especialista=agenda.especialista,
                    data=data_atual,
                    horario=horario_slot,
                    defaults={'status': 'disponivel'}
                )
