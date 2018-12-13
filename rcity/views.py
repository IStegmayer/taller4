from rcity import app

@app.route('/')
@app.route('/index')
def index():
    return "<h1>Hola!</h1>"