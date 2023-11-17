from rest_framework import serializers
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from environs import Env
from tinydb import TinyDB, Query
from phonenumbers import parse, is_valid_number
from phonenumbers.phonenumberutil import NumberParseException


env = Env()
env.read_env()
DB = TinyDB(env('TINYDB_FILE'))


class DataSerializer(serializers.Serializer):
    data = serializers.CharField()

    def validate_data(self, value):
        if self.is_valid_date(value):
            return "date"
        elif self.is_valid_phone_number(value):
            return "phone"
        elif self.is_valid_email(value):
            return "email"
        else:
            return "text"

    def is_valid_date(self, value):
        try:
            serializers.DateField().to_internal_value(value)
            return True
        except serializers.ValidationError:
            return False

    def is_valid_phone_number(self, value):
        try:
            parsed_number = parse(value)
            return is_valid_number(parsed_number)
        except NumberParseException:
            return False

    def is_valid_email(self, value):
        try:
            validate_email(value)
            return True
        except ValidationError:
            return False


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
