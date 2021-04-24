import requests
import json
from telethon import TelegramClient, events
import urbandict
import os

ID = int(os.getenv("API_ID"))
HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OXFORD_APP_ID = os.getenv("OXFORD_APP_ID")
OXFORD_APP_KEY = os.getenv("OXFORD_APP_KEY")
LANGUAGE = os.getenv("LANGUAGE")


def dictina(word):
	app_id =OXFORD_APP_ID
	app_key = OXFORD_APP_KEY
	language =LANGUAGE
	word_id = word
	fields = 'definitions'
	strictMatch = 'false'

	url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word_id.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch;

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
	#print(r.status_code, r.text)
	if r.status_code==200:
		json_data=json.loads(r.text)
		typeof  = json_data['results'][0]['lexicalEntries'][0]['lexicalCategory']['id']
		print(typeof)
		main_def= json_data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
		print(main_def)
		head    = "Definition of "+json_data['id']+"("+typeof+")"
		tail    = main_def+'\n\n'
		try:
			for i in range(len(json_data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['subsenses'])):

				sub_def=json_data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['subsenses'][i]['definitions'][0]		
				tail+=str(i)+". "+sub_def+"\n"
		except:
			print('errr')
		
		return head,tail
	else:
		return 'ERROR',r.text

def udict(query):
    print(query)
    try:
        mean = urbandict.define(query)
        #print(mean)
    except HTTPError:
        return f"Sorry, couldn't find any results for: `{query}``"
    output = ''
    limit = 2
    for i, mean_ in enumerate(mean, start=1):
        output += f"{i}. **{mean_['def']}**\n" + \
            f"  Examples:\n  * `{mean_['example'] or 'not found'}`\n\n"
    #print(output)
    if not output:
        return f"No result found for **{query}**"
    output = f"**Results**\n\n\n{output}"
    return output


bot = TelegramClient('bot',ID,HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply('Hi, Send me any word and I will give you the Def')

    raise events.StopPropagation    

@bot.on(events.NewMessage())
async def corona(event):
	if event.text and event.is_private:
		head,cont=dictina(event.text)
		print(event.text,head)
		Sending_msg="<u><b>"+head+"</b></u>\n\n"+cont
		await event.respond(Sending_msg,parse_mode='html')
		await event.respond(udict(event.text))
		print(udict(event.text))
		raise events.StopPropagation
	else:
		await event.respond('Send me a WORD')

@bot.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.respond('Send any word and get the definition\n<a=https://github.com/jaindu/DefBot>Source</a>\nBy @charindith',parse_mode='html')
    raise events.StopPropagation

print('bot start')
bot.run_until_disconnected()
