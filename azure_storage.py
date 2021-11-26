from azure.storage.blob import BlockBlobService

account_name ="xxx"
account_key ="xxx"

copy_from_container="test7"
copy_to_container ="test4"

#remove the wildcard
copy_from_prefix = 'Folder1/FileName_20191104'

def copy_blob_files(account_name, account_key, copy_from_container, copy_to_container, copy_from_prefix):
    try:
        block_blob_service = BlockBlobService(account_name,account_key)
        files = block_blob_service.list_blobs(copy_from_container,copy_from_prefix)
        for file in files:
            block_blob_service.copy_blob(copy_to_container,file.name.replace(copy_from_prefix,""),f"https://{account_name}.blob.core.windows.net/{copy_from_container}/{file.name}")

    except:
        print('could not copy files')

copy_blob_files(account_name,account_key,copy_from_container,copy_to_container,copy_from_prefix)

