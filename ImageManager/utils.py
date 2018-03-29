""" Assorted utils used throughout the service """

import json
from flask import jsonify
import random
import hashlib
from flask import make_response


def format_response(status, message=None):
    """ Utility helper to generate default status responses """
    if message:
        payload = jsonify({'message': message, 'status': status})
    elif 200 <= status < 300:
        payload = jsonify({'message': 'ok', 'status': status})
    else:
        payload = jsonify({'message': 'Request failed', 'status': status})

    return make_response(payload, status)


# from auth service
class HTTPRequestError(Exception):
    """ Exception that represents end of processing on any given request. """

    def __init__(self, error_code, message):
        super(HTTPRequestError, self).__init__()
        self.message = message
        self.error_code = error_code


def get_pagination(request):
    try:
        page = 1
        per_page = 20
        if 'page_size' in request.args.keys():
            per_page = int(request.args['page_size'])
        if 'page_num' in request.args.keys():
            page = int(request.args['page_num'])

        # sanity checks
        if page < 1:
            raise HTTPRequestError(400, "Page numbers must be greater than 1")
        if per_page < 1:
            raise HTTPRequestError(400, "At least one entry per page is mandatory")
        return page, per_page

    except TypeError:
        raise HTTPRequestError(400, "page_size and page_num must be integers")
