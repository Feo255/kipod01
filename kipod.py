import json
import requests
import csv
from datetime import datetime



USER = 'fedor.dynga@altezza.org'
PASSWORD = 'changeMe@1'
HOST = "https://tech.kipod.ru/oauth2/v1/auth/authenticate"
Payload = {"name":"fedor.dynga@altezza.org","password":"changeMe!1","rememberme":"false"}
Header_ = {"content-type": "application/json"}
since = "2025-01-31T21:00:00.000Z"
until = "2025-02-27T20:59:59.999Z"

Payload2 = json.dumps(Payload)

def auth(): # authentication
    resp = requests.post(HOST, data=Payload2, headers=Header_)
    n7token = resp.json()
    return n7token

def get_info(auth_token, since_, until_): #getting the infor from the web sile
  payl = {"since":"{}".format(since_),
          "until":"{}".format(until_),
          "order":"DESC",
          "limit":500,
          "topics_by_modules":{"KX.ObjectTrack":["LineCrossed"]},
          "channel":{"ids":[3272,3270]},
          "domain":"OTHER",
          "load_more_iteration":0,
          "event_search_request_source":"SEARCH_PAGE",
          "raw_filter_params":{"tab":"other","locations":["3272_CHANNEL","3270_CHANNEL"],
                               "timerange":"1738357200000:1740776399999",
                               "eventType":["KX.ObjectTrack:LineCrossed"]}
          }
  head = {"content-type": "application/json",
          "authorization": "Bearer {}".format(auth_token)
        }
  payl2 = json.dumps(payl)
  resp = requests.post('https://tech.kipod.ru/api/v1/events/search', data=payl2, headers=head)
  channels_list = json.loads(resp.text)
  return channels_list

def file_record(info_n): # запись фацйла
    info_m = []
    needed_keys = ['start_time', 'channel_name']
    for i in info_n:  # фильтрация нужных заголовков
        dict_you_want = {key: i[key] for key in needed_keys}
        info_m.append(dict_you_want)

    for k in info_m:  # time convertation
        st = int(list(k.values())[0])
        st /= 1000
        st2 = datetime.utcfromtimestamp(st).strftime('%Y-%m-%d %H:%M:%S')
        k.update(start_time=st2)


    keys = info_m[0].keys() # recording to CSV
    with open("my.csv", "w", newline='') as f:
        # writing the data into the file
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(info_m)

token = auth()
#print(token)
t = list(token.values())[0]
#print(t)
info_k = get_info(t, since, until)
#print('\n'.join(str(el) for el in info_n ))
file_record(info_k)
print("Файл сохранён")
