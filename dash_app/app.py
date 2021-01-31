from flask import Flask
from flask import render_template,redirect
from app1 import f1,f2
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

#### Configuration =================================================
server = Flask(__name__)
dash_app1 = f1(server)
dash_app2 = f2(server)
# server2 = Flask(__name__)
# app2 = model.execute_2(server2)

@server.route("/")
def home():
    return redirect('/dash1/')

@server.route("/reports/")
def home2():
    return redirect('/dash2/')

@server.route("/index/")
def home3():
    return redirect("/reports/")

@server.route("/another/")
def another():
    return render_template("test.html")

app = DispatcherMiddleware(server, {
    '/dash1/': dash_app1.server,
    '/dash2/': dash_app2.server
})

if __name__ == "__main__":
    run_simple('127.0.0.1',5000, app, use_reloader=True, use_debugger=True)