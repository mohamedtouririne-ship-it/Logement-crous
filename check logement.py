import os
import smtplib
import sys
from email.mime.text import MIMEText

import requests

URL = (
    "https://trouverunlogement.lescrous.fr/tools/47/search"
    "?occupationModes=alone"
    "&bounds=3.8070597_43.6533542_3.9413208_43.5667088"
    "&locationName=Montpellier"
)

# Texte affiché sur la page quand il n'y a AUCUN logement disponible
NO_RESULTS_TEXT = "Aucun logement trouvé"


def check_logements():
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    response.raise_for_status()
    page_content = response.text

    if NO_RESULTS_TEXT in page_content:
        print("Aucun logement disponible pour le moment.")
        return False

    print("Des logements semblent disponibles !")
    return True


def send_email_alert():
    sender_email = os.environ["EMAIL_SENDER"]
    sender_password = os.environ["EMAIL_PASSWORD"]
    receiver_email = os.environ["EMAIL_RECEIVER"]

    subject = "🏠 Logement CROUS disponible à Montpellier !"
    body = (
        "Un ou plusieurs logements semblent disponibles pour une "
        "cohabitation individuelle à Montpellier.\n\n"
        f"Va vérifier ici :\n{URL}"
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email d'alerte envoyé.")


if __name__ == "__main__":
    try:
        found = check_logements()
    except Exception as e:
        print(f"Erreur lors de la vérification : {e}")
        sys.exit(1)

    if found:
        send_email_alert()
