from flask import Blueprint, jsonify, request


carousel = Blueprint('carousel', __name__)

@carousel.route('/list_min')
def list_min():

    return