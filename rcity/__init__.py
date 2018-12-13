from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xde:J0w\x98|~\x80\xc8z\x8fC\x93,f\x93\xa5?w'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run(debug=True)

import views