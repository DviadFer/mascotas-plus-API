
from django.http import JsonResponse
from .models import Tuser,Tcompanion,Twalk

def get(request,ida):
 
 try:
  mi_token = request.headers["token"]
 except KeyError:
  return JsonResponse(status=401, data={})

 try:
  mi_usuario = Tuser.objects.get(active_session_token = mi_token)
 except Tuser.DoesNotExist:
  return JsonResponse(status=403, data={})
 try:
  peticion = Twalk.objects.get(id = ida)
 except Twalk.DoesNotExist:
  return JsonResponse(status=404, data={})
 diccionario={}
 diccionario["author_name"]= peticion.author.name
 diccionario["datetime"] = peticion.datetime
 diccionario["latitude"] = peticion.latitude
 diccionario["longitude"] = peticion.longitude
 diccionario["companion_requests"] = []
 mi_paseo = peticion.tcompanion_set.all()
 for fila in mi_paseo: 
  otro_diccionario = {}
  otro_diccionario["request_id"] = fila.id
  otro_diccionario["user_name"] = fila.requester.name
  otro_diccionario["message"] = fila.message
  otro_diccionario["is_accepted"] = fila.is_accepted == 1
  diccionario["companion_requests"].append(otro_diccionario)
 return JsonResponse(status=201, data = diccionario)

