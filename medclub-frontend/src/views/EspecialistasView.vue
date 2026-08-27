<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const especialistas = ref([])
const carregando = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get('/especialistas/')
    especialistas.value = data
  } finally {
    carregando.value = false
  }
})
</script>

<template>
  <div class="container">
    <h1>Especialistas</h1>
    <p style="color: var(--color-muted); margin-bottom: 2rem;">Escolha um especialista para ver os horários disponíveis.</p>

    <p v-if="carregando" style="color: var(--color-muted);">Carregando...</p>
    <p v-else-if="!especialistas.length" style="color: var(--color-muted);">Nenhum especialista cadastrado ainda.</p>

    <div style="display:flex; flex-direction:column; gap:1rem;">
      <router-link
        v-for="esp in especialistas"
        :key="esp.id"
        :to="`/especialistas/${esp.id}/horarios`"
        class="card"
        style="text-decoration:none; color:inherit; display:flex; justify-content:space-between; align-items:center;"
      >
        <div>
          <h3 style="margin-bottom:0.15rem;">{{ esp.nome }}</h3>
          <span class="badge">{{ esp.especialidade }}</span>
        </div>
        <span style="color: var(--color-primary); font-weight:600;">Ver horários →</span>
      </router-link>
    </div>
  </div>
</template>