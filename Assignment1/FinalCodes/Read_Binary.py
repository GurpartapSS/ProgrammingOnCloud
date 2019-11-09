import Data_pb2
dd = Data_pb2.Data()
f = open('Proto_DataLog', "rb")
msg = dd.FromString(f.read())
f.close()
print(msg)
