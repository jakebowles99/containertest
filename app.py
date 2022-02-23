from power_of_10 import search_athletes
from power_of_10 import get_athlete
import json
import os
from flask import Flask
from flask import render_template
from flask_restful import Resource, Api, reqparse
import pandas as pd
app = Flask(__name__)
api = Api(app)


class bests(Resource):
    def get(self):

        athleteId = search_athletes(firstname="jake", surname="bowles")
        atheleteDetails = get_athlete(athleteId[0]["athlete_id"])

        pbs = []

        for x in atheleteDetails["pb"]:
            pbs.append(x)

        return {'data': pbs}, 200  # return data and 200 OK code
    pass

class performances(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('firstname', required=True)  # add arguments
        parser.add_argument('surname', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        athleteId = search_athletes(firstname=args['firstname'], surname=args['surname'])
        atheleteDetails = get_athlete(athleteId[0]["athlete_id"])

        pbs = []

        for x in atheleteDetails["pb"]:
            pbs.append(x)

        performances = []

        for x in atheleteDetails["performances"]:
            performances.append(x)

        return {'data': performances}, 200  # return data and 200 OK code
    pass

api.add_resource(bests, '/pbs')  # '/pbs' is our entry point
api.add_resource(performances, '/perfs')  # '/pbs' is our entry point

@app.route('/')
def hello_world():
  # Initialize class and upload files
    return render_template('index.html', title='Welcome', username='jake')
# if __name__ == '__main__':
#     app.run()  # run our Flask app