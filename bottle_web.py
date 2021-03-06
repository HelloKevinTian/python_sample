from bottle import route, run, template


@route('/')
def hello():
    return "Hello World!"

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='0.0.0.0', port=8080)