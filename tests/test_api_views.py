import pytest
import json

from django.http import JsonResponse
from rest_framework.test import APIRequestFactory
from api.views import get_form


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.mark.django_db
def test_get_form(request_factory):
    data = {
        'message': 'blahblah',
        'post_date': '2008-02-12',
        'user_author': 'mememe',
        'author_email': 'author_email'
    }

    request = request_factory.post('/get-form', data)
    response = get_form(request)
    assert response.status_code == 200
    assert isinstance(response, JsonResponse)
    assert json.loads(response.content) == [
        {
        "template_name": "new_message",
        "user_author": "text",
        "author_email": "email",
        "message": "text",
        "post_date": "date"
        }
    ]
