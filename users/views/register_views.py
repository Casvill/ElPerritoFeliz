#----------------------------------------------
# views_register.py
#----------------------------------------------
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..models import Usuario   # ✅ tu modelo personalizado
#----------------------------------------------

#----------------------------------------------
# Verificar si el correo ya está registrado
#----------------------------------------------
@csrf_exempt
def check_email(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    try:
        data = json.loads(request.body)
        print("📦 Datos recibidos en check_email:", data)

        email = data.get("email") or data.get("correo")
        email = (email or "").strip().lower()

        exists = Usuario.objects.filter(email=email).exists()
        print(f"📬 Verificando correo: {email} -> Existe: {exists}")

        return JsonResponse({"exists": exists})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

#----------------------------------------------
# Verificar si el documento ya está registrado
#----------------------------------------------
@csrf_exempt
def check_documento(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    try:
        data = json.loads(request.body)
        print("📦 Datos recibidos en check_documento:", data)

        documento = data.get("documento") or data.get("nroDoc")
        exists = Usuario.objects.filter(documento=documento).exists()
        print(f"📬 Verificando documento: {documento} -> Existe: {exists}")

        return JsonResponse({"exists": exists})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

#----------------------------------------------
# Registrar nuevo usuario
#----------------------------------------------
@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        print("📦 Datos recibidos en register_user:", data)

        # Extraer datos del JSON
        nombres = data.get("firstName")
        apellidos = data.get("lastName")
        tipo_doc = data.get("documentType")
        documento = data.get("documentNumber")
        telefono = data.get("phone")
        email = data.get("email")
        direccion = data.get("address")
        password = data.get("password")

        # Validaciones básicas
        if not all([nombres, apellidos, documento, email, password]):
            return JsonResponse({"error": "Faltan campos requeridos"}, status=400)

        if Usuario.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email ya registrado"}, status=409)

        if Usuario.objects.filter(documento=documento).exists():
            return JsonResponse({"error": "Documento ya registrado"}, status=409)

        # Crear usuario
        user = Usuario.objects.create_user(
            documento=documento,
            password=password,
            nombres=nombres,
            apellidos=apellidos,
            tipo_usuario=Usuario.CLIENTE,   # 👈 por defecto, lo puedes ajustar
            telefono=telefono or "",
            email=email,
            direccion=direccion or "",
        )

        return JsonResponse({
            "msg": "Usuario creado correctamente",
            "user": {
                "id": user.id_usuario,
                "documento": user.documento,
                "email": user.email,
                "nombres": user.nombres,
                "apellidos": user.apellidos,
                "tipo_usuario": user.tipo_usuario,
            }
        }, status=201)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)

#----------------------------------------------
