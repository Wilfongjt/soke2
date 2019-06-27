# soke-web

> Soke-web provides an example of how to call serverless functions from a nuxtjs website.

## Build Setup

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

# Prerequisites
* setup aws dynamodb
* setup aws gateway api 

# Environment Variables
```
AWSSOKE={"get":"https://<aws-id>.execute-api.us-east-2.amazonaws.com/dev/documents/keywords"}
```

# Docker-Compose
## Build Container
```
cd soke/
docker-compose build 
```

## Start Container
```
cd soke/
docker-compose up
```

## Launch Website
* http://localhost:3000

# Dynamodb
```
{
    "documents": [
        {
            "AttributeDefinitions": [
                {
                    "AttributeName": "pk",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "sk",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "data",
                    "AttributeType": "S"
                }
            ],
            "TableName": "documents",
            "KeySchema": [
                {
                    "AttributeName": "pk",
                    "KeyType": "HASH"
                },
                {
                    "AttributeName": "sk",
                    "KeyType": "RANGE"
                }
            ],
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            },
            "GlobalSecondaryIndexes": [
                {
                    "IndexName": "gsi_1",
                    "KeySchema": [
                        {
                            "AttributeName": "sk",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "data",
                            "KeyType": "RANGE"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            ]
        }
    ]
}   
```
