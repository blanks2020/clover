
from flask import jsonify
from flask import request
from flask import render_template

from clover.interface import interface
from clover.interface.service import Service


@interface.route('/', strict_slashes=False)
@interface.route('/index', strict_slashes=False)
def index():
    return render_template("interface.html")


@interface.route('/api/v1/debug', methods=['POST'], strict_slashes=False)
def api_v1_debug():
    # get请求使用request.values.to_dict接收
    # post、put、delete使用request.get_json接收
    data = request.get_json()
    print(data)

    method = data['request'].get('method', None)
    if not method:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [method]',
            'data': data,
        })

    host = data['request'].get('host', None)
    if not host:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [host]',
            'data': data,
        })

    path = data['request'].get('path', None)
    if not path:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [path]',
            'data': data,
        })

    try:
        service = Service()
        data = service.execute(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data,
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })


@interface.route('/api/v1/save', methods=['POST'], strict_slashes=False)
def api_v1_save():
    # get请求使用request.values.to_dict接收
    # post、put、delete使用request.get_json接收
    data = request.get_json()

    method = data['request'].get('method', None)
    if not method:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [method]',
            'data': data,
        })

    host = data['request'].get('host', None)
    if not host:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [host]',
            'data': data,
        })

    path = data['request'].get('path', None)
    if not path:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [path]',
            'data': data,
        })

    try:
        service = Service()
        case_id = service.save(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': case_id,
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })


@interface.route('/api/v1/trigger', methods=['GET', 'POST'], strict_slashes=False)
def api_v1_trigger():
    # 这里支持GET与POST请求，获取参数方法不同。
    if request.method == 'GET':
        data = request.values.to_dict()
    else:
        data = request.get_json()

    cases = data.get('cases', None)
    if not cases:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [cases]',
            'data': data,
        })

    try:
        service = Service()
        result = service.trigger(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })

"""
# 列表页部分
"""


@interface.route('/list', strict_slashes=False)
def list():
    return render_template('list.html')


@interface.route('/api/v1/list', methods=['GET', 'POST'], strict_slashes=False)
def api_v1_list():

    if request.method == 'GET':
        data = request.values.to_dict()
    else:
        data = request.get_json()

    try:
        result = Service().list(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })
