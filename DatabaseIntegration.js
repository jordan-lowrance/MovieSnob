module.exports = class DB {};
const AWS = require('aws-sdk');
let documentClient = new AWS.DynamoDB.DocumentClient({
    'region': 'us-west-2'
});

var table = "MovieSpread"

 getMovie(key, value, table) 
     if (!table) throw 'table needed';
     if (typeof key !== 'string') throw `key was not string and was ${JSON.stringify(key)} on table ${table}`;
     if (typeof value !== 'string') throw `value was not string and was ${JSON.stringify(value)} on table ${table}`;
     if (!table) 'table needs to be users, sessions, or routes.'
     return new Promise((resolve, reject) => {
         var params = {
             TableName : table,
             IndexName : `${key}-index`,
             KeyConditionExpression : `${key} = :value`, 
             ExpressionAttributeValues : {
                 ':value' : value 
             }
         };

         documentClient.query(params, function(err, data) {
             if (err) {
                 console.error("Unable to read item. Error JSON:", JSON.stringify(err));
                 reject(err);
             } else {
                 console.log("GetItem succeeded:", JSON.stringify(data.Items));
                 resolve(data.Items);
             }
         });
     })
 




 


