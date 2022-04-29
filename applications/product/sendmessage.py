import requests

from applications.telebot.models import TeleSettings

token = '5350539323:AAEDs7_ttU8d84egZTdqsG977AKbXRd36GA'
chat_id = '-566077291'
text = 'admindnq'



def sendTelegram(tg_phone, tg_name):
    settings = TeleSettings.objects.get(pk=1)
    token = str(settings.token)
    chat_id = str(settings.chat)
    text = str(settings.message)
    api = 'https://api.telegram.org/bot'
    method = api + token + '/sendMessage'

    a = text.find('{')
    b = text.find('}')
    c = text.rfind('{')
    d = text.rfind('}')

    part_1 = text[0:a]
    part_2 = text[b+1:c]
    part_3 = text[d:-1]

    text_slise = part_1 + tg_name + part_2 + tg_phone + part_3


    req = requests.post(method, data={
        'chat_id': chat_id,
        'text': text_slise
    })





