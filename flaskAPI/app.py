from flask import Flask, jsonify, request
from print_hi import print_hi

app=Flask(__name__)
@app.route("/",methods=['GET','POST'])


def index():
    if request.method=='GET':
        module = request.args.get('module')
        lecture_hall = request.args.get('lecture_hall')
        filters = request.args.get('filters')

        result = {"status": "success", "module": module, "lecture_hall": lecture_hall, "filters": filters}
        return jsonify(result)
    else:
        return jsonify({'Error':"This is a GET API method"})


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=9007)