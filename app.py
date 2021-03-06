from flask import Flask, render_template, request, redirect

import datetime
import simplejson as json
import pandas as pd
import requests
from bokeh.plotting import figure, save
from bokeh.embed import components

app = Flask(__name__)

@app.route('/index', methods=['GET','POST'])
def index():

    if request.method == 'GET':
      return render_template('index.html')
    else:
      i=datetime.datetime.now()

      user_input=request.form['tkr']
      
      startdate='%s%s%s' % (i.year,i.month-1,i.day)
      enddate='%s%s%s' % (i.year,i.month,i.day)
      
      if len(str(i.month))==1:
        startdate='%s%s%s%s' % (i.year,0,i.month-1,i.day)
        enddate='%s%s%s%s' % (i.year,0,i.month,i.day)

      api_url='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=%s&date.lt=%s&ticker=%s&api_key=MUSMX7hgtssoAwLpwFnb' % (startdate,enddate,user_input) 

      r=requests.get(api_url)
      data=r.json()
      df=pd.DataFrame(data['datatable']['data'])

      closing_price=df[5]
      dates=df[1]

      var=[];
      var2=[];
        
      for n in range(len(closing_price)-1):
        var.append(closing_price[n])
        var2.append(dates[n])

      x=range(1,len(closing_price))
      p = figure(title="closing price", x_axis_label='x', y_axis_label='y')
      p.line(x, var, legend="Clos. Price", line_width=2)
      p.xaxis.axis_label = 'Days excluding weekends'  
      script, div = components(p)       
      return render_template('display.html', script=script, div=div)
      
      
@app.route('/', methods=['GET','POST'])
def main():
  return redirect('/index')
  
  
if __name__ == '__main__':
  app.run(host='0.0.0.0')