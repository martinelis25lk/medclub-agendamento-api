<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const agendamentos = ref([])
const carregando = ref(true)
const erro = ref('')

async function carregarAgendamentos() {
  carregando.value = true
  erro.value = ''
  try {
    const { data } = await api.get('/agendamentos/')
    agendamentos.value = data.sort((a, b) => {
      const da = `${a.horario_atendimento_detalhes.data} ${a.horario_atendimento_detalhes.horario}`
      const db = `${b.horario_atendimento_detalhes.data} ${b.horario_atendimento_detalhes.horario}`
      return da.localeCompare(db)
    })
  } catch (e) {
    erro.value = 'Não foi possível carregar seus agendamentos.'
  } finally {
    carregando.value = false
  }
}

onMounted(carregarAgendamentos)
</script>

<template>
  <div class="container">
    <h1>Meus agendamentos</h1>
    <p style="color: var(--color-muted); margin-bottom: 2rem;">Consultas que você já reservou.</p>

    <p v-if="carregando" style="color: var(--color-muted);">Carregando...</p>
    <p v-else-if="erro" class="error-text">{{ erro }}</p>
    <p v-else-if="!agendamentos.length" style="color: var(--color-muted);">Você ainda não tem agendamentos.</p>

    <div style="display:flex; flex-direction:column; gap:1rem;">
      <div
        v-for="ag in agendamentos"
        :key="ag.id"
        class="card"
        style="display:flex; justify-content:space-between; align-items:center;"
      >
        <div>
          <h3 style="margin-bottom:0.15rem;">{{ ag.horario_atendimento_detalhes.especialista_nome }}</h3>
          <span style="color: var(--color-muted); font-size:0.9rem;">
            {{ ag.horario_atendimento_detalhes.data }} às {{ ag.horario_atendimento_detalhes.horario }}
          </span>
        </div>
        <span class="badge">Reservado</span>
      </div>
    </div>
  </div>
</template>