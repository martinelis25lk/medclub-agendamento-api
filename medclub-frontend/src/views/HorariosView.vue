<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const props = defineProps({ id: String })
const router = useRouter()

const horarios = ref([])
const carregando = ref(true)
const agendando = ref(null)
const erro = ref('')

async function carregarHorarios() {
  carregando.value = true
  const { data } = await api.get(`/horarios/?status=disponivel&especialista=${props.id}`)
  horarios.value = data
  carregando.value = false
}

async function agendar(horario) {
  agendando.value = horario.id
  erro.value = ''
  try {
    await api.post('/agendamentos/', { horario_atendimento: horario.id })
    router.push(`/confirmacao/${horario.id}`)
  } catch (e) {
    erro.value = 'Este horário já não está mais disponível.'
  } finally {
    agendando.value = null
  }
}

onMounted(carregarHorarios)
</script>

<template>
  <div class="container">
    <div style="display:flex; gap:0.5rem; align-items:center; margin-bottom:2rem; color: var(--color-muted); font-size:0.85rem;">
      <span class="badge">1. Especialista ✓</span>
      <span>—</span>
      <span class="badge" style="background: var(--color-primary); color:white;">2. Horário</span>
      <span>—</span>
      <span class="badge">3. Confirmação</span>
    </div>

    <h1>Horários disponíveis</h1>
    <p v-if="erro" class="error-text">{{ erro }}</p>

    <p v-if="carregando" style="color: var(--color-muted);">Carregando...</p>
    <p v-else-if="!horarios.length" style="color: var(--color-muted);">Nenhum horário disponível no momento.</p>

    <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap:0.75rem;">
      <div v-for="h in horarios" :key="h.id" class="card" style="text-align:center; padding:1rem;">
        <div style="font-size:0.8rem; color: var(--color-muted);">{{ h.data }}</div>
        <div style="font-family: var(--font-display); font-weight:700; font-size:1.1rem; margin:0.25rem 0 0.75rem;">{{ h.horario }}</div>
        <button
          class="btn btn-primary"
          style="width:100%; padding:0.5rem;"
          :disabled="agendando === h.id"
          @click="agendar(h)"
        >
          {{ agendando === h.id ? '...' : 'Agendar' }}
        </button>
      </div>
    </div>
  </div>
</template>