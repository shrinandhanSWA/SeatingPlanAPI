from flask import Flask, jsonify, request
from main import main
from utils import get_topic, save_topic
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
            social = request.args.get('social')

            seating, info = main(module, str(lecture_hall), filters, reqs, blanks, social)

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
            social = topic_info['social']

            seating, info = main(module, str(lecture_hall), filters, reqs, blanks, social)

        if seating == -1:
            result = {"status": "failure", "reason": "Lecture hall not found"}
            return jsonify(result)
        if seating == -2:
            result = {"status": "failure", "reason": "Too many seats have been blanked out, try reducing this by " + str(info)}
            return jsonify(result)
        if seating == -3:
            result = {"status": "failure", "reason": "This hall is not big enough to support social distancing for this module, try choosing another hall or disabling social distancing"}
            return jsonify(result)
        if seating == -4:
            result = {"status": "failure", "reason": "This hall is not big enough to support both social distancing and the blanked seats, try reducing even numbered blanked seats by " + str(info)}
            return jsonify(result)
        if seating == -5:
            result = {"status": "failure", "reason": "A student (" + info + ") has been set to an odd numbered seat which is not possible due to social distancing, try allocating them to an even number seat instead"}
            return jsonify(result)
        if seating == -6:
            result = {"status": "failure", "reason": "A student (" + info + ") has been set to a seat, which has been blanked out, try removing the blanked seat or move the student elsewhere"}
            return jsonify(result)
        if seating == -7:
            result = {"status": "failure", "reason": "Lecture hall is not big enough for this module (" + str(info) + " students)"}
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
