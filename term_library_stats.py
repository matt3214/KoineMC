import json
import pandas as pd
import matplotlib.pyplot as plt

# Includes a class of objects called 'TermLibrary' (configured with default path)
from term_library import *

# initialize the term library
library=TermLibrary()

# Nice __str__ method
print(library)
pack_path="res/lang/en_us.json"
pack = json.loads(open(pack_path,'rb').read())
items=[(k,v) for k,v in pack.items()]

# Get number of matches and store in list 'counts'
counts=[]
for i in range(0,len(items)):
  relevant=library.get_relevant(" ".join([items[i][0],items[i][1]]))
  counts.append(len(relevant))
  # if i%1000==0:
  #   print(items[i])
  #   print(relevant)

# pandas
df=pd.DataFrame(counts)
zeros=df.where(df[0]==0).count()[0]

# matplotlib
gs_kw = dict(height_ratios=[3, 1])
fig, axs = plt.subplots(2,gridspec_kw=gs_kw)
fig.suptitle(f"Histogram of # of term matches \n with each line in '{pack_path}'")
axs[0].hist(df,bins=list(range(0,df.max()[0],1)))
axs[1].set_axis_off()
axs[1].add_artist(axs[1].patch)
axs[1].patch.set_zorder(-1)
axs[1].set_facecolor('lightblue')
axs[1].text(.04,.2,f"Stats:\n{len(items)} lines total.\n{zeros} lines had zero term matches.", fontsize=11)

plt.show()