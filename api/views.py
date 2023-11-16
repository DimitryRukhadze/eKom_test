from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from environs import Env
from tinydb import TinyDB, Query


env = Env()
env.read_env()
DB = TinyDB(env('TINYDB_FILE'))


# class MySerializer(serializers.Serializer):

@csrf_exempt
@api_view(['POST'])
def get_form(request):
    request_body_data = request.data
    data = DB.search(Query().fragment(request_body_data))
    return JsonResponse(data, safe=False)
