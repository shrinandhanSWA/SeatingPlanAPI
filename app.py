from flask import Flask, jsonify, request
from main import main
from pymongo import MongoClient

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        module = request.args.get('module')
        lecture_hall = request.args.get('lecture_hall')
        filters = request.args.get('filters')

        seating = main(module, str(lecture_hall), filters)

        if seating:
            result = {"status": "success", "layout": seating}
            return jsonify(result)
        else:
            result = {"status": "failure", "reason": "not enough seats for the students"}
            return jsonify(result)
    else:
        return jsonify({'Error': "This is a GET API method"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9007)
