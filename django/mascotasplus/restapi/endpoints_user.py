from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Tuser
import secrets
import bcrypt
from requests.auth import HTTPBasicAuth


@csrf_exempt
def register(request):
    json_body = json.loads(request.body)
    nombre = json_body['name']
    apellido = json_body['surname']
    mail = json_body['email']
    contrasena = json_body['password']
    if request.method == 'POST':
        try:
            Tuser.objects.get(email = mail)
        except Tuser.DoesNotExist:
            # El usuario no existe aun con ese email en BBDD. OK, seguimos adelante
            encrypted_pass = bcrypt.hashpw(contrasena.encode("utf8"), bcrypt.gensalt()).decode("utf8")
            usuario = Tuser(name = nombre, surname = apellido, email = mail, encrypted_password = encrypted_pass)
            usuario.save()
            return JsonResponse(status=201, data={})

        return JsonResponse(status=409, data={})
    return JsonResponse(status=405, data={})



@csrf_exempt
def login(request):
    json_body = json.loads(request.body)
    email_p = json_body['email']
    password_p = json_body['password']
    #active_session_token_p = json_body['active_session_token']
    mi_token = secrets.token_hex(6)

    if request.method == 'POST':
        try:
            fila_usuario = Tuser.objects.get(email = email_p)
            if bcrypt.checkpw(password_p.encode("utf8"), fila_usuario.encrypted_password.encode("utf8")):
                # OK, las pasword_p coincide con la almacenada previamente (register endpoint) en BBDD
                fila_usuario.active_session_token = mi_token
                fila_usuario.save()
                return JsonResponse(status=201, data={"user_id": fila_usuario.id, "name": fila_usuario.name, "token": mi_token})
            else:
                # La comprobacion de la password ha devuelto False
                return JsonResponse(status=401, data={})

        except Tuser.DoesNotExist:
            return JsonResponse(status=404, data={})
    else:
        return JsonResponse(status=405, data={})
