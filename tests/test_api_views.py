import pytest
import json

from django.http import JsonResponse
from rest_framework.test import APIRequestFactory
from api.views import get_form
from api.serializers import DataSerializer


@pytest.fixture
def request_factory():
    return APIRequestFactory()

@pytest.mark.parametrize('request_body,expected_response', [
    (
            {
                'message': 'blahblah',
                'post_date': '2008-02-12',
                'user_author': 'mememe',
                'author_email': 'author_email'
            },
            'new_message'
    ),
    (
            {
                'message': 'blahblah',
                'post_date': '2008-02-12',
                'user_author': 'mememe',
                'author_email': 'author_email',
                'topic': 'topic of message',
                'author_phone': '+7 926 102 94 63'
            },
            'new_message'
    ),
    (
            {
                'message': 'blahblah',
                'post_date': '2008-02-12'
            },
            'new_message'
    ),
    (
            {
                'surname': 'jezebel',
                'role': 'worker',
                'home_phone': '+7 926 102 94 63'
            },
            {
                'surname': 'text',
                'role': 'text',
                'home_phone': 'phone'
            }
    )

])
@pytest.mark.django_db
def test_get_form(request_factory, request_body, expected_response):

    request = request_factory.post('/get-form', request_body)
    response = get_form(request)
    assert response.status_code == 200
    assert isinstance(response, JsonResponse)
    assert json.loads(response.content) == expected_response
