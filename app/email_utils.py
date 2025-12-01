import os
import smtplib
import ssl
from email.message import EmailMessage
from typing import Optional
import traceback


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL") or SMTP_USER


def _build_welcome_email(to_email: str, nombre: str) -> EmailMessage:
    asunto = "Usuario creado correctamente"
    cuerpo = (
        f"Hola {nombre},\n\n"
        "Tu usuario ha sido creado correctamente en el sistema de CRUD de Personas.\n\n"
        "Si tú no solicitaste este registro, puedes ignorar este correo.\n\n"
        "Saludos,\n"
        "Equipo CRUD de Personas"
    )

    mensaje = EmailMessage()
    mensaje["Subject"] = asunto
    mensaje["From"] = FROM_EMAIL
    mensaje["To"] = to_email
    mensaje.set_content(cuerpo)

    return mensaje


def send_welcome_email(to_email: Optional[str], nombre: str) -> None:
    """
    Envía un correo de bienvenida si hay email configurado y destino válido.
    Pensado para ejecutarse en background (no bloquea la respuesta de la API).
    """
    if not to_email:
        return

    if not (SMTP_HOST and SMTP_USER and SMTP_PASSWORD and FROM_EMAIL):
        print("⚠️ Config SMTP incompleta:",
            SMTP_HOST, SMTP_USER, FROM_EMAIL)
        return


    mensaje = _build_welcome_email(to_email, nombre)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(mensaje)
        print(f"✅ Correo de bienvenida enviado a {to_email}")
    except Exception as e:
        print("❌ Error enviando correo:", repr(e))
        traceback.print_exc()

