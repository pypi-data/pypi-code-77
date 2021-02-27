import json
from pyx.tags import render_error, __html__
from pyx.main import __requests__, __DOM__
from flask import Flask, request, jsonify, abort, make_response


__APP__ = Flask(__name__)


def render(body: str):
    return str(__html__(children=body))


def _from_request(target, html):
    return jsonify(dict(
        target=target,
        html=str(html)
    ))


@__APP__.route('/pyx/<name>', methods=['GET', 'POST'])
def __pyx__requests__(name):
    _error_status = 500
    req = __requests__.get(name)
    kw = dict(request.args) | dict(json.loads(request.data))
    try:
        if not req:
            _error_status = 400
            raise ConnectionError('Bad Request')
        _id = kw.pop('id')
        print(req(**kw))
        # tag_name = req.__qualname__.split('.')[0].lower()
        # if local_tag := locals().get(tag_name):
        #     _id = str(hash(local_tag))
        return _from_request(_id, __DOM__[_id]())
    except Exception as error:
        return abort(make_response(_from_request('error', render_error(traceback=str(error), **kw)), 500))


def run_app(*a, **k):
    return __APP__.run(*a, **(k or dict(debug=True)))

# TODO: add FastAPI app
