import json
import time
import numpy as np
from ripple_api import RippleRPCClient
import plyvel


poll_t = 1 #set poll time to fetch info from node
tmp_dict = {}
n = 2
encoding = 'utf-8'

#LevelDB database location
db_dir = '/tmp/ledger.db'

#Creating RPC conection handler using python SDK
rpc = RippleRPCClient('http://s1.ripple.com:51234/', username='<username>', password='<password>')

#Removing old LevelDB data
plyvel.destroy_db(db_dir)


#Method to fetch server info periodically and parse the output and ingest required field info into LevelDB key-value database.
def get_server_info():
   server_info = rpc.server_info()

   #converting dict into json object
   server_json = json.dumps(server_info)
   #print(server_json)

   #get seq field from the json object, this sequence number generated for every new ledger
   seq_info = server_info['info']['validated_ledger']['seq']

   #fetching last close ledger time spent
   close_s = server_info['info']['last_close']['converge_time_s']

   #populating dict with key, value store i.e seq is key and close_s as value
   #this will keep unique key and latest time in case duplicate seq id comes during poll
   tmp_dict[seq_info] = close_s

   #calc current time
   ts = time.time()

   db = plyvel.DB(db_dir, create_if_missing=True)

   raw_info = str(ts) +' '+ str(seq_info)
   key = bytes(str(seq_info),'utf-8')
   val = bytes(str(ts),'utf-8')
   db.put(key, val)
   db.close()


#method takes dict as an input and calculate its min, max and avg values
def dict_mean(dict_list):
   all_v = tmp_dict.values()
   max_v = round(max(all_v),2)
   min_v = round(min(all_v),2)
   avg_v = round(float(np.mean(list(tmp_dict.values()))),2)

   #This will keep printing and overwrite stdout with latest values.
   print("Ledger Validation Time  => Maximum Value: {} , Minimum Value: {} , Avarage Value: {}".format(max_v,min_v,avg_v), end="\r")

#write ledge info to flat file
def flat_file_writer():
   db = plyvel.DB(db_dir, create_if_missing=False)
   open("/tmp/ledger_info.dat", "w").close()
   for key, value in db:
      #print(str(value,encoding),str(key,encoding))
      raw_info2 = str(value,encoding) +' '+ str(key,encoding)
      #recording the current time and each seq number in a file for graphical presentation via gnuplot
      outF = open("/tmp/ledger_info.dat", "a")
      outF.write(str(raw_info2))
      outF.write("\n")
      outF.close()
   db.close()

#This is main section
#Creating infinite while loop and calling  methods with sleep time of poll_t
while n > 0:
   get_server_info()
   flat_file_writer()
   dict_mean(tmp_dict)
   time.sleep(poll_t)
