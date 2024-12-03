from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_talisman import Talisman
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import user_agents
import mysql.connector
import os
from datetime import timedelta
import logging

def get_database_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="database_sito_italiano"
        )
        return conn
    except mysql.connector.Error as err:
        flash(f"Errore di connessione al database: {err}", "error")
        return None

app = Flask(__name__)
Talisman(app)
app.secret_key = "s2f2h4*%!81l#-nirpxe#*fd9-!+=&0$ix=!8do%zot**z-p"


app.config["UPLOAD_FOLDER"] = "static/immagini_caricate"  
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)  
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  


logging.basicConfig(level=logging.DEBUG)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#-------------------------------------------------------------------------------

username = "admin"
hashed_password = generate_password_hash("admin", method="pbkdf2:sha256", salt_length=8)

#-------------------------------------------------------------------------------

def redirect_based_on_device(pc_route, mobile_route):
    user_agent = request.headers.get("User-Agent")
    ua = user_agents.parse(user_agent)
    return redirect(url_for(pc_route if ua.is_pc else mobile_route))

def login_required(f):
    def wrap(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

#-------------------------------------------------------------------------------

@app.route("/")
def index():
    return redirect_based_on_device("desktop_page", "mobile_page")

@app.route("/add_article", methods=["POST"])
def aggiungi_articolo():
    if request.method == "POST":
        username_inserito = request.form.get("username")
        password_inserita = request.form.get("password")

        if username_inserito == username and check_password_hash(hashed_password, password_inserita):
            session["logged_in"] = True
            return redirect_based_on_device("add_article_desktop_page", "add_article_mobile_page")
        else:
            session["logged_in"] = False
            return redirect(url_for("index"))


@app.route("/submit_article", methods=["POST"])
def submit_article():

    conn = get_database_connection()
    if conn is None:
        flash("Connessione al database fallita, contattami o  riprova fra un po", "error")
        return redirect_based_on_device("add_article_desktop_page", "add_article_mobile_page")
    
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()
    genere = request.form.get("genere", "").strip()
    image = request.files.get("image")


    if not title or not url or not genere or not image:
        flash("Tutti i campi sono obbligatori!", "error")
        return redirect_based_on_device("add_article_desktop_page", "add_article_mobile_page")

    if image.filename == '':
        flash("Nessun file selezionato!", "error")
        return redirect_based_on_device("add_article_desktop_page", "add_article_mobile_page")


    if not allowed_file(image.filename):
        flash("Tipo di file non consentito! Carica un'immagine valida (png, jpg, jpeg, gif).", "error")
        return redirect_based_on_device("add_article_desktop_page", "add_article_mobile_page")


    image_filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)


    try:
        image.save(image_path)
    except Exception as e:
        flash(f"Errore nel salvataggio dell'immagine: {e}", "error")
        return redirect_based_on_device("add_article_desktop_page", "add_article_mobile_page")

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO articoli (title, url, genere, image_path)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (title, url, genere, image_path))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f"Errore nel salvataggio dell'articolo contattami o riprova fra qualche minuto: {e}", "error")
        return redirect_based_on_device("add_article_desktop_page", "add_article_mobile_page")
    finally:
        cursor.close()
        conn.close()

    flash("Articolo caricato con successo!", "success")
    return redirect_based_on_device("desktop_page", "mobile_page")

#-------------------------------------------------------------------------------

@app.route("/desktop_page")
def desktop_page():
    return render_template("desktop_index.html")

@app.route("/mobile_page")
def mobile_page():
    return render_template("mobile_index.html")

@app.route("/desktop_add_article")
@login_required
def add_article_desktop_page():
    return render_template("desktop_add_article.html")

@app.route("/mobile_add_article")
@login_required
def add_article_mobile_page():
    return render_template("mobile_add_article.html")

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
