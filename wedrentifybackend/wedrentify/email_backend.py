import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


class CustomEmailBackend(SMTPBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🚨 Nuclear Option: Create a context that ignores ALL verification 🚨
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Assign this "loose" context to the backend so Django uses it automatically
        self.ssl_context = ctx