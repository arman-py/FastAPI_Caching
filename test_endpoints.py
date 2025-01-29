from sqlmodel import select
from models import Payload


def test_create_payload(client, session):
    data = {"list_1": ["text1", "text2"], "list_2": ["text3", "text4"]}

    response = client.post("/payload", json=data)
    assert response.status_code == 200
    assert "payload_id" in response.json()
    payload_id = response.json()["payload_id"]
    stored_payload = session.exec(
        select(Payload).where(Payload.payload_id == payload_id)
    ).first()
    assert stored_payload is not None
    assert stored_payload.payload_id == payload_id


def test_get_payload(client, session):
    data = {"list_1": ["sample1", "sample2"], "list_2": ["sample3", "sample4"]}
    response = client.post("/payload", json=data)
    payload_id = response.json()["payload_id"]

    response = client.get(f"/payload/{payload_id}")

    assert response.status_code == 200
    response_json = response.json()
    assert "output" in response_json
    assert isinstance(response_json["output"], str)


def test_create_payload_duplicate(client, session):
    data = {"list_1": ["text1", "text2"], "list_2": ["text3", "text4"]}
    response = client.post("/payload", json=data)
    payload_id = response.json()["payload_id"]

    response = client.post("/payload", json=data)
    assert response.status_code == 200
    assert response.json()["payload_id"] == payload_id


def test_payload_not_found(client):
    response = client.get("/payload/nonexistent_payload_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Payload not found"}
