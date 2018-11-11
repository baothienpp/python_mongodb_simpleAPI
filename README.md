# A simple RESTful interface for MongoDB

## POST ```/config```

This end point accept a non-empty JSON payload and persist this to MongoDB database. An example of payload:
```
{
  "tenant": "acme"
  "integration_type": "flight_information_system"
  "configuration": {
    "username": "user1"
    "password": "12345"
  }
}
```
If there is an existing configuration with the same tenant and integration_type values, the existing document will be update by merging the configuration values.

It return HTTP code 201 if the document is successfully created, or 400 if the there is error while creating document

## GET ```/config?tenant=<tenant>&integration_type=<type>```
 
 This endpoint returns the available document with those keys, and an error response 404 if none is available
