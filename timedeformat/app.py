from flask import Flask, request, render_template
from .logic import build_time_format

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

DEFAULT_DT_INPUT = datetime.utcnow() + timedelta(hours=2)
DEFAULT_DESIRED_OUTPUT = DEFAULT_DT_INPUT.strftime("%A, %-M minutes past %-I%p")


@limiter.limit("20 per minute", override_defaults=False, error_message=" ")
@app.route("/")
def home():
    dt_input_iso = request.args.get("input") or DEFAULT_DT_INPUT.isoformat()
    desired_output = request.args.get("output") or DEFAULT_DESIRED_OUTPUT
    dt_format = build_time_format(datetime.fromisoformat(dt_input_iso), desired_output)
    return render_template(
        "home.html",
        input=dt_input_iso,
        output=desired_output,
        format_result=dt_format,
    )


if __name__ == "__main__":
    app.run(debug=True)
