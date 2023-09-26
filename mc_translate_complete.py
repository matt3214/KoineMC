import re
import string
import os
import openai
from dotenv import load_dotenv
import json
import csv
from term_library import *

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

library = TermLibrary()

def extract_amps(s):
  pattern = r'&&&(.*?)&&&'
  matches = re.findall(pattern, s)
  return matches


pack = json.loads(open("lang/en_us.json",'rb').read())
items=[(k,v) for k,v in pack.items()]

item=items[0]
library.get_relevant(" ".join([item[0],item[1]]))


exit()
completed=[]

def escape(item):
  if len(item)==2:
    return f"\"{item[0]}\", \"{item[1]}\", "
  elif len(item)==3:
    #print(item)
    return f"\"{item[0]}\", \"{item[1]}\", \"{item[2]}\""


completed = []


batch=1
for i in range(len(items)):
  current=items[i]

  prepared_payload=[escape(item) for item in items[i:i+batch]]

  if i>0:
    historic_items=[escape(full_item) for full_item in completed[i-batch:i]]
  else:
    historic_items=[]

  extras="\n---".join(historic_items)
  payload="\n".join(prepared_payload)


  system=f"""
Translation:
I will give you a Minecraft related term to translate into Koine / Classical Greek.
I will also give you some context by giving you the key that the game uses to refer to the text.
Make sure to include accent marks and other diacritical marks! Modern Greek is not to occur, so breathing marks are required on vowels that start words. Please use only classical and Koine era Greek with a focus on New Testament terms.
Remember that the context of all of these is the videogame Minecraft. There are terms related to GUI and also terms relating to ingame items.
Input and Output Format:
You will complete the line I send you, such as in the following examples. The text you complete is to be wrapped in ampersands as follows.  Newlines will be escaped.
Examples:
---
"gui.chatReport.send", "Send Report", &&&"Ἀποστολὴ Ἀναφορᾶς"&&&
---
"accessibility.onboarding.screen.narrator", "Press enter to enable the narrator", &&&"Πάτησε τον πλήκτρο Enter για να ενεργοποιήσεις τον αφηγητή."&&&
---
"advancement.advancementNotFound", "Unknown advancement: %s", &&&"Ἀγνωστη προκοπή: %s"&&&
---
"addServer.add", "Done", &&&"Ἔτελειώθη"&&&
---
"accessibility.onboarding.screen.title", "Welcome to Minecraft!\n\nWould you like to enable the Narrator or visit the Accessibility Settings?", &&&"Καλῶς ὑποδέχεσαι εἰς τὸ Minecraft!\n\nΘὰ ἤθελες νὰ ἐνεργοποιήσῃς τὸν ἀφηγητή ἢ νὰ ἐπισκευθῇς τὶς ἐπιλογὲς προσβασιμότητας;"&&&
---
"advancements.adventure.adventuring_time.description", "Discover every biome",&&&"Ἀνακαλύψατε πᾶσαν τὴν βιότοπον."&&&
---
REMEMBER THAT THIS IS KOINE GREEK, INCLUDE DIACRITICALS!
{extras}
"""
  relevant_csv = get_revelant(current)
  context=f"""Here is a library of terms that may be relevant to consider when creating the translations, this library is merely a set of knowledge for you to pull from (organized as a CSV)\n{relevant_csv}"""
  
  prompt=f"""{payload}"""
  

  print(system,"\n",prompt)
  response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
    {
      "role": "system",
      "content": system
    },
    {
      "role": "user",
      "content": payload
    }
  ],
    temperature=0.1,
    max_tokens=250,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  x=response.choices[0].message.content
  print(response)
  print(x)
  val = extract_amps(x)[0]
  completed.append([current[0],current[1],val])
  print(completed)
  exit()

def extract_transform(text, param_value):
    # Escape periods in the parameter value for regex
    escaped_param = re.escape(param_value)
    print(escaped_param)
    pattern = rf'"{escaped_param}",(.*?),(.*?)\n'
    
    # Find the match in the input text
    match = re.search(pattern, text+"\n")
    
    # If there's a match, extract the tuple and add the third value
    if match:
      return (f'"{param_value}"', match.group(1).strip(), match.group(2).strip())
          
  
print(extract_transform(x,items[i][0]))
exit()

def parse_response(reply)->tuple:
  try:
    r=csv.reader()
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





# def prepare_text(item):
#   return {"key":f"{item[0]}","text":f"{item[1]}"}


# def parse_response(reply)->dict:
#   try:
#     r=json.loads(reply,)
#   except json.decoder.JSONDecodeError as e:
#     print(reply)
#     print(e)
#     try:
#       r=json.loads(reply.replace("\'", "\""))
#     except json.decoder.JSONDecodeError as e:
#       print(e)
#     else:
#       return r
#   else:
#     return r
#   return None
  


# import multiprocessing
# import time
  
  
# class Process(multiprocessing.Process):
#     def __init__(self, records,offset=0):
#         super(Process, self).__init__()
#         self.records = records
#         self.offset=offset
        
#     def run(self):
#       subset=self.records
#       offset=self.offset
#       responses=[]
#       for i in range(0,len(subset)):
#         item=subset[i]
        
#         if i==0:
#           response=translate_line(item)
#         else:
          
#           index = i  # example index
#           size=1
#           # If the index is less than size, start the slice from the beginning of the list
#           start = 0 if index < size else index-size
#           response = translate_line(item,previous=[subset[start:index],responses[start:index]])
#         parsed=parse_response(response)
#         if parsed is not None:
#           parsed['i']=i+offset
#           responses.append(parsed)
#         if len(parsed.keys())==2:
#           print(parsed)
#           print(response)
#         #print(responses)

#       out_file = open(f"outputs/out_{offset}.json", "w",encoding='utf-8')
#       json.dump(responses[:], out_file, indent = 4,ensure_ascii=False)
#       out_file.close()
        
    
  
# if __name__ == '__main__':
#   pack = json.loads(open("lang/en_us.json",'rb').read())
#   items=[(k,v) for k,v in pack.items()]
#   prepared=[]
#   prepared=[prepare_text(item) for item in items]
#   prepared=prepared[:]
#   size=500
#   processes=[]
  
#   for offset in range(0,len(prepared),size):
#     end = len(prepared)-1 if offset > size else offset+size
#     subset=prepared[offset:offset+size]
#     p=Process(subset,offset)
#     p.start()
#     processes.append(p)
  
#   print(f'Spun up {len(processes)} workers')
  
