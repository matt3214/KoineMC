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
      "content": "You are a helpful translation assistant who will translate text that appears in the game Minecraft into another target language.\nHere you will translate English into Koine Greek (Biblical Greek)\nMake sure to include accent marks and other diacriticals. Please also remember that these are translations of in game items, gui text, and other Minecraft related text. Always use double quotes for starting and ending JSON strings!"
    },
    {
      "role": "user",
      "content": "Please translate the following from the key value pair.\nPlease reply with a json object containing the translation of the value and an explanation for the translation in English, for example, if I gave you:\n{\"key\":\"accessibility.onboarding.screen.narrator\", \"text\":\"Press enter to enable the narrator\"}\n\nYou might reply with:\n{\"translation\":\"Πίεσον εἰσάγω γιὰ νὰ ἐνεργοποιήσῃς τὸν ἀφηγητή.\",\n \"explanation\":\"Πίεσον: Press; εἰσάγω: enter; γιὰ νὰ: in order to; ἐνεργοποιήσῃς: enable, activate; τὸν ἀφηγητή: the narrator\"}\nThe json response should always have both objects, and always use double quotes to open and close strings."
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
    for i in range(min(len(items),len(responses))):
      strings.append(f"INPUT: {items[i]}, OUTPUT: {responses[i]}")
    
    previous_formatted="\n".join(strings).replace("\'","\"")
    
    previous_json={
      "role": "user",
      "content": f"For context and consistency in word choice, your last responses were:\n{previous_formatted}"
    }
    messages.insert(2,previous_json)
  
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=messages,
  temperature=0.75,
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
    r=json.loads(reply,)
  except json.decoder.JSONDecodeError as e:
    print(reply)
    print(e)
    try:
      r=json.loads(reply.replace("\'", "\""))
    except json.decoder.JSONDecodeError as e:
      print(e)
    else:
      return r
  else:
    return r
  return None
  


import multiprocessing
import time
  
  
class Process(multiprocessing.Process):
    def __init__(self, records,offset=0):
        super(Process, self).__init__()
        self.records = records
        self.offset=offset
        
    def run(self):
      subset=self.records
      offset=self.offset
      responses=[]
      for i in range(0,len(subset)):
        item=subset[i]
        
        if i==0:
          response=translate_line(item)
        else:
          
          index = i  # example index
          size=1
          # If the index is less than size, start the slice from the beginning of the list
          start = 0 if index < size else index-size
          response = translate_line(item,previous=[subset[start:index],responses[start:index]])
        parsed=parse_response(response)
        if parsed is not None:
          parsed['i']=i+offset
          responses.append(parsed)
        if len(parsed.keys())==2:
          print(parsed)
          print(response)
        #print(responses)

      out_file = open(f"outputs/out_{offset}.json", "w",encoding='utf-8')
      json.dump(responses[:], out_file, indent = 4,ensure_ascii=False)
      out_file.close()
        
    
  
if __name__ == '__main__':
  pack = json.loads(open("lang/en_us.json",'rb').read())
  items=[(k,v) for k,v in pack.items()]
  prepared=[]
  prepared=[prepare_text(item) for item in items]
  prepared=prepared[:]
  size=500
  processes=[]
  
  for offset in range(0,len(prepared),size):
    end = len(prepared)-1 if offset > size else offset+size
    subset=prepared[offset:offset+size]
    p=Process(subset,offset)
    p.start()
    processes.append(p)
  
  print(f'Spun up {len(processes)} workers')
  
