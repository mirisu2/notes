```
apt-get remove nodejs
apt-get autoremove
```
## [Node.js](https://github.com/nodesource/distributions/blob/master/README.md#deb)

### Installation instructions
#### Node.js v14.x:
```
# Using Debian, as root
curl -sL https://deb.nodesource.com/setup_14.x | bash -
apt-get install -y nodejs
```
#### Node.js v12.x:
```
# Using Debian, as root
curl -sL https://deb.nodesource.com/setup_12.x -o nodesource_setup.sh
bash nodesource_setup.sh
apt-get install -y nodejs
```


### Generate nuxtjs app
```
npx create-nuxt-app app_name

 To get started:

        cd app_name
        npm run dev

  To build & start for production:

        cd app_name
        npm run build
        npm run start
```

#### [nuxt.config.js](https://nuxtjs.org/api)
```
export default {
  mode: 'universal',
  server:  {
    port: 8000,
    host: '0.0.0.0'
  },
  loading: false,
  ...
}
```
