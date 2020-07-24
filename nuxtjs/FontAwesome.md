#### Install FontAwesome core and icons
```
npm install @nuxtjs/fontawesome @fortawesome/free-solid-svg-icons
```
#### Configure
```
modules: [
	nuxtjs/fontawesome'
],
fontawesome: {
	icons: {
		solid: true
	}
}
```
#### Code
```
<font-awesome-icon class="user-logout" v-on:click="logout" :icon="['fas', 'sign-out-alt']"/>
or
<span class="search-icon">
  <font-awesome-icon :icon="['fas', 'search']"/>
</span>
```
