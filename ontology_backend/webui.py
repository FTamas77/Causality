# TODO: call causal_lib from here and add to ontology
#

from flask import Blueprint
from flask import Flask, jsonify, request

import uuid

webui_blueprint = Blueprint("webui_blueprint", __name__)


BOOKS = [
    {"title": "On the Road", "author": "Jack Kerouac", "read": True, "id": "446"},
    {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J. K. Rowling",
        "read": False,
        "id": "444",
    },
    {"title": "Green Eggs and Ham", "author": "Dr. Seuss", "read": True, "id": "4474"},
]


def remove_book(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            BOOKS.remove(book)
            return True
    return False


@webui_blueprint.route("/ontology", methods=["GET", "POST"])
def all_books():
    response_object = {"status": "success"}
    if request.method == "POST":
        post_data = request.get_json()
        BOOKS.append(
            {
                "id": uuid.uuid4().hex,
                "title": post_data.get("title"),
                "author": post_data.get("author"),
                "read": post_data.get("read"),
            }
        )
        response_object["message"] = "Book added!"
    else:
        response_object["books"] = BOOKS
    return jsonify(response_object)


@webui_blueprint.route("/ontology/<book_id>", methods=["PUT", "DELETE"])
def single_book(book_id):
    response_object = {"status": "success"}
    if request.method == "PUT":
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append(
            {
                "id": uuid.uuid4().hex,
                "title": post_data.get("title"),
                "author": post_data.get("author"),
                "read": post_data.get("read"),
            }
        )
        response_object["message"] = "Book updated!"
    if request.method == "DELETE":
        remove_book(book_id)
        response_object["message"] = "Book removed!"
    return jsonify(response_object)
