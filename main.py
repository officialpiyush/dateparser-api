import os
import json
from flask import Flask, Response, request as _request
from dateparser import parse
from dateparser.search import search_dates

app = Flask(__name__)


@app.route("/")
def parse_date_route():
    try:
        try:
            date = _request.args["date"]
        except KeyError:
            return Response(
                json.dumps(
                    {"message": "date query parameter not found", "success": False}
                ),
                mimetype="application/json",
                status=400,
            )

        try:
            timestamp = parse(date).timestamp()
        except:
            return Response(
                json.dumps(
                    {
                        "message": "Parser was not able to parse the date",
                        "success": False,
                    }
                ),
                mimetype="application/json",
                status=400,
            )
        return Response(
            json.dumps({"message": timestamp, "success": True}),
            mimetype="application/json",
            status=200,
        )
    except Exception as e:
        print(e)
        return Response(
            json.dumps({"message": "Internal Server Error", "success": False}),
            mimetype="application/json",
            status=500,
        )

@app.route("/fromstr")
def parse_from_string_route():
    try:
        try:
            date = _request.args["message"]
        except KeyError:
            return Response(
                json.dumps(
                    {"message": "Time not supplied", "success": False}
                ),
                mimetype="application/json",
                status=400,
            )

        try:
            timestamp = search_dates(date, settings={'PREFER_DATES_FROM': 'future'})
        except:
            return Response(
                json.dumps(
                    {
                        "message": "Parser was not able to parse the date",
                        "success": False,
                    }
                ),
                mimetype="application/json",
                status=400,
            )
        if len(timestamp) <= 0 or timestamp is None:
            return Response(
                json.dumps(
                    {
                        "message": "Unable to find date in the message",
                        "success": False,
                    }
                ),
                mimetype="application/json",
                status=400,
            )

        return Response(
            json.dumps({"message": (timestamp[0])[1].timestamp(),"readable_time": (timestamp[0])[0] ,"success": True}),
            mimetype="application/json",
            status=200,
        )
    except Exception as e:
        print(e)
        return Response(
            json.dumps({"message": "Internal Server Error", "success": False}),
            mimetype="application/json",
            status=500,
        )

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 8000),
    )
