'use strict';
const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
/* Welcome to Serverless!
 * Generated from write_handler_starter.sh
 * See serverless.yml for configuration
*/
module.exports.documents_keywords = async (event) => {
  // need to remove duplicate words
  let keywords = event.queryStringParameters && event.queryStringParameters.keywords;
  let param = {};
  let data = [] ;

  let headers = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type,Accept-Langauge",
      "Access-Control-Allow-Methods": "OPTIONS,GET"
  };

  if (keywords === undefined) {
    data = {
       "Items": []
     };
    return {
      statusCode: 200,
      headers: headers,
      body: JSON.stringify({param, data}) };
  }
  let vals = keywords.split(" ");
  let param_list = [];
  let i = 0;

  for(i = 0; i < vals.length; i++){
    let skv = "%w.1".replace("%w",vals[i]);

    param_list.push({
      TableName: process.env.TABLE_NAME,
      IndexName: "gsi_1",
      KeyConditionExpression: "sk = :sk1",
      ExpressionAttributeValues: {
       ":sk1": skv
      }
    });
  }

  if(vals.length === 0){
    return {
      statusCode: 200,
      headers: headers,
      body: JSON.stringify({ param_list, data }) };
  }

  // load array with promises
  // pass arry to Promise.all()

  try {
    const plst = [];

    for(i=0; i < param_list.length; i++){
      plst.push(docClient.query(param_list[i]).promise());
    }

    const results = await Promise.all(plst);

    return {
      statusCode: 200,
      headers: headers,
      body: JSON.stringify({results}) };

  } catch(error){
    return {statusCode: 400, body: error};
  }
};

module.exports.document_pk = async (event) => {
  /*
  returns all items for a document 
  */
  let msg = 'document';
  let pk = event.pathParameters && event.pathParameters.pk;

  if (pk === undefined) {
    msg = JSON.stringify({message: 'Missing pk {}'.replace('{}',pk)});
    return {
      statusCode: 400,
      body: msg
    };
  }
  var params = {
    ExpressionAttributeValues: {
     ":v1": pk
    },
    KeyConditionExpression: "pk = :v1",
    TableName: process.env.TABLE_NAME
   };
   try {

     const data = await docClient.query(params).promise();

     return { statusCode: 200, body: JSON.stringify({ params, data }) };
   } catch (error){
     return {
       statusCode: 400,
       error: 'Could not post: ${error.stack}'
     };
   }

};
