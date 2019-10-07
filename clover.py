#coding=utf-8

from flask import Flask
from flask import jsonify
from flask import render_template

from environment import environment
from automation import automation
from interface import interface

app = Flask(__name__)
app.config.from_object('config')

app.logger.info("load config {0}".format(app.config))


app.register_blueprint(environment)
app.register_blueprint(automation)
app.register_blueprint(interface)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/info")
def info():
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': {
            'author': "taoyanli0808",
            'introduce': "A Simple and Easy-to-Use Automated Testing Platform",
            # 'config': app.config,
            'function': {
                'automation': {
                    'version': "0.1.00",
                    'dependence': "3.141.0",
                },
                'interface': {
                    'version': "0.0.00",
                    'requests': "2.18.3",
                }
            }
        }
    })


if __name__ == '__main__':
    app.run(
        host=app.config['SERVER']['HOST'],
        port=app.config['SERVER']['PORT'],
        debug=app.config['SERVER']['DEBUG']
    )