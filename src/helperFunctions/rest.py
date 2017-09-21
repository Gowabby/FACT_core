import json
from copy import deepcopy
import time
import calendar


def get_current_gmt():
    # Note that NTP can mess with this
    return int(calendar.timegm(time.gmtime()))


def success_message(data, targeted_url, request_data=None, return_code=200):
    assert isinstance(data, dict), 'data must be of type dict'
    message = deepcopy(data)

    message['timestamp'] = get_current_gmt()
    message['request_resource'] = targeted_url
    message['status'] = 0
    if request_data:
        message['request'] = request_data
    return message, return_code


def error_message(error, targeted_url, request_data=None, return_code=400):
    assert isinstance(error, str), 'error must be of type str'
    message = dict(error_message=error)

    message['timestamp'] = get_current_gmt()
    message['request_resource'] = targeted_url
    message['status'] = 1
    if request_data:
        message['request'] = request_data
    return message, return_code


def convert_rest_request(data=None):
    try:
        test_dict = json.loads(data.decode())
        return test_dict
    except json.JSONDecodeError:
        raise TypeError('Request should be a dict !')
    except (AttributeError, UnicodeDecodeError) as error:
        raise TypeError(str(error))


def get_paging(request_parameter):
    offset = request_parameter['offset'] if 'offset' in request_parameter else 0
    try:
        offset = int(offset)
    except (TypeError, ValueError):
        return 'Malformed offset parameter', False

    limit = request_parameter['limit'] if 'limit' in request_parameter else 0
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        return 'Malformed limit parameter', False

    return (offset, limit), True


def get_query(request_parameter):
    try:
        query = request_parameter.get('query')
        query = json.loads(query if query else '{}')
    except (AttributeError, KeyError):
        return dict()
    except json.JSONDecodeError:
        raise ValueError('Query must be a json document')
    return query if query else dict()