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
    (4, 64, 10, 403, "c8566b58-9d83-4086-9071-64c227e6e236XXX"),  # test invalid Token -- 403 Forbidden b'{"detail":"You do not have permission to perform this action."}'
    (4, 64, 10, 201, TOKEN),  # test success -- 201 Created b'{"id":102,"from_voter":4,"to_participant":64,"point":10}'

    # 4 - Norway, 66 - Slovenia
    (4, 66, 10, 400, TOKEN),  # test failed -- 400 Bad Request b'["10 point is already given."]'

    # 4 - Norway, 3 - Norway
    (4, 3, 8, 400, TOKEN),  # test failed -- 400 Bad Request b'["You are not allowed to vote for your own country."]'

    # 4 - Norway, 64 - Belgium
    (4, 64, 8, 400, TOKEN),  # test failed -- 400 Bad Request b'["You\'ve already given a point to these participant."]'

    # 4 - Norway, 66 - Slovenia
    (4, 66, 8, 201, TOKEN),  # test success -- 201 Created b'{"id":102,"from_voter":4,"to_participant":66,"point":8}'

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
