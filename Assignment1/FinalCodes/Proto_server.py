import socket
import sys
import Data_pb2
import pandas as pd
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print(sys.stderr, 'starting up on', server_address)
sock.bind(server_address)

sock.listen(1)

while True:
    # Wait for a connection
    #exit = (input("Enter xx to exit or hit enter to continue:  "))
    #if exit == "xx":
        #connection.close()
        #break
    print(sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print (sys.stderr, 'connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(4096)
            print(sys.stderr, 'received ',data)
            if data:
                r = Data_pb2.Request().FromString(data)
                RFWID = r.RFWID
                BenchType = r.BenchType
                Column = r.Column
                dinbatch = r.dinbatch
                BatchesStart = r.BatchesStart
                BatchNum = r.BatchNum
                
                filename = "static/{}.csv".format(BenchType)
                dfN = pd.read_csv(filename)
    
                d = Data_pb2.Data()
                d.RFWID = RFWID

                ehto = ((BatchesStart-1)*dinbatch)
                ethe = (((BatchesStart+BatchNum-1)*dinbatch))
                print(ehto,ethe)
                if ethe >= len(dfN):
                    ethe = len(dfN)
                d.LastBatchN = ((ethe-ehto)//dinbatch)+BatchesStart-1
                for i in dfN[Column][ehto:ethe].values:
                    d.data.append(i)
                
                data = d.SerializeToString()
                connection.sendall(data)
                
            else:
                print(sys.stderr, 'no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()