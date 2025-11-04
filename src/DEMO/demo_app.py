"""Flask Demo App for Achievement System Testing."""

import requests
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

# Configuración - URL base de la API Django
API_BASE_URL = "http://localhost:8000/api/v1"
DEMO_USER_ID = 1  # Superusuario creado


@app.route("/")
def index():
    """Página principal de la demo."""
    return render_template("index.html")


@app.route("/static/<path:filename>")
def static_files(filename):
    """Servir archivos estáticos."""
    return app.send_static_file(filename)


@app.route("/api/achievements")
def get_achievements():
    """Obtener todos los logros disponibles."""
    try:
        response = requests.get(f"{API_BASE_URL}/achievements/", timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/user-achievements")
def get_user_achievements():
    """Obtener logros del usuario con progreso."""
    try:
        # Obtener todos los logros con progreso
        response = requests.get(
            f"{API_BASE_URL}/achievements/all-progress/",
            params={"user_id": DEMO_USER_ID},
            timeout=5,
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/user-stats")
def get_user_stats():
    """Obtener estadísticas del usuario."""
    try:
        # Obtener todos los logros con progreso del usuario
        response = requests.get(
            f"{API_BASE_URL}/achievements/all-progress/",
            params={"user_id": DEMO_USER_ID},
            timeout=5,
        )

        # Si falla, intentar endpoint alternativo
        if response.status_code != 200:
            response = requests.get(f"{API_BASE_URL}/achievements/", timeout=5)

        response.raise_for_status()

        # Retornar estadísticas basadas en logros desbloqueados
        data = response.json()
        unlocked_count = 0
        total_xp = 0
        tasks_completed = 0

        results = data.get("results", data) if isinstance(data, dict) else data

        for achievement in results:
            if achievement.get("is_unlocked"):
                unlocked_count += 1
                total_xp += achievement.get("reward_xp", 0)

            # Obtener el máximo de tareas completadas del progreso
            progress = achievement.get("progress", 0)
            criteria_type = achievement.get("criteria", {}).get("type", "")
            if criteria_type == "task_count" and progress > tasks_completed:
                tasks_completed = progress

        return jsonify(
            {
                "tasks_completed": tasks_completed,
                "current_streak": 0,  # Se actualizará con rachas reales
                "achievements_unlocked": unlocked_count,
                "total_xp": total_xp,
            }
        )
    except requests.RequestException as e:
        return (
            jsonify(
                {
                    "error": str(e),
                    "tasks_completed": 0,
                    "current_streak": 0,
                    "achievements_unlocked": 0,
                    "total_xp": 0,
                }
            ),
            500,
        )


@app.route("/api/simulate-task", methods=["POST"])
def simulate_task():
    """Simular la completación de tareas."""
    try:
        data = request.get_json()
        task_count = data.get("count", 1)

        # Llamar al comando de Django para simular tareas
        # (Esto requeriría ejecutar el comando manage.py, lo simularemos con la API)

        # Por ahora, retornamos éxito y el frontend consultará los logros actualizados
        return jsonify(
            {
                "success": True,
                "message": f"Simuladas {task_count} tareas completadas",
                "tasks_completed": task_count,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/unlock-achievement", methods=["POST"])
def unlock_achievement():
    """Desbloquear un logro manualmente (para testing)."""
    try:
        data = request.get_json()
        achievement_id = data.get("achievement_id")

        response = requests.post(
            f"{API_BASE_URL}/achievements/unlock/",
            json={"achievement_id": achievement_id, "user_id": DEMO_USER_ID},
            timeout=5,
        )

        if response.status_code in [200, 201]:
            return jsonify({"success": True, "data": response.json()})
        return jsonify({"success": False, "error": "Failed to unlock achievement"}), response.status_code

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("=" * 60)
    print("🎮 Gamify Achievement System - Demo App")
    print("=" * 60)
    print("📍 Demo URL: http://localhost:5000")
    print("🔧 Django API debe estar corriendo en http://localhost:8000")
    print("👤 Usuario de prueba: ID = 1 (superusuario)")
    print("=" * 60)
    app.run(debug=True, port=5000)
