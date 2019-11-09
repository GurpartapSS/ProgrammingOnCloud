import requests
import json
from requests.models import PreparedRequest
import pprint
from random import seed
from random import randint

LOF= {1:"DVD-testing",2:"DVD-training",3:"NDBench-testing",4:"NDBench-training"}
LOC = {1:"CPUUtilization_Average",2:"NetworkIn_Average",3:"NetworkOut_Average",4:"MemoryUtilization_Average"}
pp = pprint.PrettyPrinter(indent=2)

##get user requests
Name = input('Enter your name: ')

url_t = 'http://127.0.0.1:5000/test_connection'
op = requests.get(url_t)
RFWID = op.json()['randomNo']

print("\nYour RFWID is {}".format(RFWID))
print("\nSelect the Benchmark:")
pp.pprint(LOF)
BenchType = LOF[(int(input("Enter the index: ")))]
print("\nSelect the Feature:")
pp.pprint(LOC)
Column = LOC[(int(input("Enter the index: ")))]
dinbatch = int(input("\nENter samples in one batch: "))
BatchesStart = int(input("Enter the batch ID: "))
BatchNum = int(input("Enter number of batches: "))

##do the preprocessing 
#batchStart = (BatchesStart-1) * NBatch
#batchENd = ((BatchesStart + BatchNumber - 1) * NBatch)-1
#lastbatch = BatchNumber + BatchesStart -1


###make url
API = "reqData"
url = 'http://127.0.0.1:5000/{}?'.format(API)
params = {'RFWID':RFWID,'BenchType':BenchType,'Column':Column,'dinbatch':dinbatch,'batchStart':BatchesStart,'batchNum':BatchNum}
req = PreparedRequest()
req.prepare_url(url,params)
rep = requests.get(req.url)
if rep.status_code == 200:
	print("\n")
	pp.pprint(rep.json())
	print("\nData:\n",rep.json()['DATA'])
	print("\nRFWID:\n",rep.json()['ID'])
	print("\nLastBatchID:\n",rep.json()['LastBatchID'])
	with open('data.json', 'w') as outfile:
    		json.dump(rep.json(), outfile)
else:
	print("Request could not be completed!")