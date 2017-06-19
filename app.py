from flask import Flask, render_template, request, redirect

import datetime
import simplejson as json
import pandas as pd
import requests
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():

    if request.method == 'GET':
        return render_template('index.html')
    else:
      i=datetime.datetime.now()

      startdate='%s%s%s' % (i.year,i.month-1,i.day)
      enddate='%s%s%s' % (i.year,i.month,i.day)
      user_input=request.form['tkr']

        if len(str(i.month))==1:
          startdate='%s%s%s%s' % (i.year,0,i.month-1,i.day)
          enddate='%s%s%s%s' % (i.year,0,i.month,i.day)

      api_url='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=%s&date.lt=%s&ticker=%s&api_key=MUSMX7hgtssoAwLpwFnb' % (startdate,enddate,user_input) 

      r=requests.get(api_url)
      data=r.json()
      df=pd.DataFrame(data['datatable']['data'])

      closing_price=df[5]

      var=[];

      for n in range(len(closing_price)-1):
        var.append(closing_price[n])

      x=range(1,len(closing_price))
      p = figure(title="closing price", x_axis_label='x', y_axis_label='y')
      p.line(x, var, legend="Temp.", line_width=2)
  
      script, div = components(p)       
      return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
  app.run(host='0.0.0.0')
