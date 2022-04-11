from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os
import sys
import configparser
import csv
import pdb

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"


cpass = configparser.RawConfigParser()
cpass.read('config.data')


#Method for matching user object with id
def get_user_name(all_users, all_users_id, id):
    for i in range(len(all_users_id)):
        if all_users_id[i] == id:
            if all_users[i].username is not None:
                return all_users[i].username
    return ''

def get_all_participants(target_group):
    all_participants = []
    all_participants_id = []
    try:
        all_participants = client.get_participants(target_group)
        all_participants_id = [p.id for p in all_participants]
    finally:
        return all_participants,all_participants_id


# Connection to Telegram Api
try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))

# Search client groups

# Params for group request
os.system('clear')
chats = []
last_date = None
chunk_size = 200
groups = []


result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        groups.append(chat)
    except:
        continue
# User dialog to select groups
print(gr+'[+] Choose a group to scrape members :'+re)
i = 0
for g in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - ' + g.title)
    i += 1

g_index = input(gr+"[+] Enter a Number : "+re)
target_group = groups[int(g_index)]

# Get all user in selected chat 
all_participants, all_participants_id = get_all_participants(target_group)


print(gr+'[+] Fetching Chat...')
# Iterating messages and writhing them to a file 
with open("chat.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=";", lineterminator="\n")
    writer.writerow(['id', 'author', 'text', 'date'])
    for message in client.iter_messages(target_group, limit=None):
        try:
            #pdb.set_trace()
            text = message.text.replace('\n', ' ').strip() or ''
            date = message.date
            id = message.id
            user_name = ''
            if message.from_id is not None and len(all_participants) > 0:
                user_id = message.from_id.user_id                
                user_name = get_user_name(
                   all_participants, all_participants_id, user_id)
            writer.writerow([id, user_name, text, date])
        except Exception as e:
            continue
