from django.contrib import admin
from .models import Especialista, Agenda, HorarioAtendimento, Agendamento

admin.site.register(Especialista)
admin.site.register(Agenda)
admin.site.register(HorarioAtendimento)
admin.site.register(Agendamento)