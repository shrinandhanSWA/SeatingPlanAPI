from flask import Flask, jsonify, request
from main import main
from main import get_lecture_hall

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        module = request.args.get('module')
        lecture_hall = request.args.get('lecture_hall')
        filters = request.args.get('filters')

        seating = main(module, lecture_hall, filters)

        result = {"status": "success", "layout": seating, "module": module, "lecture_hall": lecture_hall, "filters": filters}
        return jsonify(result)
    else:
        return jsonify({'Error': "This is a GET API method"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9007)
