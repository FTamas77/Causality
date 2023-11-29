# TODO: uses ontology as a data structure or database
# furthermore, use causal_lib as a computation/algorithm lib on ontology
#

from flask import Blueprint
from flask import Flask, jsonify, request
from ontology import selected_parameters

import uuid

webui_blueprint = Blueprint("webui_blueprint", __name__)


def remove_parameter(name):
    for param in selected_parameters:
        if param["name"] == name:
            selected_parameters.remove(param)
            return True
    return False


@webui_blueprint.route("/ontology", methods=["GET", "POST"])
def all_parameters():
    response_object = {"status": "success"}
    if request.method == "POST":
        post_data = request.get_json()
        selected_parameters.append(
            {
                "name": post_data.get("name"),
                "active": post_data.get("active"),
            }
        )

        response_object["message"] = "Parameter added!"
    else:
        # get all
        response_object["parameters"] = selected_parameters
    return jsonify(response_object)


@webui_blueprint.route("/ontology/<name>", methods=["PUT", "DELETE"])
def single_parameter(name):
    response_object = {"status": "success"}
    if request.method == "PUT":
        post_data = request.get_json()
        remove_parameter(name)
        selected_parameters.append(
            {
                "name": post_data.get("name"),
                "active": post_data.get("active"),
            }
        )

        response_object["message"] = "Parameter updated!"

    if request.method == "DELETE":
        remove_parameter(name)
        response_object["message"] = "Parameter removed!"

    return jsonify(response_object)
