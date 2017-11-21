import os, json, tempfile, requests

from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
azure_blob_account = os.environ['azure_blob_account']
azure_blob_account_key = os.environ['azure_blob_account_key']
block_blob_service = BlockBlobService(account_name=azure_blob_account, account_key=azure_blob_account_key)

def handle(json_in):
    loaded_json = json.loads(json_in)[0]

    if loaded_json['eventType'] == 'Microsoft.EventGrid.SubscriptionValidationEvent':
        validation_code = loaded_json['data']['validationCode']
        response = {'validationResponse': validation_code}
        return json.dumps(response)

    filename = loaded_json['subject']
    filename = filename.replace('/blobServices/default/containers/', '')
    container, garbage, blob_name = filename.split('/')

    tempdir = tempfile.gettempdir() + '/'
    file_path = tempdir + blob_name
    block_blob_service.get_blob_to_path(container, blob_name, file_path)

    r = requests.post('http://gateway:8080/function/imagemagick_bw', data=file(file_path, 'rb').read())

    with open(file_path, 'wb') as f:
        f.write(r.content)

    block_blob_service.create_blob_from_path(
        'black-and-white',
        blob_name,
        file_path,
        content_settings=ContentSettings(content_type='image/jpg')
    )

    print("Retroization succeeded for -> " + file_path)
