#!/usr/bin/python3
"""
state obj handling
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    retrieves all State objects
    :return: json of all states
    """
    statesl = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        statesl.append(obj.to_json())

    return jsonify(statesl)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    create state route
    :return: newly created state obj
    """
    jason_state = request.get_json(silent=True)
    if json_state is None:
        abort(400, 'Not a JSON')
    if "name" not in json_state:
        abort(400, 'Missing name')

    new_state = State(**json_state)
    new_state.save()
    resp = jsonify(new_state.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    lists State object by ID
    :param state_id: state object id
    :return: state obj with the specified id or error
    """

    ret_obj = storage.get("State", str(state_id))

    if ret_obj is None:
        abort(404)

    return jsonify(ret_obj.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    updates specific State object by ID
    :param state_id: state object ID
    :return: state object and 200 on success, or 400 or 404 on failure
    """
    json_state = request.get_json(silent=True)
    if json_state is None:
        abort(400, 'Not a JSON')
    ret_obj = storage.get("State", str(state_id))
    if ret_obj is None:
        abort(404)
    for key, val in json_stste.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(ret_obj, key, val)
    ret_obj.save()
    return jsonify(ret_obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    deletes State by id
    :param state_id: state object id
    :return: empty dict with 200 or 404 if not found
    """

    ret_obj = storage.get("State", str(state_id))

    if ret_obj is None:
        abort(404)

    storage.delete(ret_obj)
    storage.save()

    return jsonify({})
