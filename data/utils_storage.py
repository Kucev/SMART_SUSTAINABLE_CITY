import boto3
import config
import requests
def load_image_on_yandex_storage(name,img_url):
    session = boto3.session.Session(region_name=config.OBGECT_STORAGE_REGION,
                                    aws_secret_access_key=config.OBGECT_STORAGE_REGION_ACCES_KEY,
                                    aws_access_key_id=config.OBGECT_STORAGE_KEY_ID)
    s3 = session.client(service_name='s3',endpoint_url='https://storage.yandexcloud.net')
    response = requests.get(img_url)
    s3.put_object(Bucket='storageimpressivebot', Key='human_in_the_loop/' + str(name) + '.jpg', Body=response.content, StorageClass='COLD')
    return "https://storage.yandexcloud.net/storageimpressivebot/human_in_the_loop/" + str(name) + '.jpg'