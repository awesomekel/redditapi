#!venv/bin/python
import requests
import json
import bs4
import os
from flask import Flask, jsonify
from flask import make_response
 
app = Flask(__name__)
 
@app.route('/gethot', methods=['GET'])
def get_hot():
    return get_news('hot/')
 
@app.route('/getrising', methods=['GET'])
def get_rising():
    return get_news('rising/')
 
@app.route('/gettop', methods=['GET'])
def get_top():
    return get_news('top/')

@app.route('/getcontroversial', methods=['GET'])
def get_controversial():
    return get_news('controversial/')

@app.route('/r/<string:subreddit>', methods=['GET'])
def get_funny(subreddit):
    return get_news('r/'+subreddit+'/',1)
 
def get_news(category='',cattype=0):
    index_url="https://www.reddit.com/"
    response=requests.get(index_url+category)
    ret=[]
    soup = bs4.BeautifulSoup(response.text, "html5lib")
    posts=soup.select("div#siteTable div.thing")
    for post in posts:
        info=post.select("p.title a")[0]
        if cattype==0:
            subreddit=post.select("p.tagline a")[1].text[3:].capitalize()
            ret.append({"title":info.text,"link":info['href'],"subreddit":subreddit})
        else:
            ret.append({"title":info.text,"link":info['href']})
    return json.dumps(ret)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

 if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)