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
    ('/api/v0/votes/', 403),
    ('/fake-url', 404)
]


@pytest.mark.parametrize('url, status_code', server_rsp_params)
def test_server_responses(url, status_code):
    base_url = 'http://127.0.0.1:8000'
    rsp = requests.get(base_url + url)
    assert rsp.status_code == status_code


# #  Test Votes API
# def test_post_response_200():
#     # test
#     pass


endpoint = 'http://17.0.0.1:8000/api/v0/votes/'


vote_data = [
    (4, 66, 12),  # "12 poin is already given"
]


@pytest.mark.parametrize('from_voter, to_participant', 'point', vote_data)
#
@pytest.mark.smoketest
def test_vote_post_endpoint():
    """
    Verifies that the post vote endpoint is returning data with an expected
    """

    resp = requests.post(endpoint, {
        "from_voter": "4",
        "to_participant": "66",
        "point": "12"
    })

    assert resp.status_code == 200
    assert schema.is_valid(resp.json())
