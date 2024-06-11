import unittest
import json
from app import create_app


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True

        # Initialize some sample data for testing
        self.sample_bloq = {"title": "Sample Bloq", "address": "123 Sample St"}
        self.sample_locker = {
            "bloq_id": "484e01be-1570-4ac1-a2a9-02aad3acc54e",
            "status": "OPEN",
            "is_occupied": False,
        }
        self.sample_rent = {"locker_id": "2191e1b5-99c7-45df-8302-998be394be48", "weight": 10.5, "size": "M",
                            "status": "CREATED"}

    def test_get_bloqs(self):
        response = self.client.get("/api/bloqs")
        self.assertEqual(response.status_code, 200)

    def test_create_bloq(self):
        response = self.client.post(
            "/api/bloqs",
            data=json.dumps(self.sample_bloq),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn("id", data)
        self.assertEqual(data["title"], self.sample_bloq["title"])
        self.assertEqual(data["address"], self.sample_bloq["address"])

    def test_get_bloq(self):
        # Create a bloq first
        response = self.client.post(
            "/api/bloqs",
            data=json.dumps(self.sample_bloq),
            content_type="application/json",
        )
        bloq_id = json.loads(response.data.decode())["id"]

        # Retrieve the created bloq
        response = self.client.get(f"/api/bloqs/{bloq_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["id"], bloq_id)

    def test_get_lockers(self):
        response = self.client.get("/api/lockers")
        self.assertEqual(response.status_code, 200)

    def test_create_locker(self):
        response = self.client.post(
            "/api/lockers",
            data=json.dumps(self.sample_locker),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn("id", data)
        self.assertEqual(data["status"], self.sample_locker["status"])
        self.assertEqual(data["is_occupied"], self.sample_locker["is_occupied"])

    def test_get_locker(self):
        # Create a locker first
        response = self.client.post(
            "/api/lockers",
            data=json.dumps(self.sample_locker),
            content_type="application/json",
        )
        locker_id = json.loads(response.data.decode())["id"]

        # Retrieve the created locker
        response = self.client.get(f"/api/lockers/{locker_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["id"], locker_id)

    def test_update_locker_status(self):
        # Create a locker first
        response = self.client.post(
            "/api/lockers",
            data=json.dumps(self.sample_locker),
            content_type="application/json",
        )
        locker_id = json.loads(response.data.decode())["id"]

        # Update the locker status
        updated_status = {"status": "CLOSED", "is_occupied": False}
        response = self.client.put(
            f"/api/lockers/{locker_id}/status",
            data=json.dumps(updated_status),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["status"], updated_status["status"])
        self.assertEqual(data["is_occupied"], updated_status["is_occupied"])

    def test_get_rents(self):
        response = self.client.get("/api/rents")
        self.assertEqual(response.status_code, 200)

    def test_create_rent(self):
        # Create a new locker
        response = self.client.post(
            "/api/lockers",
            data=json.dumps(self.sample_locker),
            content_type="application/json",
        )
        locker_id = json.loads(response.data.decode())["id"]
        self.sample_rent["locker_id"] = locker_id
        response = self.client.post(
            "/api/rents/rent",
            data=json.dumps(self.sample_rent),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn("id", data)
        self.assertEqual(data["status"], self.sample_rent["status"])
        self.assertEqual(data["size"], self.sample_rent["size"])

    def test_get_rent(self):
        # Create a new locker
        response = self.client.post(
            "/api/lockers",
            data=json.dumps(self.sample_locker),
            content_type="application/json",
        )
        locker_id = json.loads(response.data.decode())["id"]
        self.sample_rent["locker_id"] = locker_id
        # Create a rent first
        response = self.client.post(
            "/api/rents/rent",
            data=json.dumps(self.sample_rent),
            content_type="application/json",
        )
        rent_id = json.loads(response.data.decode())["id"]

        # Retrieve the created rent
        response = self.client.get(f"/api/rents/{rent_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["id"], rent_id)

    def test_update_rent_status(self):
        # Create a new locker
        response = self.client.post(
            "/api/lockers",
            data=json.dumps(self.sample_locker),
            content_type="application/json",
        )
        locker_id = json.loads(response.data.decode())["id"]
        self.sample_rent["locker_id"] = locker_id
        # Create a rent first
        response = self.client.post(
            "/api/rents/rent",
            data=json.dumps(self.sample_rent),
            content_type="application/json",
        )
        rent_id = json.loads(response.data.decode())["id"]

        # Update the rent status
        updated_status = {"status": "DELIVERED"}
        response = self.client.put(
            f"/api/rents/{rent_id}/status",
            data=json.dumps(updated_status),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["status"], updated_status["status"])


if __name__ == "__main__":
    unittest.main()
