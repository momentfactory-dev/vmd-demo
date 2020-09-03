import datetime
from functools import wraps
from flask import request, Response


def annotation(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(datetime.datetime.now(), ": ============================ START ============================")
        print(datetime.datetime.now(), ":", "function::", f.__name__)
        print(datetime.datetime.now(), ":", "url:", request.path)
        print(datetime.datetime.now(), ":", "data:", request.get_data(), type(request.get_data()))
        result = f(*args, **kwargs)
        print(datetime.datetime.now(), ": ============================ END ============================")					# 9)

        return result
    return decorated_function


def on_json_loading_failed_return_dict(e):
    print("json 파싱 에러")
    print(e)
    return {}


def annotation_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request.on_json_loading_failed = on_json_loading_failed_return_dict
        print(datetime.datetime.now(), ": ============================ START ============================")
        print(datetime.datetime.now(), ":", "function::", f.__name__)
        print(datetime.datetime.now(), ":", "url:", request.path)
        print(datetime.datetime.now(), ":", "data:", request.get_json(), type(request.get_json()))
        result = f(*args, **kwargs)
        print(datetime.datetime.now(), ": ============================ END ============================")					# 9)

        return result
    return decorated_function


def log(param):
    print(now(), ":", param)


def now():
    return datetime.datetime.now()