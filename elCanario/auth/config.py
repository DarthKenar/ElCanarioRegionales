from django.urls import reverse_lazy


LOGIN_REDIRECT_URL = reverse_lazy("core:home")
LOGOUT_REDIRECT_URL = reverse_lazy("core:home")


def INSTALLED_APPS_update(INSTALLED_APPS: list[str]):
    INSTALLED_APPS += [
        "allauth",
        "allauth.account",
        "allauth.socialaccount",
        "allauth.socialaccount.providers.google",
    ]
    return INSTALLED_APPS


def MIDDLEWARE_update(MIDDLEWARE: list):
    MIDDLEWARE += ["allauth.account.middleware.AccountMiddleware"]
    return MIDDLEWARE


def TEMPLATES_update(TEMPLATES: list[dict[str, dict[str, list]]]):
    TEMPLATES[0]["OPTIONS"]["context_processors"].append("django.template.context_processors.request")
    return TEMPLATES


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# * Configuración de cuentas locales
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180  # segundos para que no se pueda reenviar otro correo
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 60  # segundos de espera una vez que se superó el límite de intentos
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True  # se loguea automáticamente una vez confirmado el email
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True  # se loguea automáticamente una vez cambiado el password
# ACCOUNT_USER_DISPLAY (default: user.username)
# ACCOUNT_USER_MODEL_EMAIL_FIELD (default: "email")
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # (default: "username")
ACCOUNT_USERNAME_REQUIRED = False

# * Configuración de cuentas sociales
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
# Considerar que se produce un inicio de sesión "social" y la cuenta social viene con una dirección
# de correo electrónico verificada (verificada por el proveedor de la cuenta),
# pero esa dirección de correo electrónico ya está tomada por una cuenta de usuario "local".
# Además, la cuenta de usuario local puede no tiene ninguna cuenta social conectada.
# Ahora bien, si se confía plenamente en el proveedor, deberíamos tratar
# este escenario como un inicio de sesión en la cuenta de usuario local existente,
# incluso si la cuenta local aún no tiene la cuenta social conectada,
# porque, según el proveedor, el el usuario que inicia sesión
# tiene la propiedad de la dirección de correo electrónico.
# Así es como se maneja este escenario cuando SOCIALACCOUNT_EMAIL_AUTHENTICATION se establece en Verdadero.
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
# En caso de que se aplique la autenticación de correo electrónico,
# esta configuración controla si la cuenta social se conecta automáticamente o no a la cuenta local.
# En caso de Falso, la cuenta local permanece sin cambios durante el inicio de sesión.
# En el caso de Verdadero, la cuenta social con la que coincidió el correo electrónico
# se agrega automáticamente a la lista de cuentas sociales conectadas a la cuenta local.
# Como resultado, incluso si el usuario cambiara la dirección de correo electrónico posteriormente,
# el inicio de sesión social aún sería posible cuando se utiliza True, pero no en el caso de False.

ACCOUNT_EMAIL_VERIFICATION = "optional"
SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_UNIQUE_EMAIL = True

# https://github.com/mdrhmn/dj-social-auth
# link documentacion para logearse con cuentas de google.

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
    }
}
