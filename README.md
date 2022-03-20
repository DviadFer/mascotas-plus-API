# Mascotas Plus - API REST

## Dependencias para visualizar el proyecto de manera local.

- Instalar PHP y la librería para Apache2.
- Instalar mariadb y crear la bases de datos `mascotasplusdb` con usuario `dev` y contraseña `1234`.
- Sustituir 'raspi' por 'localhost' en el `db_connection.php` de los proyectos:

```php
  function get_db_connection_or_die() {
    //OLD: $mysqli = new mysqli('raspi', 'dev', '1234', 'mascotasplusdb');
    $mysqli = new mysqli('localhost', 'dev', '1234', 'mascotasplusdb');
    if ($mysqli->connect_error) {
		// Mensaje de error
    }
    return $mysqli;
  }
```

> :eyes: Los datos necesarios para crear la bd están en `create-tables-mascotaspluso.sql`

## Tareas realizadas en el proyecto.

Fui encargado de realizar el end-point `endpoints_walks.py` dentro del directorio `./django/mascotasplus/restapi`. Gracias a a la view `request_walk()`, el framework de Django controla el acceso de la base de datos según el método HTTP que reciba como petición el servidor.

>  :warning: Se emplean respuestas Json determinadas segun el error recogido en el try-except.

También se ha importado dentro del código del endpoint, el archivo `formula_haversine.py` donde se implementa la **fórmula matemática necesaria para calcular la distancia en km** que existe entre dos latitudes y longitudes. Esto servirá para calcular el radio de búsqueda deseado de los paseos publicados por los usuarios. 

**Fórmula de Haversine en Python**

```python
import math

def calcularDistancia(lt1, ln1, lt2, ln2):
    radio_terrestre = 6373.0

    lat1 = math.radians(float(lt1))
    lat2 = math.radians(float(lt2))
    lon1 = math.radians(float(ln1))
    lon2 = math.radians(float(ln2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return radio_terrestre*c #km
```

### Método GET:

```python
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
```

### Método POST:

````python
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

````
