# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('./vendor')

from flask import Flask, request, abort
from flask_cors import CORS, cross_origin
import redis
import urllib.parse

app = Flask(__name__) #ローカルポート5000番
CORS(app)

print("REDIS_URL: " + os.environ["YOKOSUKA2018_REDIS_URL"])
url = urllib.parse.urlparse(os.environ["YOKOSUKA2018_REDIS_URL"])
pool = redis.ConnectionPool(host=url.hostname,
                            port=url.port,
                            db=url.path[1:],
                            password=url.password,
                            decode_responses=True)
r = redis.StrictRedis(connection_pool=pool)

@app.route("/", methods=['GET'])
def callback():
    print(request)
    speed = request.args.get('speed')
    r.incr("count")
    count = r.get("count")
    r.set(count, speed)
    print("count: " + count + ", speed:" + speed)
    return "count: " + count + ", speed:" + speed


# @app.route("/speed")
# def apple():

# @app.route("/count")
# def count():
#     return r.get("apple") + " " + r.get("banana")
#
#
# @app.route("/reset")
# def reset():
#     r.set("apple",0)
#     r.set("banana",0)
#     print(r.get("apple"))
#     print(r.get("banana"))
#     return "Reset Complete!"
#

if __name__ == "__main__":
    app.debug = True;
    print("server run!")
    app.run()
