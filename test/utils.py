from httpx import Response


def validate_response(response: Response):
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['code'] is not None
    assert response_json['item'] is not None
    assert response_json['code'] == 0

    return response_json['item']