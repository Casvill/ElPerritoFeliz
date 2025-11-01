from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Envía un correo con el token de restablecimiento de contraseña
    """
    email_plaintext_message = f"""
                                    Hola 👋

                                    Has solicitado restablecer tu contraseña en El Perrito Feliz 🐶

                                    Usa este token para continuar con el proceso:
                                    {reset_password_token.key}

                                    Si tú no solicitaste esto, ignora este mensaje.
                                """

    send_mail(
        "Recuperación de contraseña - El Perrito Feliz 🐶",
        email_plaintext_message,
        settings.DEFAULT_FROM_EMAIL,
        [reset_password_token.user.email],
    )
