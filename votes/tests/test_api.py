import pytest
import requests

# @pytest.mark.api
# def test_api_get_remote():
#     # test
#     pass


# @pytest.mark.api
# @pytest.mark.post
# def test_api_post_remote():
#     # test
#     pass


server_rsp_params = [
    ('/api/v0/', 200),
    ('/api/v0/votes/r', 403),
    ('/fake-url', 404)
]


@pytest.mark.parametrize('url, status_code', server_rsp_params)
def test_server_responses(url, status_code):
    base_url = 'http://127.0.0.1:8000'
    rsp = requests.get(base_url + url)
    assert rsp.status_code == status_code
