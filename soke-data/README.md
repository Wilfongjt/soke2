# soke-data


# Prerequistes
* Jupyter Notebook 


* dont let data get into repo

# Jupyter 
```
# 
cd soke\
jupyter-notebook

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






