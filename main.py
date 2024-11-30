from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_talisman import Talisman
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import user_agents
import mysql.connector
import os
from datetime import timedelta
import logging

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="database_sito_italiano"
)
cursor = conn.cursor()

app = Flask(__name__)
Talisman(app)
app.secret_key = "s2f2h4*%!81l#-nirpxe#*fd9-!+=&0$ix=!8do%zot**z-p"

# Configura la cartella di upload per le immagini
app.config["UPLOAD_FOLDER"] = "static/immagini_caricate"  # Cartella di upload separata
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)  # Assicurati che la cartella esista
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limita la dimensione a 16 MB

# Configura il logging
logging.basicConfig(level=logging.DEBUG)

# Definisci estensioni consentite
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Funzione per controllare le estensioni dei file
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
    title = request.form["title"]
    url = request.form["url"]
    genere = request.form["genere"]
    
    image = request.files["image"]
    
    image_path = None
    if image:
        if image.filename != '' and allowed_file(image.filename):
            # Proteggi il nome del file
            filename = secure_filename(image.filename)
            # Salva l'immagine nella cartella di upload
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        else:
            flash("Tipo di file non supportato. Carica un'immagine.", "error")
            return redirect(request.url)
    
    try:
        query = """
        INSERT INTO articoli (title, url, genere, image_path)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (title, url, genere, filename if image else None))
        conn.commit()  # Salva le modifiche nel database
    except mysql.connector.Error as e:
        conn.rollback()  # Fai il rollback in caso di errore
        flash(f"Errore nel salvataggio dell'articolo: {e}", "error")
        return redirect(request.url)
    finally:
        cursor.close()  # Chiudi il cursore
        conn.close()    # Chiudi la connessione al database

    return redirect(url_for("index"))

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
