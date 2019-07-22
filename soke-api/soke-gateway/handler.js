'use strict';
const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
/* Welcome to Serverless!
 * Generated from write_handler_starter.sh
 * See serverless.yml for configuration
*/
module.exports.index = async (event) => {
  // return list of words with link to documents
  // need to remove duplicate words
  let keywords = event.queryStringParameters && event.queryStringParameters.keywords;
  let vals = []; // list of keywords
  // let param = {};
  let param_list = [];
  let data = [];

  let headers = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type,Accept-Langauge",
      "Access-Control-Allow-Methods": "OPTIONS,GET"
  };

  if (keywords === undefined || keywords === null) {
    data = {
       "Items": []
     };
    return {
      statusCode: 200,
      headers: headers,
      body: JSON.stringify({param_list, data})
    };
  }

  vals = keywords.split(" ");

  if(vals.length === 0){
    return {
      statusCode: 200,
      headers: headers,
      body: JSON.stringify({ param_list, data }) };
  }

  let i = 0;
  /*
   prepare a search for each word
  */
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

  // run all the searches
  const plst = [];

  try {
    for(i=0; i < param_list.length; i++){
      plst.push(docClient.query(param_list[i]).promise());
    }
  } catch(error){
    return {statusCode: 400, body: error};
  }

  // wait for the searches to end
  try {
    const results = await Promise.all(plst);

    return {
      statusCode: 200,
      headers: headers,
      body: JSON.stringify({results}),
      isBase64Encoded: false
    };
  } catch(error){
    return {statusCode: 400, body: error};
  }

};

module.exports.document = async (event) => {
  /*
  returns all items for a document by pk
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
