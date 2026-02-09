
import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"
TEST_USER = {
    "email": "verify_user@example.com",
    "password": "password123",
    "full_name": "Verify User"
}

def log_test(name, status, result=None):
    print(f"[{'PASS' if status else 'FAIL'}] {name}")
    if result:
        print(f"    Result: {result}")

def test_system():
    print("--- Phase III Full Verification ---")
    
    # 1. DB Health
    try:
        resp = requests.get(f"{BASE_URL}/db-health")
        log_test("DB Health Check", resp.status_code == 200, resp.json())
    except Exception as e:
        log_test("DB Health Check", False, str(e))
        return

    # 2. Auth: Signup
    try:
        resp = requests.post(f"{BASE_URL}/auth/signup", json=TEST_USER)
        # 400 if already exists is also fine for re-run, but 200 is pass for fresh run
        log_test("Signup", resp.status_code in [200, 400], resp.text)
    except Exception as e:
        log_test("Signup", False, str(e))

    # 3. Auth: Signin
    token = None
    try:
        signin_data = {"username": TEST_USER["email"], "password": TEST_USER["password"]}
        resp = requests.post(f"{BASE_URL}/auth/signin", data=signin_data)
        log_test("Signin", resp.status_code == 200)
        if resp.status_code == 200:
            token = resp.json().get("access_token")
    except Exception as e:
        log_test("Signin", False, str(e))
    
    if not token:
        print("Aborting remaining tests: No Auth Token.")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 4. Auth: /users/me
    try:
        resp = requests.get(f"{BASE_URL}/auth/users/me", headers=headers)
        log_test("Users/Me", resp.status_code == 200, resp.json().get("email"))
        user_id = resp.json().get("id")
    except Exception as e:
        log_test("Users/Me", False, str(e))

    # 5. Todo CRUD
    task_id = None
    try:
        # Create
        resp = requests.post(f"{BASE_URL}/todos/", json={"title": "Test Phase III Task", "description": "Verification"}, headers=headers)
        log_test("Create Todo", resp.status_code == 200, resp.json().get("title"))
        task_id = resp.json().get("id")
        
        # List
        resp = requests.get(f"{BASE_URL}/todos/", headers=headers)
        log_test("List Todos", resp.status_code == 200, f"Found {len(resp.json())} tasks")
        
        # Complete
        resp = requests.patch(f"{BASE_URL}/todos/{task_id}/complete", headers=headers)
        log_test("Complete Todo", resp.status_code == 200, f"Completed: {resp.json().get('completed')}")
        
        # Update
        resp = requests.put(f"{BASE_URL}/todos/{task_id}", json={"title": "Updated Task Title"}, headers=headers)
        log_test("Update Todo", resp.status_code == 200, resp.json().get("title"))
        
        # Delete
        resp = requests.delete(f"{BASE_URL}/todos/{task_id}", headers=headers)
        log_test("Delete Todo", resp.status_code == 200)
    except Exception as e:
        log_test("Todo CRUD", False, str(e))

    # 6. AI Chatbot (Internal MCP tools mapping via /mcp/chat)
    chat_tests = [
        "Add a task buy milk",
        "Show my todos",
        "Mark task 1 complete",
        "Delete test task",
        "Who am I logged in as?"
    ]
    
    print("\n--- Testing AI Agent (Chat) ---")
    for msg in chat_tests:
        try:
            resp = requests.post(f"{BASE_URL}/mcp/chat", json={"message": msg}, params={"user_id": user_id})
            log_test(f"Chat: '{msg}'", resp.status_code == 200, resp.json().get("reply"))
        except Exception as e:
            log_test(f"Chat: '{msg}'", False, str(e))

if __name__ == "__main__":
    time.sleep(2) # Wait for server
    test_system()
