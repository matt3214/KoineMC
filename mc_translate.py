import re
import string
import os
import openai
from dotenv import load_dotenv
import json
import csv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def translate_line(line,previous=[None]):
  
  messages=[
    {
      "role": "system",
      "content": "You are a helpful translation assistant who will translate text that appears in the game Minecraft into another target language.\nHere you will translate English into Koine Greek (Biblical Greek)\nMake sure to include accent marks and other diacriticals."
    },
    {
      "role": "user",
      "content": "Please translate the following from the key value pair.\nPlease reply with two things, the translation of the value, and an explanation for the translation in English, for example, if I gave you:\n{\"key\":\"accessibility.onboarding.screen.narrator\", \"text\":\"Press enter to enable the narrator\"}\n\nYou would reply with:\n{\"translation\":\"Πίεσον εἰσάγω γιὰ νὰ ἐνεργοποιήσῃς τὸν ἀφηγητή.\",\n \"explanation\":\"Πίεσον = Press | εἰσάγω = introduce, bring in | γιὰ νὰ = in order to | ἐνεργοποιήσῃς = enable, activate | τὸν ἀφηγητή = the narrator\"}"
    },
    {
      "role": "user",
      "content": f"Please perform this task for:\n{line}, output only the json response"
    }
  ]
  
  if previous[0] is None:
    pass
  else:
    items=previous[0]
    responses=previous[1]
    strings=[]
    for i in range(len(items)):
      strings.append(f"input: {items[i]}, output: {responses[i]}")
    
    previous_formatted="\n".join(strings)
    
    previous_json={
      "role": "user",
      "content": f"For context and consistency in word choice, your last responses were:\n{previous_formatted}"
    }
    messages.insert(2,previous_json)
  
  response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=messages,
  temperature=0.25,
  max_tokens=1024,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
  )
  #mc_translate.pyprint(messages[2])
  return response.choices[0].message.content

def prepare_text(item):
  return {"key":f"{item[0]}","text":f"{item[1]}"}


def parse_response(reply)->dict:
  try:
    r=json.loads(reply)
  except json.decoder.JSONDecodeError:
    print(reply)
    return None
  else:
    return r
  
  
  
pack = json.loads(open("lang/en_us.json",'rb').read())

items=[(k,v) for k,v in pack.items()]
prepared=[]
responses=[]
prepared=[prepare_text(item) for item in items]

dump_size=3

for i in range(0,len(items)):
  item=items[i]
  
  if i==0:
    response=translate_line(prepare_text(item))
  else:
    
    
    index = i  # example index
    size=3
    # If the index is less than size, start the slice from the beginning of the list
    start = 0 if index < size else index-size
    response = translate_line(prepare_text(item),previous=[prepared[start:index],responses[start:index]])
  parsed=parse_response(response)
  if parsed is not None:
    parsed['i']=i
    responses.append(parsed)
  #print(responses)
  
  if i%dump_size==0 and i>0:
    k=int(i/dump_size)
    out_file = open(f"write_{k}.json", "w")
    json.dump(responses[i-dump_size:i], out_file, indent = 4)
    out_file.close()
  



