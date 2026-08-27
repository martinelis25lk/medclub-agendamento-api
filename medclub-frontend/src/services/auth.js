import { ref } from 'vue'

export const isLoggedIn = ref(!!localStorage.getItem('access_token'))

export function setAuth(access, refresh) {
  localStorage.setItem('access_token', access)
  localStorage.setItem('refresh_token', refresh)
  isLoggedIn.value = true
}

export function clearAuth() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  isLoggedIn.value = false
}