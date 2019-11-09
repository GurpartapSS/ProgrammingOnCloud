from flask import Flask, render_template, request
import json
import pandas as pd
from random import seed
from random import randint
seed(1)
app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello ..please proceed with request at reqData'

@app.route("/reqData")
def req():
    RFWID = int(request.args.get("RFWID"))
    BenchType=request.args.get("BenchType")
    Column= request.args.get("Column")
    dinbatch=int(request.args.get("dinbatch"))
    batchStart=int(request.args.get("batchStart"))
    batchNum= int(request.args.get("batchNum"))
    
    
    filename = "static/{}.csv".format(BenchType)
    dfN = pd.read_csv(filename)
    
    ddata = []
    for i in range(batchNum):
        ehto = ((batchStart+i-1)*dinbatch)
        ethe = (((batchStart+i)*dinbatch))
        if ethe >= len(dfN):
            ethe = len(dfN)
            ddata.append(((dfN[Column][ehto:ethe]).values).tolist())
            lastbatch = batchStart+i
            break
        else:
            ddata.append(((dfN[Column][ehto:ethe]).values).tolist())
            lastbatch = batchStart+i
    return(json.dumps({'ID':RFWID,'LastBatchID':lastbatch,'DATA': ddata}))

@app.route("/test_connection")
def test_connection():
    no = randint(0,10000)
    return json.dumps({"randomNo":no})


if __name__ == "__main__":
	app.run()