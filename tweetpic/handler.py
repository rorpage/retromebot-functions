import twitter, os, json, time, tempfile, contextlib, sys, io

from PIL import Image

from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
azure_blob_account = os.environ['azure_blob_account']
azure_blob_account_key = os.environ['azure_blob_account_key']
block_blob_service = BlockBlobService(account_name=azure_blob_account, account_key=azure_blob_account_key)

api = twitter.Api(
    consumer_key=os.environ['consumer_key'],
    consumer_secret=os.environ['consumer_secret'],
    access_token_key=os.environ['access_token'],
    access_token_secret=os.environ['access_token_secret']
)

def handle(json_in):
    loaded_json = json.loads(json_in)[0]

    if loaded_json['eventType'] == 'Microsoft.EventGrid.SubscriptionValidationEvent':
        validation_code = loaded_json['data']['validationCode']
        response = {'validationResponse': validation_code}
        print json.dumps(response)
        return

    filename = loaded_json['subject']
    filename = filename.replace('/blobServices/default/containers/', '')
    container, garbage, blob_name = filename.split('/')

    tempdir = tempfile.gettempdir() + '/'
    file_path = tempdir + blob_name
    block_blob_service.get_blob_to_path('black-and-white', blob_name, file_path)

    in_reply_to_status_id = blob_name.replace('.jpg', '')

    with open(file_path, 'rb') as image:
        size = os.fstat(image.fileno()).st_size
        im = Image.open(file_path)
        if size > 5 * 1048576:
            maxsize = (1028, 1028)
            im.thumbnail(maxsize, Image.ANTIALIAS)
        im = im.convert("RGB")
        im.save(file_path, "JPEG")
        image = open(file_path, 'rb')

        status = api.PostUpdate("I retroified your image using OpenFaaS!",
            media=image,
            auto_populate_reply_metadata=True,
            in_reply_to_status_id=in_reply_to_status_id)
        image.close()
        return {
            "reply_to": in_reply_to_status_id,
            "status_id": status.id
        }