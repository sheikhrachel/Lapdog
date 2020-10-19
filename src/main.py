"""Flask app to handle slash command endpoints."""
import os
from flask import abort, Flask, request, jsonify
from lapdog import Lapdog

app = Flask(__name__)


def is_request_valid(request):
    """Validate Slack tokens for endpoints."""
    is_token_valid = request.form["token"] == os.environ["SLACK_VERI_TOKEN"]
    is_team_id_valid = request.form["team_id"] == os.environ["SLACK_TEAM_ID"]
    return is_token_valid and is_team_id_valid


@app.route("/how_many", methods=["POST"])
def how_many():
    """Check current number of issues waiting in SQS."""
    if not is_request_valid(request):
        abort(400)
    lapdog_instance = Lapdog()
    lapdog_instance.how_many()
    return jsonify(
        response_type="in_channel",
        text="There are 4 issues waiting to be handled",
    )


@app.route("/grab_issue", methods=["POST"])
def grab_issue():
    """Grab first issue in SQS to handle."""
    if not is_request_valid(request):
        abort(400)
    lapdog_instance = Lapdog()
    lapdog_instance.grab_issue()
    return jsonify(
        response_type="in_channel",
        text="There are 4 issues waiting to be handled",
    )


@app.route("/complete_issue", methods=["POST"])
def complete_issue():
    """Mark current issue as complete, remove from SQS, log write up in S3."""
    if not is_request_valid(request):
        abort(400)
    lapdog_instance = Lapdog()
    lapdog_instance.complete_issue()
    return jsonify(
        response_type="in_channel",
        text="There are 4 issues waiting to be handled",
    )


@app.route("/submit_issue", methods=["POST"])
def submit_issue():
    """Create new issue and submit into SQS with confirmation."""
    if not is_request_valid(request):
        abort(400)
    lapdog_instance = Lapdog()
    lapdog_instance.submit_issue()
    return jsonify(
        response_type="in_channel",
        text="There are 4 issues waiting to be handled",
    )
