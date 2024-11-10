import requests



def file(links):
    for url, save_path in links:
        response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"file salvato con successo in {save_path}")
    else:
        print(f"Errore: impossibile scaricare il file da {url}. Status code: {response.status_code}")

links = [
    ("https://raw.githubusercontent.com/morad200120/sito_italiano/refs/heads/main/main.py", "/home/giornalemattei/mysite/giornalemattei.py"),
    ("https://raw.githubusercontent.com/morad200120/sito_italiano/refs/heads/main/templates/desktop_index.html", "/home/giornalemattei/mysite/templates/desktop_index.html"),
    ]

file(links)