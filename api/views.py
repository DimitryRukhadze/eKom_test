from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from environs import Env
from tinydb import TinyDB, Query

from .serializers import DataSerializer


env = Env()
env.read_env()
DB = TinyDB(env('TINYDB_FILE'))


@csrf_exempt
@api_view(['POST'])
def get_form(request):
    request_body_data = request.data
    request_form = {}
    serializer = DataSerializer()

    for field in request_body_data:
        request_form[field] = serializer.validate_data(request_body_data[field])

    search_fragment = {
        key: value
        for key, value in request_form.items()
        if DB.search((Query()[key].exists()) & (Query()[key] == value))
    }

    if not search_fragment:
        return JsonResponse(request_form, safe=False)

    data = DB.search(Query().fragment(search_fragment))

    return JsonResponse(data, safe=False)
