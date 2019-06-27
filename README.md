# soke
search

# Process


# Prerequistes
* AWS account https://aws.amazon.com 

# Useful Tools
* Atom https://atom.io
* Docker https://www.docker.com 
* Nuxtjs https://nuxtjs.org/guide/installation 
* Dotenv https://github.com/nuxt-community/dotenv-module
* Serverless https://serverless.com
* Python

# Development
* I use Atom and Docker for website development
* I use Atom with the Serverless pluggin for AWS Gateway and Lambda development
* I use Python to create dynamodb tables, manipulate documents, and load data



# Website

# Gateway and Lambda

# Database



# Environment Variables
```
AWSSOKE={"get":"https://<aws-id>.execute-api.us-east-2.amazonaws.com/dev/documents/keywords"}
```

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

