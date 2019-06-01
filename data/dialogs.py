import utils
import config
import utils_db

def start_msg(user_id):
    user_info = utils_db.get_sex_and_name(user_id)
    agreement = ['согласнен','согласна','согласен']
    return 'Привет, %s!\n Пришлите мне фотографию своего счетчика. Теперь не нужно вводить показания вручную!'%(user_info['user_name'])

def info():
    return 'Пришли мне фотографию своего счетчика! Теперь не нужно вводить показания вручную!'
