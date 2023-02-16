import json
from flask import Flask
from flask import make_response, jsonify

from optionPrice import *

def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(json.dumps(dict(**kwargs), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response

app = Flask(__name__)
@app.route('/<symbol>/<key>')
def index(symbol, key):
    dic = optionPrice(symbol, key).record()
    return jsonify(indent=2, sort_keys=False, flask_response=dic)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


