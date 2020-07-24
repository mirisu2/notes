#### Task: setup variables into nuxt-link
##### My hierarchy of folders:
```
pages/user/settings/_username.vue
```
##### Solution:
```
Nuxt uses vue-router by reading off the vue-router documentation. Open .nuxt/router.js. 
This file contains information about routes
{
    path: "/user/settings/:username?",
    component: _505a7f2d,
    name: "user-settings-username"
  }
```
##### Code:
```
<template>
    <nuxt-link v-bind:to="{ 
        name: 'user-settings-username', 
        params: {username:user.username} 
    }">{{ user.fname }} {{ user.lname }}</nuxt-link>
</template>
<script>
export default {
  computed: {
    user() {
      return this.$auth.user
    }
  }
}
</script>
```


