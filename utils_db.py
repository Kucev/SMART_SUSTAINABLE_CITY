import config
import utils 
import psycopg2
import psycopg2.extras
from contextlib import closing
params_db = {'dbname':config.DB_NAME, 'user':config.DB_USER,'password':config.DB_PASSWORD, 
             'host':config.DB_HOST, 'port':config.DB_PORT,'cursor_factory':psycopg2.extras.RealDictCursor}

def user_id_in_db(user_id):
    with closing(psycopg2.connect(**params_db)) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT exists (SELECT 1 FROM users WHERE user_id = %d LIMIT 1)'%user_id)
            return cursor.fetchone()['exists']
        
def add_user_in_db(user_id):
    user_info_from_vk = utils.get_user_info_by_id(user_id)
    dct = {
        'user_id':user_id,
        'user_name':user_info_from_vk['first_name'],
        'user_surname':user_info_from_vk['last_name'],
        'sex': user_info_from_vk['sex']
        }
    with closing(psycopg2.connect(**params_db)) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''insert into 
            users  (user_id, user_name, user_surname, sex)
            values (%(user_id)s, %(user_name)s, %(user_surname)s, %(sex)s)''',dct)
            conn.commit()
            
def get_sex_and_name(user_id):
    with closing(psycopg2.connect(**params_db)) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT user_name,sex FROM users WHERE user_id = %(user_id)s''',{'user_id':user_id})
            return cursor.fetchall()[0]
        
def add_img_to_db(user_id,image_id,url_img):
    dct = {'user_id':user_id,'image_id':image_id,'url_vk':url_img,'status':0}
    with closing(psycopg2.connect(**params_db)) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''insert into images (user_id,image_id,url_vk,status) 
                            values (%(user_id)s, %(image_id)s, %(url_vk)s, %(status)s)''',dct)
            conn.commit()
            
def review_is_now_being_written(user_id):
    with closing(psycopg2.connect(**params_db)) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT exists (SELECT 1 FROM images WHERE user_id = %d AND status <=2 LIMIT 1)'%user_id)
            return cursor.fetchone()['exists']
        
def add_url_storage_in_db(image_id, url_storage):
    with closing(psycopg2.connect(**params_db)) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""UPDATE images SET status = 1, url_storage = %(url_storage)s  WHERE image_id = %(image_id)s""",
                               {'url_storage': url_storage,'image_id':image_id})
            conn.commit()
            
def select_img_to_yandex_storage_upload():
    with closing(psycopg2.connect(**params_db)) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT image_id,url_vk FROM images WHERE status = 0')
            return cursor.fetchall()
        
def select_new_img_to_toloka():
    with closing(psycopg2.connect(**params_db)) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT image_id,url_storage,user_id FROM images WHERE status = 1')
            return cursor.fetchall()
        
def add_toloka_task_id_in_db(image_id, id_toloka_task):
    with closing(psycopg2.connect(**params_db)) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""UPDATE images SET status = 2, id_toloka_task = %(id_toloka_task)s  
                              WHERE image_id = %(image_id)s""", {'id_toloka_task': id_toloka_task,'image_id':image_id})
            conn.commit()
            
def select_reviewing_images():
    with closing(psycopg2.connect(**params_db)) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT image_id,id_toloka_task,user_id,url_storage FROM images WHERE status = 2')
            return cursor.fetchall()
        
def add_review_in_db(image_id, info):
    with closing(psycopg2.connect(**params_db)) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""UPDATE images SET status = 3, info = %(info)s WHERE image_id = %(image_id)s""",
            {'info': info, 'image_id':image_id})
            conn.commit()