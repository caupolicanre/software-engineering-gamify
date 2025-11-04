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
        # Usar el nuevo endpoint de estadísticas
        response = requests.get(
            f"{API_BASE_URL}/achievements/user-stats/",
            params={"user_id": DEMO_USER_ID},
            timeout=5,
        )
        response.raise_for_status()
        stats = response.json()

        # Contar logros desbloqueados
        achievements_response = requests.get(
            f"{API_BASE_URL}/achievements/all-progress/",
            params={"user_id": DEMO_USER_ID},
            timeout=5,
        )

        unlocked_count = 0
        if achievements_response.status_code == 200:
            achievements = achievements_response.json()
            results = achievements.get("results", achievements) if isinstance(achievements, dict) else achievements
            unlocked_count = sum(1 for ach in results if ach.get("is_unlocked"))

        return jsonify(
            {
                "tasks_completed": stats.get("total_tasks_completed", 0),
                "current_streak": stats.get("current_streak", 0),
                "longest_streak": stats.get("longest_streak", 0),
                "current_level": stats.get("current_level", 1),
                "achievements_unlocked": unlocked_count,
                "total_xp": stats.get("total_xp", 0),
            }
        )
    except requests.RequestException as e:
        return (
            jsonify(
                {
                    "error": str(e),
                    "tasks_completed": 0,
                    "current_streak": 0,
                    "longest_streak": 0,
                    "current_level": 1,
                    "achievements_unlocked": 0,
                    "total_xp": 0,
                }
            ),
            500,
        )


@app.route("/api/simulate-task", methods=["POST"])
def simulate_task():
    """Simular la completación de tareas usando el nuevo endpoint."""
    try:
        data = request.get_json()
        task_count = data.get("count", 1)

        # Usar el nuevo endpoint de simulación de tareas
        response = requests.post(
            f"{API_BASE_URL}/achievements/simulate-tasks/",
            json={
                "user_id": DEMO_USER_ID,
                "count": task_count,
                "update_streak": True,
            },
            timeout=10,
        )

        if response.status_code == 200:
            result = response.json()
            return jsonify(
                {
                    "success": True,
                    "message": result.get("message", f"Simuladas {task_count} tareas"),
                    "tasks_completed": result.get("tasks_completed", task_count),
                    "total_tasks_completed": result.get("total_tasks_completed", 0),
                    "current_streak": result.get("current_streak", 0),
                    "current_level": result.get("current_level", 1),
                    "total_xp": result.get("total_xp", 0),
                    "achievements_unlocked": result.get("achievements_unlocked", 0),
                    "unlocked_achievements": result.get("unlocked_achievements", []),
                }
            )
        return jsonify({"success": False, "error": "Error al simular tareas"}), response.status_code

    except requests.RequestException as e:
        return jsonify({"error": str(e), "success": False}), 500


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
