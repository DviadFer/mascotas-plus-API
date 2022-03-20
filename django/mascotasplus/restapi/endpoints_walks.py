from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
import json
from datetime import datetime
from .models import Twalk, Tuser
from .formula_haversine import calcularDistancia

@csrf_exempt
def request_walk(request):
	if request.method == 'GET':
		try:
			token = request.headers['token']
		except KeyError:
			return JsonResponse(status=401, data={'Error': 'No se ha compartido el token de cabecera.'})

		author_user_id = request.GET.get('author_user_id')
		if author_user_id is not None:
			# Debemos devolver la lista de paseos del usuario, cualquiera que sea su ubicación.
			# Se van a mostrar en la pantalla Mis Paseos
			try:
				usuario = Tuser.objects.get(id = author_user_id, active_session_token = token)
			except Tuser.DoesNotExist:
				return JsonResponse(status=403, data={'Error': 'El token de sesión es inválido.'})

			walks = Twalk.objects.filter(author_id = usuario.id).order_by('-datetime')
			lista_paseos = []
			for row in walks:
				data = {}
				data['id'] = row.id
				data['author_name'] = usuario.name
				data['datetime'] = row.datetime
				data['latitude'] = row.latitude
				data['longitude'] = row.longitude
				lista_paseos.append(data)
			return JsonResponse(lista_paseos, status=200, safe=False)

		else:
			# Debemos devolver la lista de paseos cercanos.
			# Se van a mostrar en la pantalla Paseos Cercanos
			try:
				Tuser.objects.get(active_session_token = token) # Sólo validamos el token
			except Tuser.DoesNotExist:
				return JsonResponse(status=403, data={'Error': 'El token de sesión es inválido.'})
			try:
				latitude = request.GET['latitude']
				longitude = request.GET['longitude']
				radius = request.GET['radius']
				not_started = request.GET['not_started']
			except (ValueError, MultiValueDictKeyError) as e:
				return JsonResponse(status=400, data={'Error': 'Falta algún campo o su contenido es inválido.'})
			lista_paseos = []
			if (not_started == 'true'):
				walks = Twalk.objects.filter(datetime__gte = datetime.now()).order_by('datetime')
				for row in walks:
					data = {}
					if (calcularDistancia(latitude, longitude, row.latitude, row.longitude)<=float(radius)):
						data['id'] = row.id
						data['author_name'] = row.author.name
						data['datetime'] = row.datetime
						data['latitude'] = row.latitude
						data['longitude'] = row.longitude
						lista_paseos.append(data)
				return JsonResponse(lista_paseos, status=200, safe=False)
			else:
				return JsonResponse(status=400, data={'Error': 'El parámetro not_started ha de ser siempre true.'})
	elif request.method == 'POST':
		try:
                        token = request.headers['token']
		except KeyError:
                        return JsonResponse(status=401, data={'Error': 'No se ha compartido el token de cabecera'})
		json_peticion = json.loads(request.body)
		try:
			date = json_peticion['datetime']
			lat = json_peticion['latitude']
			long = json_peticion['longitude']
		except (ValueError, KeyError) as e:
			return JsonResponse(status=400, data={'Error': 'Falta algún campo o su contenido es inválido.'})
		try:
			usuario = Tuser.objects.get(active_session_token = token)
		except Tuser.DoesNotExist:
			return JsonResponse(status=403, data={'Error': 'El token de sesión es inválido.'})
		paseo = Twalk(datetime=date, latitude=lat, longitude=long, author=usuario)
		paseo.save()
		return JsonResponse(status=201, data={'status': 'ok'})


