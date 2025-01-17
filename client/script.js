const API_URL = 'http://localhost:8000';
let token = null;

// Регистрация
document.getElementById('register-form').onsubmit = async (e) => {
    e.preventDefault();
    const data = {
        username: e.target.username.value,
        password: e.target.password.value
    };

    try {
        const response = await fetch(API_URL + '/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (response.ok) {
            token = result.token;
            document.getElementById('auth-forms').style.display = 'none';
            document.getElementById('main-content').style.display = 'block';
            document.getElementById('username-display').textContent = data.username;
            loadTexts();
        } else {
            alert(result.detail);
        }
    } catch (error) {
        alert('Ошибка при регистрации');
    }
};

// Вход
document.getElementById('login-form').onsubmit = async (e) => {
    e.preventDefault();
    const data = {
        username: e.target.username.value,
        password: e.target.password.value
    };

    try {
        const response = await fetch(API_URL + '/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (response.ok) {
            token = result.token;
            document.getElementById('auth-forms').style.display = 'none';
            document.getElementById('main-content').style.display = 'block';
            document.getElementById('username-display').textContent = data.username;
            loadTexts();
        } else {
            alert(result.detail);
        }
    } catch (error) {
        alert('Ошибка при входе');
    }
};

// Выход
document.getElementById('logout-btn').onclick = () => {
    token = null;
    document.getElementById('auth-forms').style.display = 'block';
    document.getElementById('main-content').style.display = 'none';
};

// Добавление текста
document.getElementById('add-text-form').onsubmit = async (e) => {
    e.preventDefault();
    const data = {
        text: e.target.text.value
    };

    try {
        const response = await fetch(`${API_URL}/texts?token=${token}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            e.target.reset();
            loadTexts();
        } else {
            const result = await response.json();
            alert(result.detail);
        }
    } catch (error) {
        alert('Ошибка при сохранении текста');
    }
};

// Загрузка текстов
async function loadTexts() {
    try {
        const response = await fetch(`${API_URL}/texts?token=${token}`);
        const texts = await response.json();
        const textsList = document.getElementById('texts-list');
        textsList.innerHTML = '';
        texts.forEach(text => {
            const div = document.createElement('div');
            div.className = 'text-item';
            div.innerHTML = `
                <div class="text-preview">${text.text.substring(0, 100)}${text.text.length > 100 ? '...' : ''}</div>
                <div class="actions">
                    <button onclick="viewText(${text.id})">Просмотреть</button>
                    <button onclick="deleteText(${text.id})">Удалить</button>
                </div>
            `;
            textsList.appendChild(div);
        });
    } catch (error) {
        alert('Ошибка при загрузке текстов');
    }
}

// Просмотр одного текста
async function viewText(id) {
    try {
        const response = await fetch(`${API_URL}/texts/${id}?token=${token}`);
        const text = await response.json();
        if (response.ok) {
            document.getElementById('main-content').style.display = 'none';
            document.getElementById('text-view').style.display = 'block';
            document.getElementById('full-text').textContent = text.text;
            document.getElementById('text-date').textContent = 
                'Создан: ' + new Date(text.timestamp).toLocaleString();
        } else {
            alert(text.detail);
        }
    } catch (error) {
        alert('Ошибка при загрузке текста');
    }
}

// Возврат к списку текстов
document.getElementById('back-btn').onclick = () => {
    document.getElementById('text-view').style.display = 'none';
    document.getElementById('main-content').style.display = 'block';
};

// Удаление текста
async function deleteText(id) {
    try {
        const response = await fetch(`${API_URL}/texts/${id}?token=${token}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            loadTexts();
        } else {
            const result = await response.json();
            alert(result.detail);
        }
    } catch (error) {
        alert('Ошибка при удалении текста');
    }
}

// Шифрование
document.getElementById('encrypt-btn').onclick = async () => {
    const form = document.getElementById('cipher-form');
    const data = {
        text: form.text.value,
        key: form.key.value
    };

    try {
        const response = await fetch(`${API_URL}/encrypt?token=${token}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (response.ok) {
            document.getElementById('cipher-result').value = result.result;
        } else {
            alert(result.detail);
        }
    } catch (error) {
        alert('Ошибка при шифровании');
    }
};

// Дешифрование
document.getElementById('decrypt-btn').onclick = async () => {
    const form = document.getElementById('cipher-form');
    const data = {
        text: form.text.value,
        key: form.key.value
    };

    try {
        const response = await fetch(`${API_URL}/decrypt?token=${token}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (response.ok) {
            document.getElementById('cipher-result').value = result.result;
        } else {
            alert(result.detail);
        }
    } catch (error) {
        alert('Ошибка при дешифровании');
    }
}; 