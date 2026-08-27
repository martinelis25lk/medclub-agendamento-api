<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const isAuth = () => !!localStorage.getItem('access_token')

function sair() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
}
</script>

<template>
  <header style="border-bottom: 1px solid var(--color-border); background: var(--color-surface);">
    <div class="container" style="display:flex; justify-content:space-between; align-items:center; padding-top:1rem; padding-bottom:1rem;">
      <strong style="font-family: var(--font-display); font-size: 1.25rem; color: var(--color-primary);">
        medclub<span style="color: var(--color-accent);">.</span>
      </strong>
      <button v-if="isAuth()" class="btn btn-ghost" @click="sair">Sair</button>
    </div>
  </header>
  <router-view />
</template>