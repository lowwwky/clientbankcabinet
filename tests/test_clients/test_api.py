from uuid import uuid4


async def test_get_client_ok(client, test_client_obj):
    r = await client.get(f"/test_clients/{test_client_obj.client_id}/me/info/")
    assert r.status_code == 200
    assert r.json()["first_name"] == "Иван"


async def test_get_client_not_found(client):
    r = await client.get(f"/test_clients/{uuid4()}/me/info/")
    assert r.status_code == 404


async def test_get_client_bad_uuid(client):
    r = await client.get("/test_clients/не-uuid/me/info/")
    assert r.status_code == 422


async def test_update_contacts_empty_body(client, test_client_obj):
    url = f"/test_clients/{test_client_obj.client_id}/me/update/"
    r = await client.patch(url, json={})
    assert r.status_code == 200
    assert r.json()["phone"] == "+79990000000"


async def test_update_phone_boundary(client, test_client_obj):
    url = f"/test_clients/{test_client_obj.client_id}/me/update/"
    r = await client.patch(url, json={"phone": "1" * 10})
    assert r.status_code == 200

    r = await client.patch(url, json={"phone": "1" * 9})
    assert r.status_code == 422


async def test_documents_empty_list(client, test_client_obj):
    r = await client.get(f"/test_clients/{test_client_obj.client_id}/documents/all/")
    assert r.status_code == 200
    assert r.json() == []


async def test_relation_with_self(client, test_client_obj):
    cid = str(test_client_obj.client_id)
    r = await client.post(
        f"/test_clients/{cid}/relations/add/",
        json={"related_client_id": cid, "relation_type": "Родитель"},
    )
    assert r.status_code == 400


async def test_relation_duplicate(client, test_client_obj, second_client_obj):
    cid = test_client_obj.client_id
    body = {"related_client_id": str(second_client_obj.client_id), "relation_type": "Родитель"}
    assert (await client.post(f"/test_clients/{cid}/relations/add/", json=body)).status_code == 201
    assert (await client.post(f"/test_clients/{cid}/relations/add/", json=body)).status_code == 400


async def test_relation_unknown_related_client(client, test_client_obj):
    r = await client.post(
        f"/test_clients/{test_client_obj.client_id}/relations/add/",
        json={"related_client_id": str(uuid4()), "relation_type": "Родитель"},
    )
    assert r.status_code == 404


async def test_relation_invalid_type(client, test_client_obj, second_client_obj):
    r = await client.post(
        f"/test_clients/{test_client_obj.client_id}/relations/add/",
        json={"related_client_id": str(second_client_obj.client_id), "relation_type": "Друг"},
    )
    assert r.status_code == 422


async def test_delete_missing_relation(client, test_client_obj, second_client_obj):
    r = await client.request(
        "DELETE",
        f"/test_clients/{test_client_obj.client_id}/relations/delete/",
        json={
            "related_client_id": str(second_client_obj.client_id),
            "relation_type": "Родитель",
        },
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Связи не существует."