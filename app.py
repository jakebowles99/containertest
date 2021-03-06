from power_of_10 import search_athletes
from power_of_10 import search_event
from power_of_10 import get_athlete
from results import get_results
import json
import os
from flask import Flask, request, redirect
from flask import render_template
from flask_restful import Resource, Api, reqparse
import pandas as pd
app = Flask(__name__)
api = Api(app)


class bests(Resource):
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

        performances = []

        for x in atheleteDetails["performances"]:
            performances.append(x)
        for result in performances:

            blank = result['value'].count(':')
            split = result['value'].split(":")

            secs= 0
            for i in range(0, blank +1):
                index = blank - i
                if(i == 0):
                    counter = 1
                else:
                    counter = 60**i
                try:
                    secs += int(split[index]) * counter
                except:
                    print("no integer my drilla")
            result['value'] = secs

        return {'data': performances}, 200  # return data and 200 OK code
    pass

class atheleteDetails(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('firstname', required=True)  # add arguments
        parser.add_argument('surname', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        athleteId = search_athletes(firstname=args['firstname'], surname=args['surname'])
        # atheleteDetails = get_athlete(athleteId[0]["athlete_id"])

        return {'data': athleteId}, 200  # return data and 200 OK code
    pass

def get_events(firstname, lastname):
  athleteId = search_athletes(firstname=firstname, surname=lastname)
  atheleteDetails = get_athlete(athleteId[0]["athlete_id"])

  array = []

  for result in atheleteDetails["performances"]:
      meetingR=result["meeting"].replace("#","%23")
      meetingR=meetingR.replace(",","%2c")
      meetingR=meetingR.replace("&","%26")
      array.append(search_event(meeting=meetingR, terrain="any",date_from=result["date"], date_to=result["date"]))

  return array


class events(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('firstname', required=True)  # add arguments
        parser.add_argument('surname', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        events = get_events(args['firstname'], args['surname'])


        return {'data': events}, 200  # return data and 200 OK code
    pass

class results(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('firstname', required=True)  # add arguments
        parser.add_argument('surname', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        results=[]

        events = get_events(args['firstname'], args['surname'])

        for i in range(1, 10):
            meetingId=events[i][0]["meeting_id"]
            print(meetingId)
            results.append(get_results(meeting_id=meetingId))

        for result in results:
            resultList = result['results'][0]['results']
            count = 0
            for item in resultList:
                blank = item['perf'].count(':')
                split = item['perf'].split(":")

                secs= 0
                for i in range(0, blank +1):
                    index = blank - i
                    if(i == 0):
                        counter = 1
                    else:
                        counter = 60**i
                    try:
                        secs += int(split[index]) * counter
                    except:
                        print("no integer my drilla")
                result['results'][0]['results'][count]['perf'] = secs
                count=count+1


        return {'data': results}, 200  # return data and 200 OK code
    pass

api.add_resource(bests, '/pbs')  # '/pbs' is our entry point
api.add_resource(performances, '/perfs')  # '/pbs' is our entry point
api.add_resource(atheleteDetails, '/details')  # '/pbs' is our entry point
api.add_resource(events, '/events')  # '/pbs' is our entry point
api.add_resource(results, '/results')  # '/pbs' is our entry point

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    data = request.form.get('data')
    processed_text = text.upper()
    string_arr = processed_text.split(" ")

    return redirect(f"https://jbcicd.azurewebsites.net/{data}?firstname={string_arr[0]}&surname={string_arr[1]}")

@app.route('/')
def hello_world():
  # Initialize class and upload files
    return render_template('index.html', title='Welcome', username='Jake')
# if __name__ == '__main__':
#     app.run()  # run our Flask app
