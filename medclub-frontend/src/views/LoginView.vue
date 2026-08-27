<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const username = ref('')
const password = ref('')
const erro = ref('')
const carregando = ref(false)

async function entrar() {
  erro.value = ''
  carregando.value = true
  try {
    const { data } = await api.post('/auth/token/', {
      username: username.value,
      password: password.value,
    })
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    router.push('/especialistas')
  } catch (e) {
    erro.value = 'Usuário ou senha inválidos.'
  } finally {
    carregando.value = false
  }
}
</script>

<template>
  <div class="container" style="max-width: 400px;">
    <h1>Entrar</h1>
    <p style="color: var(--color-muted); margin-bottom: 2rem;">Acesse sua conta para agendar sua consulta.</p>

    <form @submit.prevent="entrar" style="display:flex; flex-direction:column; gap:1rem;">
      <div>
        <label>Usuário</label>
        <input v-model="username" class="input" required />
      </div>
      <div>
        <label>Senha</label>
        <input v-model="password" type="password" class="input" required />
      </div>
      <p v-if="erro" class="error-text">{{ erro }}</p>
      <button class="btn btn-primary" type="submit" :disabled="carregando">
        {{ carregando ? 'Entrando...' : 'Entrar' }}
      </button>
    </form>

    <p style="margin-top: 1.5rem; text-align:center; color: var(--color-muted);">
      Não tem conta?
      <router-link to="/registrar" style="color: var(--color-primary); font-weight:600;">Cadastre-se</router-link>
    </p>
  </div>
</template>