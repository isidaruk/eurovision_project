import json
import pytest
import requests


# Fixes needed:
# - Create a temporary database.
# - Manage testing not on real database data.
# - No hardcoding.

# Skip it just for now:
TOKEN = "c8566b58-9d83-4086-9071-64c227e6e236"

test_data = [
    # 4 - Norway, 64 - Belgium
    (4, 64, 10, 403, "c8566b58-9d83-4086-9071-64c227e6e236XXX"),  # test invalid Token (permission errors) -- 403 Forbidden b'{"detail":"You do not have permission to perform this action."}'
    (4, 64, 10, 201, TOKEN),  # test success (successful casses)-- 201 Created b'{"id":102,"from_voter":4,"to_participant":64,"point":10}'


    # 4 - Norway, 66 - Slovenia
    (4, 66, 10, 400, TOKEN),  # test failed (validation errors)-- 400 Bad Request b'["10 point is already given."]'

    # 4 - Norway, 3 - Norway
    (4, 3, 8, 400, TOKEN),  # test failed (validation errors) -- 400 Bad Request b'["You are not allowed to vote for your own country."]'

    # 4 - Norway, 64 - Belgium
    (4, 64, 8, 400, TOKEN),  # test failed (validation errors) -- 400 Bad Request b'["You\'ve already given a point to these participant."]'

    # Successful
    # 4 - Norway, 66 - Slovenia
    (4, 66, 8, 201, TOKEN),  # test success (successful casses) -- 201 Created b'{"id":X,"from_voter":4,"to_participant":66,"point":8}'

    # 4 - Norway, 67 - Russia
    (4, 67, 12, 201, TOKEN),  # test success (successful casses) -- 201 Created b'{"id":X,"from_voter":4,"to_participant":67,"point":12}'


    # Votes exhusted.
    # 4 - Norway, 67 - Russia
    (4, 67, 12, 400, TOKEN),  # test failed (validation errors) -- 400 Bad Request b'["You've voted 10 times"]'

]


@pytest.mark.parametrize('from_voter, to_participant, point, status_code, token', test_data)
def test_vote_post_endpoint_data(from_voter, to_participant, point, status_code, token):
    endpoint = 'http://127.0.0.1:8000/api/v0/votes/'

    resp = requests.post(endpoint, data=json.dumps({
        "from_voter": from_voter,
        "to_participant": to_participant,
        "point": point
    }), headers={"Content-Type": "application/json", "Token": token})

    assert resp.status_code == status_code


def test_vote_get_endpoint_data():
    endpoint = 'http://127.0.0.1:8000/api/v0/votes/'

    rsp = requests.get(endpoint)
    assert rsp.status_code == 200
