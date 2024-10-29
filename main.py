from flask import Flask, render_template, request, redirect, url_for, flash, session
import user_agents

app = Flask(__name__)
app.secret_key = "s2f2h4*%!)81l#-nirpxe#*fd9-!+=&)0$ix=!8do%zot**z-p"

@app.route("/")
def ottieni_ua():
    user_agent = request.headers.get("User-Agent")
    ua = user_agents.parse(user_agent)

    if ua.is_pc:
        return redirect(url_for("desktop_page"))
    else:
        return redirect(url_for("mobile_page"))


@app.route("/desktop_page", methods=["GET"])
def desktop_page():
    return render_template("desktop_index.html")

@app.route("/mobile_page", methods=["GET"])
def mobile_page():
    return render_template("mobile_index.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

