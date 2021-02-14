from flask import Flask, request, render_template
from .logic import build_time_format

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

TIME_INPUT = datetime(2021, 8, 29, 19, 5, 35)
DEFAULT_DESIRED_OUTPUT = "Sunday, 5 minutes past 7"


@limiter.limit("20 per minute", override_defaults=False, error_message=" ")
@app.route("/")
def home():
    desired_output = request.args.get("desired_output") or DEFAULT_DESIRED_OUTPUT
    time_format = build_time_format(TIME_INPUT, desired_output)
    return render_template(
        "home.html",
        time_input=TIME_INPUT,
        desired_output=desired_output,
        format_result=time_format,
    )


if __name__ == "__main__":
    app.run(debug=True)
