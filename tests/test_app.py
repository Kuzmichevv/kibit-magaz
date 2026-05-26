import unittest

from app import app, get_valid_products


class ShopAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.secret_key = "test-secret-key"
        self.client = app.test_client()

    def test_index_page_opens(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"KIBIT Magaz", response.data)

    def test_index_can_filter_products_by_category(self):
        products = get_valid_products()
        selected_product = products[0]
        other_product = next(product for product in products if product["category"] != selected_product["category"])

        response = self.client.get("/", query_string={"category": selected_product["category"]})

        self.assertEqual(response.status_code, 200)
        self.assertIn(selected_product["name"].encode("utf-8"), response.data)
        self.assertNotIn(other_product["name"].encode("utf-8"), response.data)

    def test_categories_page_opens(self):
        response = self.client.get("/categories")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Каталог товарів".encode("utf-8"), response.data)

    def test_add_to_cart_creates_session_entry(self):
        response = self.client.post("/add/1", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as session_data:
            self.assertEqual(session_data["cart"]["1"], 1)

    def test_update_cart_changes_quantity(self):
        with self.client.session_transaction() as session_data:
            session_data["cart"] = {"1": 1}

        response = self.client.post("/update/1", data={"quantity": "3"}, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as session_data:
            self.assertEqual(session_data["cart"]["1"], 3)

    def test_checkout_requires_customer_data(self):
        with self.client.session_transaction() as session_data:
            session_data["cart"] = {"1": 1}

        response = self.client.post("/checkout", data={"name": "", "address": ""}, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Заповніть".encode("utf-8"), response.data)

    def test_checkout_clears_cart_after_success(self):
        with self.client.session_transaction() as session_data:
            session_data["cart"] = {"1": 2}

        response = self.client.post(
            "/checkout",
            data={"name": "Андрій", "address": "Київ, вул. Центральна, 1"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Замовлення оформлено".encode("utf-8"), response.data)
        with self.client.session_transaction() as session_data:
            self.assertEqual(session_data["cart"], {})


if __name__ == "__main__":
    unittest.main()
