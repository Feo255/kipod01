import json
import requests
import csv
from datetime import datetime, timedelta



USER = ''
PASSWORD = ''
HOST = "https://tech.kipod.ru/oauth2/v1/auth/authenticate"
Payload = {"name":"fedor.dynga@altezza.org","password":"changeMe!1","rememberme":"false"}
Header_ = {"content-type": "application/json"}
since = "2025-02-01T21:00:00.000Z"
until = "2025-02-10T20:00:00.000Z"

Payload2 = json.dumps(Payload)

def auth(): # authentication
    resp = requests.post(HOST, data=Payload2, headers=Header_)
    n7token = resp.json()
    return n7token

def get_info(auth_token, since_, until_): #getting the infor from the web sile

  ev_list = []

  start_time = datetime.strptime(since_, '%Y-%m-%dT%H:%M:%S.%fZ')
  end_time = datetime.strptime(until_, '%Y-%m-%dT%H:%M:%S.%fZ')

  head = {"content-type": "application/json",
          "authorization": "Bearer {}".format(auth_token)
        }
  #payl2 = json.dumps(payl)
  offset = 0
  limit_ = 500

  current_time = start_time
  while current_time <= end_time:
    since_2 =  current_time.isoformat() + 'Z'
    until_time = current_time
    until_time += timedelta(hours=1)
    until_2 = until_time.isoformat() + 'Z'
    payl = {"since": "{}".format(since_2),
            "until": "{}".format(until_2),
            "order": "DESC",
            "limit": "{}".format(limit_),
            "topics_by_modules": {"KX.ObjectTrack": ["LineCrossed"]},
            "channel": {"ids": [3272, 3270]},
            "domain": "OTHER",
            "load_more_iteration": "{}".format(offset),
            "event_search_request_source": "SEARCH_PAGE",
            "raw_filter_params": {"tab": "other", "locations": ["3272_CHANNEL", "3270_CHANNEL"],
                                  "timerange": "1738357200000:1740776399999",
                                  "eventType": ["KX.ObjectTrack:LineCrossed"]}
            }
    payl2 = json.dumps(payl)
    print(payl2)

    resp = requests.post('https://tech.kipod.ru/api/v1/events/search', data=payl2, headers=head)

    # Check for request success
    if resp.status_code != 200:
      print(f"Error: {resp.status_code}")
      break
    #print(len(resp))

    data = resp.json()
    #print(data)
    print("data", len(data))


    for y in range(len(data)):
        ev_list.append(data[y])
    print("chanel", len(ev_list))
    current_time += timedelta(hours=1)


  return ev_list


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
#print(since, until)
info_k = get_info(t, since, until)
#print(info_k)
file_record(info_k)
print("Файл сохранён")
