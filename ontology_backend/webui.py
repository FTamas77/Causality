from flask import Blueprint
from flask import Flask, jsonify

webui_blueprint = Blueprint("webui_blueprint", __name__)


# sanity check route
@webui_blueprint.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")
