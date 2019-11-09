import socket
import sys
import random
from datetime import datetime
random.seed(datetime.now())

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print(sys.stderr, 'connecting to port',server_address)
sock.connect(server_address)

import requests
import json
from requests.models import PreparedRequest
import pprint

LOF= {1:"DVD-testing",2:"DVD-training",3:"NDBench-testing",4:"NDBench-training"}
LOC = {1:"CPUUtilization_Average",2:"NetworkIn_Average",3:"NetworkOut_Average",4:"MemoryUtilization_Average",5:"Final_Target"}
pp = pprint.PrettyPrinter(indent=2)

##get user requests
Naam = input("Please enter your name: ")
RFWID = random.randint(0,100)
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

import Data_pb2
r = Data_pb2.Request()
dd = Data_pb2.Data()

r.RFWID = RFWID
r.BenchType = BenchType
r.Column = Column
r.dinbatch = dinbatch
r.BatchesStart = BatchesStart
r.BatchNum = BatchNum

t = r.SerializePartialToString()
print(t)

try:
    
    # Send data
    message = 'This is the message.  It will be repeated.'
    print(sys.stderr, 'sending ')
    sock.sendall(t)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(4096)
        dd.FromString(data)
        print(dd)
        
        amount_received += len(data)
        print(sys.stderr, 'received ',data)

finally:
    print(sys.stderr, 'closing socket')
    sock.close()
    f = open('Proto_DataLog', "wb")
    f.write(data)
    #f.write(dd.FromString(data))
    f.close()
Data = dd.FromString(data)
print('\nRecieved Data ..\n',Data)