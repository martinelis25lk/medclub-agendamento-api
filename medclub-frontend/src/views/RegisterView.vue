<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const username = ref('')
const email = ref('')
const password = ref('')
const erro = ref('')
const carregando = ref(false)

async function cadastrar() {
  erro.value = ''
  carregando.value = true
  try {
    await api.post('/auth/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
    })
    router.push('/login')
  } catch (e) {
    erro.value = 'Não foi possível cadastrar. Verifique os dados.'
  } finally {
    carregando.value = false
  }
}
</script>

<template>
  <div class="container" style="max-width: 400px;">
    <h1>Criar conta</h1>
    <p style="color: var(--color-muted); margin-bottom: 2rem;">Leva menos de um minuto.</p>

    <form @submit.prevent="cadastrar" style="display:flex; flex-direction:column; gap:1rem;">
      <div>
        <label>Usuário</label>
        <input v-model="username" class="input" required />
      </div>
      <div>
        <label>E-mail</label>
        <input v-model="email" type="email" class="input" required />
      </div>
      <div>
        <label>Senha</label>
        <input v-model="password" type="password" class="input" required minlength="6" />
      </div>
      <p v-if="erro" class="error-text">{{ erro }}</p>
      <button class="btn btn-primary" type="submit" :disabled="carregando">
        {{ carregando ? 'Criando...' : 'Criar conta' }}
      </button>
    </form>

    <p style="margin-top: 1.5rem; text-align:center; color: var(--color-muted);">
      Já tem conta?
      <router-link to="/login" style="color: var(--color-primary); font-weight:600;">Entrar</router-link>
    </p>
  </div>
</template>