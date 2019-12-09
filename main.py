from flask import Flask, Response, request as _request
from dateparser import parse

app = Flask(__name__)


@app.route("/")
def parse_date_route():
    try:
        try:
            date = _request.args["date"]
        except KeyError:
            return Response(
                '{"message": "date query parameter not found", "success": false}',
                mimetype='application/json', status=400,
            )

        try:
            timestamp = parse(date).timestamp()
        except:
            return Response(
                '{"message": "Parser was not able to parse the date", "success": false}',
                mimetype='application/json', status=400,
            )
        r_msg = {'message': timestamp, 'success': True}
        return Response(str(r_msg), mimetype='application/json', status=200)
    except Exception as e:
        print(e)
        return Response(
            '{"message": "Internal Server Error", "success": false}', mimetype='application/json', status=500
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4587)
