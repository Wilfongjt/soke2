# soke-web
> Soke-web is search tool that provides an example of how to call serverless functions from a nuxtjs website.

### Features
* Search for one or more keywords
* Search looks for keywords across multiple sources
* Search returns a sentence that contains a keyword
* Search returns a single sentence per keyword per source
* Shows source name as a title
* Shows sentence as a description
* Shows keyword(s) in bold in the description

### Definitions
* Sentence is a list of space delimited words
* Sentence is part of an item
* Keyword is a word for which to search
* Source refers to the document or website from which the a sentence was acquired

## DEV Build Setup

``` bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
$ npm start

# generate static project
$ npm run generate
```

For detailed explanation on how things work, checkout [Nuxt.js docs](https://nuxtjs.org).

## DEV Prerequisites
* setup aws dynamodb in your aws account
* setup aws gateway api in your aws account

## DEV Environment Variables
* Replace <aws-host-name> with your amazon host name from your gateway.
```
deprecated AWS SOKE={"get":"https://<aws-host-name>.execute-api.us-east-2.amazonaws.com/dev/documents/keywords"}

INDEX=https://dev-api.lyttlebit.com/index
APIKEY=<aws-api-key>
```

## Docker-Compose
### DEV Build Container
Build when you first download the repo.
Build when or if you change the docker-compose.yml
Build when or if you change the Dockerfile
```
cd soke/
docker-compose build
```

### DEV Start Container
```
cd soke/
docker-compose up
```

## DEV Website
Use Chrome or Firefox
* http://localhost:3000


## Common Issues
* Safari
  * DONT USE SAFARI it has issues with AWS
  * Preflight response is not successful
  * XMLHttpRequest cannot load ... due to access control checks
  * Failed to load resource: Preflight response is not successful
