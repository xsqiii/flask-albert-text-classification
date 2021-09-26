from flask import Flask, request
import json
from dataclasses import *
import dataclasses
import predict

app = Flask(__name__)

predictor = predict.Predictor()


@dataclass
class Response:
    code: int
    msg: str
    data: object


@app.route('/nlp/sentiment_analyze', methods=['POST'])
def sentiment():

    data = json.loads(request.get_data())

    text_list = data["text_list"]

    result = predictor.predict(text_list)

    if result:
        resp = Response(0, "", {"result": result})
    else:
        resp = Response(-1, "failed", None)

    return dataclasses.asdict(resp)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
