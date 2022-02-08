# client

## Prerequisites
[Node.js](https://nodejs.org/en/). You can follow [the instruction](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-20-04) to install it on Ubuntu.

## Development
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```
Open http://localhost:8080 to see the web app.

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## Deployment
```
npm run build
```
And then copy the content of dist to S3 bucket `manage.vanityart.com bucket`.
