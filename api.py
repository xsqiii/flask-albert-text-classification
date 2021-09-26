# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template
import json

import predict

sentiment = Flask(__name__)

api = predict.Api()


@sentiment.errorhandler(404)
def page_not_found():
    return render_template('errors/404.html'), 404


@sentiment.route('/nlp/sentiment_analyzer', methods=['POST'])
def documentAdd():
    code = 0
    message = "success"

    data = json.loads(request.get_data())

    text_list = data["texts"]

    result = api.api(text_list)
    if result:
        resp = json.dumps({'code': code, 'msg': message, "data": {"result": result}},
                          ensure_ascii=False)
    else:
        resp = json.dumps({'code': -1, 'msg': "failed", "data": {"result": result}},
                          ensure_ascii=False)
    return resp


if __name__ == '__main__':
    sentiment.run(host="0.0.0.0", debug=False)
