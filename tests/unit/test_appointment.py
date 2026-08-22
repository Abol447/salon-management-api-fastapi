from tests.conftest import client


def test_filter_appointment(client):
    res = client.get(
        "/appointments/search",
        params={
            "customer_id": 1,
            "page": 1,
            "page_size": 10,
        },
    )
    assert res.status_code == 200
