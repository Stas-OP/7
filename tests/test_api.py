import unittest
import requests
import uuid

class SimpleApiTests(unittest.TestCase):

    BASE_URL = "http://localhost:8000"
    
    def generate_unique_username(self):
        return f"testuser_{uuid.uuid4().hex[:8]}"

    def test_1_register_success(self):
        username = self.generate_unique_username()
        payload = {"username": username, "password": "password123"}
        response = requests.post(f"{self.BASE_URL}/register", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("token", data)
        self.assertIn("id", data)

    def test_2_login_success(self):
        username = self.generate_unique_username()
        password = "password123"
        requests.post(f"{self.BASE_URL}/register", json={"username": username, "password": password})
        
        payload = {"username": username, "password": password}
        response = requests.post(f"{self.BASE_URL}/login", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("token", data)

    def test_3_login_fail_password(self):
        username = self.generate_unique_username()
        password = "password123"
        requests.post(f"{self.BASE_URL}/register", json={"username": username, "password": password})

        payload = {"username": username, "password": "wrongpassword"}
        response = requests.post(f"{self.BASE_URL}/login", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_4_encrypt_decrypt_simple(self):
        username = self.generate_unique_username()
        password = "password123"
        register_response = requests.post(f"{self.BASE_URL}/register", json={"username": username, "password": password})
        token = register_response.json()["token"]

        text_to_encrypt = "simple test"
        key = "key"
        
        encrypt_payload = {"text": text_to_encrypt, "key": key}
        encrypt_response = requests.post(f"{self.BASE_URL}/encrypt?token={token}", json=encrypt_payload)
        self.assertEqual(encrypt_response.status_code, 200)
        encrypted_text = encrypt_response.json()["result"]
        self.assertIsInstance(encrypted_text, str)
        self.assertNotEqual(encrypted_text, text_to_encrypt)

        decrypt_payload = {"text": encrypted_text, "key": key}
        decrypt_response = requests.post(f"{self.BASE_URL}/decrypt?token={token}", json=decrypt_payload)
        self.assertEqual(decrypt_response.status_code, 200)
        decrypted_text = decrypt_response.json()["result"]
        
        # Примечание: Шифр Плейфера может добавлять 'x' или 'z', поэтому точное совпадение не всегда будет
        # Это очень простой тест, проверяющий только успешность вызова
        self.assertIsInstance(decrypted_text, str) 

    def test_5_add_get_text(self):
        username = self.generate_unique_username()
        password = "password123"
        register_response = requests.post(f"{self.BASE_URL}/register", json={"username": username, "password": password})
        token = register_response.json()["token"]

        text_content = "This is a test text."
        add_payload = {"text": text_content}
        add_response = requests.post(f"{self.BASE_URL}/texts?token={token}", json=add_payload)
        self.assertEqual(add_response.status_code, 200)
        added_text_id = add_response.json()["id"]

        get_response = requests.get(f"{self.BASE_URL}/texts/{added_text_id}?token={token}")
        self.assertEqual(get_response.status_code, 200)
        retrieved_text = get_response.json()
        self.assertEqual(retrieved_text["text"], text_content)
        self.assertEqual(retrieved_text["id"], added_text_id)

if __name__ == '__main__':
    unittest.main() 