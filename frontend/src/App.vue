<template>
  <h1>Hello {{ firstName }}</h1>
  <h3>{{ homeData ? homeData.details : 'chargement...' }}</h3>
  <p>Compteur: {{ count }}</p>
  <div>
    <button @click="increment">Incrementer</button>
    <button @click="decrement">Decrementer</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const firstName = ref("Marie")

setInterval(() => {
  if (firstName.value === 'Marie') {
    firstName.value = 'Sammy';
  } else {
    firstName.value = 'Marie';
  }
}, 1000);

const count = ref(0)
const increment = (event) => {
  console.log(event)
  count.value++
}

const decrement = () => {
  count.value--
}

const homeData = ref(null)

const fetchdta = async() => {
  try {
    let baseURL = "http://localhost:8000"
    let response = await fetch(`${baseURL}/home`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    if (!response.ok) {
      const text = await response.text()
      throw new Error(`HTTP error! status: ${response.status}, message: ${text}`);
    }
    let data = await response.json()
    console.log(data)
    return data
  } catch (error) {
    console.error("Error fetching data:", error)
  }
};
onMounted(async() => {
  homeData.value = await fetchdta()
})

</script>

<style>
h1 {
  color: rgba(255, 162, 0, 0.66);
}
</style>