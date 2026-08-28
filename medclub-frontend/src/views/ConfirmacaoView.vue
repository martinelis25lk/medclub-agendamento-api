<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const props = defineProps({ id: String })

const horario = ref(null)
const carregando = ref(true)
const erro = ref('')

async function carregarHorario() {
  carregando.value = true
  erro.value = ''
  try {
    const { data } = await api.get(`/horarios/${props.id}/`)
    horario.value = data
  } catch (e) {
    erro.value = 'Não foi possível carregar os dados deste horário.'
  } finally {
    carregando.value = false
  }
}

onMounted(carregarHorario)
</script>

<template>
  <div class="container">
    <div style="display:flex; gap:0.5rem; align-items:center; margin-bottom:2rem; color: var(--color-muted); font-size:0.85rem;">
      <span class="badge">1. Especialista ✓</span>
      <span>—</span>
      <span class="badge">2. Horário ✓</span>
      <span>—</span>
      <span class="badge" style="background: var(--color-primary); color:white;">3. Confirmação</span>
    </div>

    <p v-if="carregando" style="color: var(--color-muted);">Carregando...</p>
    <p v-else-if="erro" class="error-text">{{ erro }}</p>

    <template v-else-if="horario">
      <template v-if="horario.status === 'reservado'">
        <h1>Consulta confirmada!</h1>
        <p style="color: var(--color-muted); margin-bottom: 2rem;">Seu horário foi reservado com sucesso. Os detalhes estão abaixo.</p>
      </template>
      <template v-else>
        <h1>Horário ainda não reservado</h1>
        <p style="color: var(--color-muted); margin-bottom: 2rem;">Este horário consta como disponível. Se você esperava vê-lo reservado, tente agendar novamente.</p>
      </template>

      <div class="card" style="margin-bottom:1.5rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
          <h3 style="margin:0;">{{ horario.especialista_nome }}</h3>
          <span
            class="badge"
            :style="horario.status !== 'reservado' ? 'background: var(--color-border); color: var(--color-muted);' : ''"
          >
            {{ horario.status === 'reservado' ? 'Reservado' : 'Disponível' }}
          </span>
        </div>
        <p style="margin:0; color: var(--color-muted);">Data</p>
        <p style="margin:0 0 0.75rem; font-weight:600;">{{ horario.data }}</p>
        <p style="margin:0; color: var(--color-muted);">Horário</p>
        <p style="margin:0; font-weight:600;">{{ horario.horario }}</p>
      </div>

      <div style="display:flex; gap:0.75rem;">
        <router-link to="/meus-agendamentos" class="btn btn-primary">Ver meus agendamentos</router-link>
        <router-link to="/especialistas" class="btn btn-ghost">Agendar outro horário</router-link>
      </div>
    </template>
  </div>
</template>