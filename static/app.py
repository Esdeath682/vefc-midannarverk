import os
import urllib.request
from flask import Flask, render_template, request, json
from datetime import datetime
from jinja2 import ext

app = Flask(__name__)

#na i petrol a apis.is
with urllib.request.urlopen("https://apis.is/petrol") as url:
    gogn = json.loads(url.read().decode())


app.jinja_env.add_extension(ext.do)

def format_time(gogn):
    return datetime.strptime(gogn, '%Y-%m-%d-%H:%S.%f').strftime('%d. %m. %Y. KL. %H:')

app.jinja_env.filters['format_time'] = format_time


def minPetrol():
    minPetrolPrice = 1000
    company = None
    address = None
    lst = gogn['results']

    for i in lst:
        if i['bensin95'] is not None:
            if i['bensin95'] < minPetrolPrice:
                company = i['company']
                address = i['name']
    return [minPetrolPrice, company, address]
# oll fyrirtaeki x1
@app.route('/')
def home():
    return render_template('index.html',gogn=gogn, MinP = minPetrol())

# eitt fyrirtaeki - allar stodvar
@app.route('/company/<company>')
def comp(company):
    return render_template('company.html', gogn=gogn, com=company)

@app.route('/moreinfo/<key>')
def info(key):
    return render_template('moreinfo.html',gogn=gogn,k=key)

#villuskilabod
@app.errorhandler(404)
def pagenotfound(error):
    return render_template('pagenotfound.html'), 404




if __name__ == '__main__':
    app.run(debug=True)


