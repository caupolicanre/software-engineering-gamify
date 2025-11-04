"""Script para verificar que la demo está lista para ejecutarse."""

import sys

import requests


def check_django_api():
    """Verifica que la API Django esté disponible."""
    print("🔍 Verificando API Django en http://localhost:8000...")
    try:
        response = requests.get("http://localhost:8000/api/v1/achievements/", timeout=5)
        if response.status_code == 200:
            print("✅ API Django funcionando correctamente")
            data = response.json()
            count = len(data.get("results", []))
            print(f"   📊 {count} logros disponibles")
            return True
        print(f"❌ API Django respondió con código {response.status_code}")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a Django. ¿Está corriendo en puerto 8000?")
        print("   💡 Ejecuta: uv run python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def check_achievements():
    """Verifica que haya logros creados."""
    print("\n🏆 Verificando logros...")
    try:
        response = requests.get("http://localhost:8000/api/v1/achievements/", timeout=5)
        data = response.json()
        results = data.get("results", [])

        if len(results) > 0:
            print(f"✅ {len(results)} logros encontrados")
            for achievement in results[:3]:  # Mostrar primeros 3
                print(f"   • {achievement['name']} ({achievement['rarity']})")
            return True
        print("⚠️  No hay logros creados")
        print("   💡 Ejecuta: uv run python manage.py create_sample_achievements")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def check_flask_available():
    """Verifica que Flask esté instalado."""
    print("\n🌐 Verificando Flask...")
    try:
        import flask  # noqa: F401

        print("✅ Flask instalado correctamente")
        return True
    except ImportError:
        print("❌ Flask no está instalado")
        print("   💡 Ejecuta: uv add flask requests")
        return False


def main():
    """Ejecutar todas las verificaciones."""
    print("=" * 60)
    print("  🎮 Gamify Achievement System - Verificación de Demo")
    print("=" * 60)

    checks = [check_flask_available(), check_django_api(), check_achievements()]

    print("\n" + "=" * 60)
    if all(checks):
        print("✅ ¡Todo listo para la demo!")
        print("\n📋 Pasos siguientes:")
        print("   1. Ejecuta: uv run python demo_app.py")
        print("   2. Abre: http://localhost:5000")
        print("=" * 60)
        return 0
    print("❌ Hay problemas que resolver antes de ejecutar la demo")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    sys.exit(main())
