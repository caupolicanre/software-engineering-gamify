"""
Configuración para la aplicación de demostración.
Puedes modificar estos valores según tus necesidades.
"""

# URL base de la API Django
API_BASE_URL = "http://localhost:8000/api/v1"

# ID del usuario de demostración (superusuario)
DEMO_USER_ID = 1

# Puerto donde correrá Flask
FLASK_PORT = 5000

# Modo debug (True para desarrollo, False para producción)
FLASK_DEBUG = True

# Timeout para peticiones HTTP (segundos)
REQUEST_TIMEOUT = 5

# Colores de rareza para la interfaz
RARITY_COLORS = {
    "common": "secondary",
    "rare": "info",
    "epic": "primary",
    "legendary": "warning",
}

# Iconos de Bootstrap para estadísticas
STAT_ICONS = {
    "tasks": "bi-check-circle-fill",
    "streak": "bi-fire",
    "achievements": "bi-trophy",
    "xp": "bi-star-fill",
}
