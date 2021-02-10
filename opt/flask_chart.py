# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 18:11:08 2021

@author: kurihara
"""

import os
import glob
import io
from flask import Flask, send_file, request, render_template
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from muzinzo.Muzinzo import Muzinzo

#DATA_PATH = "\\\\larkbox\larkbox\muzinzo\data/"
DATA_PATH = "/root/opt/share/data/"
#DATA_PATH = "./data/"

app = Flask(__name__)
CORS(app)

mz = Muzinzo(DATA_PATH)

# http://サーバ:5000/
@app.route('/')
def hello():
    return "Chart Server"

# http://サーバ:5000/candle2?code=1001&term=200&volume=True
@app.route('/candle2')
def candle2():
    code = request.args.get('code', default=None, type=int)
    term = request.args.get('term', default=200, type=int)
    volume = request.args.get('volume', default="True", type=str)
    return render_template("candle2.html", title="chart", code=code, term=term, volume=volume)


# http://サーバ:5000/candle?code=1001&term=200&volume=True
@app.route("/candle")
def candle():
    code = request.args.get('code', default=None, type=int)
    term = request.args.get('term', default=200, type=int)
    volume = str2bool(request.args.get('volume', default="True", type=str))
    stochastic = str2bool(request.args.get('stochastic', default="True", type=str))
    macd = str2bool(request.args.get('macd', default="True", type=str))
    mav = str2bool(request.args.get('mav', default="True", type=str))
    
    image = io.BytesIO()
    mz.plot_chart(code, term, volume=volume, stochastic=stochastic, macd=macd, mav=mav)
    plt.savefig(image, format='png')
    image.seek(0)
    return send_file(image, attachment_filename="image.png")

class StockList:
    def __init__(self, code, name):
        self.code = code
        self.name = name[:8]

def walk_around(dic, sl):
    for i in range(1, 10):
        input_path = mz.get_database_path() + str(i*1000) + "/*.csv"
        csv_files = sorted(glob.glob(input_path))
        for csv_file in csv_files:
            filename = os.path.basename(csv_file)
            code = int(filename[0:4])
            s = StockList(code, dic[str(code)].name)
            sl.append(s)
            
# http://サーバ:5000/list/
@app.route("/list")
def list():
    dic = mz.get_dict()
    sl = []
    walk_around(dic, sl)
    return render_template("list.html", title='Stock List', members=sl)


def str2bool(s):
     return s.lower() in ["true", "t", "yes", "y", "1"]

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)
