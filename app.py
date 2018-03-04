# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('./vendor')

import ast

from flask import Flask, request, render_template
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
    count = r.get("count")
    res = r.get(count)
    print("Redis response:")
    print(res)

    # JSONに変換したいところだが、Redisから取得した値がシングルクォートに入っているため断念。
    dic = ast.literal_eval(res)
    return render_template('index.html', speed=dic["speed"])


@app.route("/speed")
def speed():
    print(request)
    speed = request.args.get('speed')
    date = request.args.get('date')
    r.incr("count")
    count = r.get("count")
    r.set(count, {"speed":speed, "date": date})
    return "count: " + count + ", speed:" + speed + ", date:" + date


@app.route("/last")
def last():
    print(request)
    count = r.get("count")
    res = r.get(count)
    print("Redis response:")
    print(res)
    dic = ast.literal_eval(res)
    return dic["speed"]


@app.route("/button")
def button():
    count = r.get("count")
    speed = r.get(count)
    return speed


if __name__ == "__main__":
    app.debug = True;
    print("server run!")
    app.run()
