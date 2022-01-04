from flask import Flask, jsonify, request
from main import main, get_topic, save_topic
from pymongo import MongoClient

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        refresh = request.args.get('fromdb')

        if refresh == '0':
            module = request.args.get('module')
            lecture_hall = request.args.get('lecture_hall')
            filters = request.args.get('filters')
            reqs = request.args.get('reqs')
            blanks = request.args.get('blanks')

            seating = main(module, str(lecture_hall), filters, reqs, blanks)

        else:
            # need to look information up from database
            module = request.args.get('module')
            topic = request.args.get('topic')

            # find topic from the main database
            topic_info = get_topic(topic)

            lecture_hall = topic_info['lectureHall']
            filters = topic_info['filterString']
            reqs = topic_info['reqString']
            blanks = topic_info['blankString']

            seating = main(module, str(lecture_hall), filters, reqs, blanks)

        if seating == -1:
            result = {"status": "failure", "reason": "Lecture hall not found"}
            return jsonify(result)
        if seating == -2:
            result = {"status": "failure", "reason": "Trying to set student "
                                                     "to a blanked out seat"}
            return jsonify(result)
        if seating is not None:
            # save to the topic if it is a shuffle before returning it
            if refresh == '1':
                save_topic(request.args.get('topic'), seating)

            result = {"status": "success", "layout": seating}
            return jsonify(result)
        else:
            result = {"status": "failure",
                      "reason": "Not enough seats for the students"}
            return jsonify(result)
    else:
        return jsonify({'Error': "This is a GET API method"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9007)
