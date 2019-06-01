import config
import dialogs
import utils_db

import time
import numpy as np

from vk_api.longpoll import VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import vk_api


vk_session = vk_api.VkApi(token=config.TOKEN_VK)
vk = vk_session.get_api()
vk_session_error_send_bot=vk_api.VkApi(token=config.TOKEN_VK_ERROR_SEND_BOT)
vk_error_bot = vk_session_error_send_bot.get_api()

def get_url_img_from_attachments(event):
    url = 0
    if list(event.attachments.values()).count('photo') == 1 and len(event.attachments) == 2:
        msg = vk.messages.getById(message_ids=event.message_id)
        sizes_img = msg['items'][0]['attachments'][0]['photo']['sizes']
        url = sizes_img[np.array(list(map(lambda x: x['width']*x['height'],sizes_img ))).argmax()]['url']
    elif event.attachments == {'fwd': '0_0'}:
        msg = vk.messages.getById(message_ids=event.message_id)
        #if fwd only 1, have only 1 attachments, and it is photo
        if len(msg['items'][0]['fwd_messages']) == 1 and len(msg['items'][0]['fwd_messages'][0]['attachments']) == 1\
            and msg['items'][0]['fwd_messages'][0]['attachments'][0]['type'] == 'photo':
            sizes_img = msg['items'][0]['fwd_messages'][0]['attachments'][0]['photo']['sizes']
            url = sizes_img[np.array(list(map(lambda x: x['width']*x['height'],sizes_img ))).argmax()]['url']
        #if reply_message only 1, have only 1 attachments, and it is photo
        elif msg['items'][0]['fwd_messages'] == [] and 'reply_message' in msg['items'][0] and \
                        len(msg['items'][0]['reply_message']['attachments']) == 1 and \
                        msg['items'][0]['reply_message']['attachments'][0]['type'] == 'photo':
            sizes_img = msg['items'][0]['reply_message']['attachments'][0]['photo']['sizes']
            url = sizes_img[np.array(list(map(lambda x: x['width']*x['height'],sizes_img ))).argmax()]['url']
    return url

def send_msg(user_id,msg):
    vk.messages.send(user_id=user_id,random_id=get_random_id(),message=msg, dont_parse_links = 1)

def send_me_error(name,caught_exception):
    vk_error_bot.messages.send(user_id=23107592,random_id=get_random_id(), message=name + str(caught_exception))

def msg_to_bot(event):
    return event.type == VkEventType.MESSAGE_NEW and event.to_me

def get_user_info_by_id(user_id):
    return vk.users.get(user_id=user_id,fields = 'sex,bdate')[0]

def send_start_msg(user_id):
    vk.messages.send(user_id=user_id,random_id=get_random_id(), message=dialogs.start_msg(user_id))
    
def image_processing(user_id,url_img):
    image_id = int('{:0<17}'.format(str(time.time()).replace('.','')))
    utils_db.add_img_to_db(user_id,image_id,url_img)
    send_msg(user_id,"Запускаю нейронную сеть! Через минут я скажку какие показания на счетчике!")