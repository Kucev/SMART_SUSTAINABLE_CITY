import config
import requests

headers = {'Authorization':'OAuth %s'%config.TOLOKA_OAUTH_TOKEN,'Content-Type':'application/JSON'}
url_create_tasks = config.TOLOKA_DOMAIN + 'tasks?allow_defaults=true&open_pool=true'

def create_json_for_tasks(im):
    return list(map(lambda x: {"input_values":{"image":x['url_storage']},"pool_id":config.TOLOKA_POOL_ID,'overlap':5},im))