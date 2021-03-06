from flask import Flask,request,render_template
from flask_bootstrap import Bootstrap
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import BadRequest
import os

# Init app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
Bootstrap(app)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

