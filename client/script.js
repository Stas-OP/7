const API_URL = 'http://localhost:8000';
let token = null;

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

document.getElementById('logout-btn').onclick = () => {
    token = null;
    document.getElementById('auth-forms').style.display = 'block';
    document.getElementById('main-content').style.display = 'none';
};

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

async function loadTexts() {
    try {
        const response = await fetch(`${API_URL}/texts?token=${token}`);
        if (!response.ok) {
            if (response.status === 401) {
                document.getElementById('logout-btn').click();
                alert('Сессия истекла. Пожалуйста, войдите снова.');
                return;
            }
            throw new Error('Не удалось загрузить тексты');
        }
        const texts = await response.json();
        const textsList = document.getElementById('texts-list');
        textsList.innerHTML = '';
        texts.forEach(text => {
            const div = document.createElement('div');
            div.className = 'text-item';
            const escapedText = text.text.replace(/'/g, "\\'").replace(/"/g, '&quot;'); 
            div.innerHTML = `
                <div class="text-preview">${text.text.substring(0, 100)}${text.text.length > 100 ? '...' : ''}</div>
                <div class="actions">
                    <button onclick="viewText(${text.id})">Просмотреть</button>
                    <button onclick="startEdit(${text.id}, '${escapedText}')">Редактировать</button> 
                    <button onclick="deleteText(${text.id})">Удалить</button>
                </div>
            `;
            textsList.appendChild(div);
        });
    } catch (error) {
        console.error('Ошибка при загрузке текстов:', error);
        alert('Ошибка при загрузке текстов');
    }
}

function showTextView(textId, textContent, timestamp, isEditing) {
    document.getElementById('main-content').style.display = 'none';
    document.getElementById('text-view').style.display = 'block';

    const title = document.getElementById('text-view-title');
    const textArea = document.getElementById('full-text-area');
    const dateDisplay = document.getElementById('text-date');
    const saveButton = document.getElementById('save-text-btn');

    title.textContent = isEditing ? 'Редактирование текста' : 'Просмотр текста';
    textArea.value = textContent;
    textArea.readOnly = !isEditing;
    dateDisplay.textContent = 
        `Последнее изменение: ${new Date(timestamp).toLocaleString()}`;

    if (isEditing) {
        saveButton.style.display = 'block';
        saveButton.replaceWith(saveButton.cloneNode(true)); 
        document.getElementById('save-text-btn').onclick = () => saveTextChanges(textId); 
    } else {
        saveButton.style.display = 'none';
        saveButton.onclick = null;
    }
}

async function viewText(id) {
    try {
        const response = await fetch(`${API_URL}/texts/${id}?token=${token}`);
        const text = await response.json();
        if (response.ok) {
            showTextView(id, text.text, text.timestamp, false);
        } else {
            alert(text.detail);
        }
    } catch (error) {
        alert('Ошибка при загрузке текста');
    }
}

function startEdit(id, currentText) {
    showTextView(id, currentText, new Date().toISOString(), true);
}

async function saveTextChanges(id) {
    const newText = document.getElementById('full-text-area').value;
    const data = { text: newText };

    try {
        const response = await fetch(`${API_URL}/texts/${id}?token=${token}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert('Текст успешно обновлен!');
            document.getElementById('back-btn').click();
            loadTexts();
        } else {
            const result = await response.json();
            alert(`Ошибка при сохранении: ${result.detail}`);
        }
    } catch (error) {
        console.error('Ошибка при сохранении текста:', error);
        alert('Ошибка при сохранении текста.');
    }
}

document.getElementById('back-btn').onclick = () => {
    document.getElementById('text-view').style.display = 'none';
    document.getElementById('main-content').style.display = 'block';
};

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