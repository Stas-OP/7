import requests
import os

class Client:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.token = None
        self.is_auth = False

    def register(self, username: str, password: str) -> bool:
        try:
            r = requests.post(f"{self.base_url}/register", 
                            json={"username": username, "password": password})
            if r.status_code == 200:
                data = r.json()
                self.token = data["token"]
                self.is_auth = True
                print(f"Регистрация успешна!\nID: {data['id']}\nТокен: {self.token}")
                return True
            print(f"Ошибка: {r.json()['detail']}")
            return False
        except Exception as e:
            print(f"Ошибка: {e}")
            return False

    def login(self, username: str, password: str) -> bool:
        try:
            r = requests.post(f"{self.base_url}/login", 
                            json={"username": username, "password": password})
            if r.status_code == 200:
                data = r.json()
                self.token = data["token"]
                self.is_auth = True
                print(f"Вход выполнен!\nID: {data['id']}\nТокен: {self.token}")
                return True
            print(f"Ошибка: {r.json()['detail']}")
            return False
        except Exception as e:
            print(f"Ошибка: {e}")
            return False

    def change_password(self, old_password: str, new_password: str) -> bool:
        if not self.token:
            print("Требуется авторизация")
            return False
        try:
            r = requests.patch(f"{self.base_url}/change-password", 
                             params={"old_password": old_password, 
                                    "new_password": new_password, 
                                    "token": self.token})
            if r.status_code == 200:
                self.token = r.json()["token"]
                print("Пароль изменен")
                return True
            print(f"Ошибка: {r.json()['detail']}")
            return False
        except Exception as e:
            print(f"Ошибка: {e}")
            return False

    def logout(self):
        self.token = None
        self.is_auth = False
        print("Выход выполнен")

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def main():
    client = Client()
    while True:
        clear()
        if not client.is_auth:
            print("\n1. Регистрация\n2. Вход\n3. Выход")
            choice = input("\nВыбор: ")
            if choice == "1":
                clear()
                username = input("Логин: ")
                password = input("Пароль: ")
                client.register(username, password)
            elif choice == "2":
                clear()
                username = input("Логин: ")
                password = input("Пароль: ")
                client.login(username, password)
            elif choice == "3":
                break
        else:
            print("\n1. Сменить пароль\n2. Выйти из аккаунта\n3. Выход")
            choice = input("\nВыбор: ")
            if choice == "1":
                clear()
                old_pass = input("Старый пароль: ")
                new_pass = input("Новый пароль: ")
                client.change_password(old_pass, new_pass)
            elif choice == "2":
                client.logout()
            elif choice == "3":
                break
        input("\nНажмите Enter...")

if __name__ == "__main__":
    main() 