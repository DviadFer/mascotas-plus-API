
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Tcompanion
from .models import Tuser
from .models import Twalk
import smtplib, ssl

@csrf_exempt

def request_companion(request, id):

# Compruebo que el método sea POST

	if request.method !='POST':
		return JsonResponse(status=405, data={'error': 'Invalid method'})

# Capturo el parámetro token y compruebo que se llega con la petición
	try:
		mi_token = request.headers['token']
	except KeyError:
		return JsonResponse(status=401, data={'error': 'Missing token'})

# Capturo el mensaje que se envia en el cuerpo de la  petición y compruebo que se llega en la peticioón
	json_body = json.loads(request.body)
	try:
		mensaje = json_body['message']
	except KeyError:
		return JsonResponse (status=400, data={'error': 'Missing parameter'})

# Guardo el id que viene en el path de la petición en la variable id_paseo
	id_paseo = id

# Compruebo que existe us usuario en la tabla de usuarios de la base de datos con el token que viene en la petición
	try:
		usuario = Tuser.objects.get(active_session_token = mi_token)
	except Tuser.DoesNotExist:
		return JsonResponse(status=403, data={'error': 'Invalid token'})

# Compruebo que existe un paseo con el id que viene en la petición
	try:
		paseo = Twalk.objects.get(id = id_paseo)
	except Twalk.DoesNotExist:
		return JsonResponse(status=404 , data={'error': 'Walk does not exist'})

# Creo la fila que se va a guardar en la base de datos cuando el endpoint se ejecuta correctamente

	fila_companion = Tcompanion(
		requester = usuario,
		walk = paseo,
		message = mensaje,
		is_accepted = False
 	)
# Guardo en la base de datos
	fila_companion.save()

#	print(mensaje)
#	print(usuario.id)
#	print(paseo.id)
	return JsonResponse(status=201, data={})

@csrf_exempt

def accept_request(request,id,request_id):

# Compruebo que el método de la petición sea POST 
	if request.method !='POST':
                return JsonResponse(status=405, data={'error': 'Invalid method'})

# Compruebo que en el header de la petición viene un token y lo guardo en la variable mi_token
	try:
                mi_token = request.headers['token']
	except KeyError:
		return JsonResponse(status=401, data={'error': 'Missing token'})

# Guardo los id que vienen el el path de la petición en dos variables id_paseo y id_peticion
	id_paseo = id
	id_peticion = request_id

# Compruebo que en la base de datos hay un usuario con el token que viene en la petición
	try:
		usuario = Tuser.objects.get(active_session_token = mi_token)
	except Tuser.DoesNotExist:
		return JsonResponse(status=403, data={'error': 'Invalid token'})

# Compruebo que existe una petición con el id_peticion que viene en el path  
	try:
		peticion = Tcompanion.objects.get(id = request_id)
	except Tcompanion.DoesNotExist:
		return JsonResponse(status=404 , data={'error': 'Request does not exist'})

# Compruebo que existe un paseo en la base de datos con el id_paseo que viene en el path
	try:
		paseo = Twalk.objects.get(id = id_paseo)
	except Twalk.DoesNotExist:
		return JsonResponse(status=404 , data={'error': 'Walk does not exist'})

# Modifico el valor de is_accepted de la base de datos de la tabla tCompanion a True

	peticion.is_accepted = True
	peticion.save()

# Capturo los datos que necesito para enviar el correo de confirmación al usuario que realizó la petición que es aceptada

	companion_user = Tuser.objects.get(id=peticion.requester_id)
	email_companion = companion_user.email
	user_name = usuario.name
	user_surname = usuario.surname
	latitud = paseo.latitude
	longitud = paseo.longitude
	hora = paseo.datetime

#	print(companion_user.email)
#	print(peticion)
#	print(usuario.id)
#	print(paseo.id)

# Envio el correo de confirmación

	receiver = email_companion
	sender = "t2notifications_no_reply@fpcoruna.afundacion.org"
	password = "Password"
	message = """Subject: Peticion paseo aceptada.

	Tu peticion ha sido aceptada.

	Datos del paseo:

		Nombre del organizador:"""+user_name+"""
		Apellidos: """+user_surname+"""
		Localizacion:
			Latitud: """+str(latitud)+"""
			Longitud: """+str(longitud)+"""
			Hora:"""+str(hora)+"""

	Este correo es automatico, no envie ningun mensaje.
	"""

	port = 587
	server = "smtp.gmail.com"

	context = ssl.create_default_context()
	with smtplib.SMTP(server, port) as server:
		server.starttls(context=context)
		server.login(sender, password)
		server.sendmail(sender, receiver, message)

	return JsonResponse(status=201, data={})

