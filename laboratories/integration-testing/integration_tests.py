import pytest
import requests
import uuid

BASE_URL = "https://todo.pixegami.io"

@pytest.fixture
def user_id():
    """
    Fixture care generează un user_id unic pentru fiecare test.
    """
    return str(uuid.uuid4())


@pytest.fixture
def sample_task(user_id):
    """
    Creează un task de testare și îl returnează.
    """
    task_data = {
        "user_id": user_id,
        "content": "Sample task content",
        "is_done": False
    }
    response = requests.put(f"{BASE_URL}/create-task", json=task_data)
    assert response.status_code == 200
    return response.json()["task"]


# ======================
# EXERCIȚII
# ======================

def test_create_task(user_id):
    """
    Testează crearea unui task nou.

    Pași:
    1. Trimite un request PUT către /create-task cu date valide.
    2. Verifică răspunsul (status 200).
    3. Extrage task_id și folosește-l pentru a face un GET.
    4. Verifică dacă datele returnate corespund celor introduse.

    Hint: În răspunsul de la /get-task nu vei mai avea `user_id`, deci verifică doar ce este disponibil.
    """

    task_data = {
        "user_id": user_id,
        "content": "Test task content",
        "is_done": False
    }
    create_response = requests.put(f"{BASE_URL}/create-task", json=task_data)
    assert create_response.status_code == 200

    task_id = create_response.json()["task"]["task_id"]

    get_response = requests.get(f"{BASE_URL}/get-task/{task_id}")
    assert get_response.status_code == 200

    retrieved_task = get_response.json()
    assert retrieved_task["content"] == task_data["content"]
    assert retrieved_task["is_done"] == task_data["is_done"]


def test_update_task(sample_task):
    """
    Testează actualizarea unui task existent.

    Pași:
    1. Creează un task.
    2. Trimite un PUT către /update-task cu modificări.
    3. Verifică status code-ul (200).
    4. Fă un GET pentru acel task și asigură-te că modificările sunt prezente.

    Hint: În răspunsul de la /update-task primești doar `updated_task_id`.
    """
    updated_task_data = {
        "task_id": sample_task["task_id"],
        "content": "Updated task content",
        "is_done": True
    }
    update_response = requests.put(f"{BASE_URL}/update-task", json=updated_task_data)
    assert update_response.status_code == 200

    updated_task_id = update_response.json()["updated_task_id"]
    assert updated_task_id == sample_task["task_id"]

    get_response = requests.get(f"{BASE_URL}/get-task/{updated_task_id}")
    assert get_response.status_code == 200

    retrieved_task = get_response.json()
    assert retrieved_task["content"] == updated_task_data["content"]
    assert retrieved_task["is_done"] == updated_task_data["is_done"]


def test_list_multiple_tasks(user_id):
    """
    Testează listarea task-urilor pentru un user.

    Pași:
    1. Creează 3 task-uri pentru același user_id.
    2. Trimite un GET către /list-tasks/{user_id}.
    3. Verifică dacă sunt exact 3 task-uri returnate.

    Hint: Folosește un user_id unic pentru a evita datele altor colegi.
    """
    user_id = user_id + "5"
    tasks = []
    for i in range(3):
        task_data = {
            "user_id": user_id,
            "content": f"Task {i + 1}",
            "is_done": False
        }
        response = requests.put(f"{BASE_URL}/create-task", json=task_data)
        assert response.status_code == 200
        tasks.append(response.json()["task"])

    list_response = requests.get(f"{BASE_URL}/list-tasks/{user_id}")
    assert list_response.status_code == 200

    retrieved_tasks = list_response.json()["tasks"]
    assert len(retrieved_tasks) == 3

    retrieved_task_ids = {task["task_id"] for task in retrieved_tasks}
    created_task_ids = {task["task_id"] for task in tasks}
    assert retrieved_task_ids == created_task_ids


def test_delete_task(sample_task):
    """
    Testează ștergerea unui task.

    Pași:
    1. Creează un task.
    2. Trimite un DELETE către /delete-task/{task_id}.
    3. Verifică status-ul (200).
    4. Încearcă să faci GET pe acel task și verifică că primești 404.
    """
    delete_response = requests.delete(f"{BASE_URL}/delete-task/{sample_task['task_id']}")
    assert delete_response.status_code == 200

    get_response = requests.get(f"{BASE_URL}/get-task/{sample_task['task_id']}")
    assert get_response.status_code == 404


def test_get_nonexistent_task():
    """
    Testează obținerea unui task inexistent.

    Pași:
    1. Generează un UUID aleator ca task_id.
    2. Trimite GET pe acel id.
    3. Verifică dacă primești status 404.

    Hint: Nu este nevoie să creezi nimic, doar folosește un id invalid (unic).
    """
    random_task_id = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/get-task/{random_task_id}")
    assert response.status_code == 404


def test_update_nonexistent_task(user_id):
    """
    Testează actualizarea unui task care nu există.

    Pași:
    1. Generează un UUID aleator ca task_id.
    2. Trimite PUT pe /update-task cu acel id.
    3. Verifică dacă primești eroare sau operația se execută cu succes.

    Hint: Dacă operația se execută cu succes, puteți face verificarea folosind GET.
    """
    random_task_id = str(uuid.uuid4())
    updated_task_data = {
        "task_id": random_task_id,
        "content": "Nonexistent task content",
        "is_done": True
    }
    update_response = requests.put(f"{BASE_URL}/update-task", json=updated_task_data)
    assert update_response.status_code == 200

    get_response = requests.get(f"{BASE_URL}/get-task/{random_task_id}")
    assert get_response.status_code == 200


def test_delete_nonexistent_task():
    """
    Testează ștergerea unui task inexistent.

    Pași:
    1. Generează un UUID aleator ca task_id.
    2. Trimite DELETE pe acel id.
    3. Verifică statusul.

    Hint: Validează că operația e "safe", adică nu aruncă excepție.
    """
    random_task_id = str(uuid.uuid4())
    response = requests.delete(f"{BASE_URL}/delete-task/{random_task_id}")
    assert response.status_code == 200

def test_create_task_invalid_data():
    """
    Testează crearea unui task cu date invalide.

    Pași:
    1. Trimite un request cu date invalide (ex: is_done="some_string").
    2. Verifică statusul și mesajul de eroare.
    """
    invalid_task_data = {
        "user_id": "id",
        "content": "Content", 
        "is_done": "some_string" 
    }
    response = requests.put(f"{BASE_URL}/create-task", json=invalid_task_data)
    assert response.status_code == 422
    error_message = response.json()["detail"][0]["msg"]
    assert "value could not be parsed to a boolean" in error_message


