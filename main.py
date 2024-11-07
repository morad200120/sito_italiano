from flask import Flask, render_template, request, redirect, url_for
import user_agents

app = Flask(__name__)
app.secret_key = "s2f2h4*%!)81l#-nirpxe#*fd9-!+=&)0$ix=!8do%zot**z-p"

#-------------------------------------------------------------------------------

def redirect_based_on_device(pc_route, mobile_route):
    user_agent = request.headers.get("User-Agent")
    ua = user_agents.parse(user_agent)
    return redirect(url_for(pc_route if ua.is_pc else mobile_route))

#-------------------------------------------------------------------------------

@app.route("/")
def index():
    return redirect_based_on_device("desktop_page", "mobile_page")

@app.route("/aggiungi_articolo", methods=["GET"])
def aggiungi_articolo():
    return redirect_based_on_device("desktop_login", "mobile_login")

#-------------------------------------------------------------------------------

@app.route("/desktop_page")
def desktop_page():
    return render_template("desktop_index.html")

@app.route("/mobile_page")
def mobile_page():
    return render_template("mobile_index.html")

@app.route("/login_desktop")
def desktop_login():
    return render_template("desktop_login.html")

@app.route("/login_mobile")
def mobile_login():
    return render_template("mobile_login.html")

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
