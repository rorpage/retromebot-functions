# retrobotme OpenFaaS functions

[![OpenFaaS](https://img.shields.io/badge/openfaas-serverless-blue.svg)](https://www.openfaas.com)

This repo contains OpenFaaS functions, using Azure Event Grid for backend messaging, that convert a tweeted 
picture into a black and white one and submit the result back as a Twitter response.

### Read more about OpenFaas:
[OpenFaaS](https://github.com/openfaas/faas)


### Read more about Azure Event Grid:
[Azure Event Grid](https://azure.microsoft.com/en-us/services/event-grid/)

### Notes for deploying your own version

#### Create an env.list file
Be sure to create an env.list file that your OpenFaaS functions can use with the following values:

```
azure_blob_account=your_azure_blob_account_name
azure_blob_account_key=your_azure_blob_account_key
consumer_key=your_twitter_app_consumer_key
consumer_secret=your_twitter_app_consumer_secret
access_token=your_twitter_app_access_token
access_token_secret=your_twitter_app_access_token_secret
```

You can create a Twitter app for your own bot at https://apps.twitter.com/app/new