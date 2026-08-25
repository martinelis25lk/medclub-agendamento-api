from django.db import models
from django.core.exceptions import ValidationError

class Especialista(models.Model):
    nome = models.CharField(max_length=255)
    especialidade = models.CharField(max_length=255)
    registro_conselho = models.CharField(max_length=50, unique=True)  # ex: CRM/CRO

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"


class Agenda(models.Model):
    DIAS_SEMANA = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE, related_name='agendas')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    vagas_totais_dia = models.PositiveIntegerField(help_text="Quantidade de vagas disponíveis por dia")

    def clean(self):
        if self.horario_inicio >= self.horario_fim:
            raise ValidationError("O horário de início deve ser anterior ao horário de término.")

    def __str__(self):
        return f"{self.especialista.nome} - {self.get_dia_semana_display()} ({self.horario_inicio} às {self.horario_fim})"


class HorarioAtendimento(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('reservado', 'Reservado'),
    ]

    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, related_name='horarios')
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE, related_name='horarios')
    data = models.DateField()
    horario = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['especialista', 'data', 'horario'], name='unique_horario_especialista')
        ]

    def __str__(self):
        return f"{self.data} às {self.horario} - {self.especialista.nome} ({self.status})"


class Agendamento(models.Model):
    cliente_nome = models.CharField(max_length=255)
    cliente_email = models.EmailField()
    horario_atendimento = models.OneToOneField(HorarioAtendimento, on_delete=models.CASCADE, related_name='agendamento')
    criado_em = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.horario_atendimento.status == 'reservado':
            raise ValidationError("Este horário já está reservado.")

    def save(self, *args, **kwargs):
        # Garante a regra de negócio: ao agendar, muda o status do slot para reservado
        self.full_clean()
        self.horario_atendimento.status = 'reservado'
        self.horario_atendimento.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Agendamento de {self.cliente_nome} para {self.horario_atendimento}"