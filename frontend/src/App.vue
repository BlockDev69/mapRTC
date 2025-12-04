<template>
  <h1>Hello {{ firstName }}</h1>
  <h3>{{ homeData ? homeData.details : 'chargement...' }}</h3>
  <p>Session state: <strong>{{  status  }}</strong></p>
  <p v-if="userId">UserID: {{ userId }}</p>
  <div>
    <button @click="checkSession" :disabled="!userId">
      Check Session
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
})

const firstName = ref("Marie")

setInterval(() => {
  firstName.value = firstName.value === 'Marie' ? 'Sammy' : 'Marie'
}, 1000)

const homeData = ref(null)

const fetchHomeData = async () => {
  try {
    const response = await api.get('/home')
    console.log(response.data)
    return response.data
  } catch (err) {
    console.error('Error fetching data:', err)
    return null
  }
}

const userId = ref(null)
const status = ref('Not logged in')

const initSession = async () => {
  try {
    const response = await api.post('/session/init')
    userId.value = response.data.user_id
    status.value = response.data.status === 'created' ? 'Session created' : 'Session exists'
    console.log("Session data:", response.data)
  } catch (error) {
    console.error('Error initializing session:', error)
    status.value = 'Error initializing session'
  }
}

const checkSession = async () => {
  try {
    console.log("Cookies:", document.cookie)
    const response = await api.get('/session/me')
    console.log("Session data:", response.data)
    alert(`User ID: ${response.data.user_id}\nAnonymous: ${response.data.is_anonymous}`)
  } catch (error) {
    console.error('Error checking session:', error)
    alert("Session invalid or expired")
  }
}

onMounted(async () => {
  homeData.value = await fetchHomeData()
  await initSession()
})

</script>

<style>
h1 {
  color: rgba(255, 162, 0, 0.66);
}
</style>