from flask import Flask, jsonify, request
from main import print_hi

app=Flask(__name__)
@app.route("/",methods=['GET','POST'])

def index():
    if request.method=='GET':
        # TODO: read arguments that are given
        result = {"status": "success"}
        return jsonify(result)
    else:
        return jsonify({'Error':"This is a GET API method"})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=9007)