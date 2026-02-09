
import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8001"
TEST_USER = {
    "email": f"test_user_{int(time.time())}@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
}

def test_root():
    print("Testing Root Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}, Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return False

def test_auth():
    print("\nTesting Authentication...")
    # Signup
    print("1. Signup...")
    signup_resp = requests.post(f"{BASE_URL}/auth/signup", json=TEST_USER)
    print(f"Signup Status: {signup_resp.status_code}")
    if signup_resp.status_code != 200:
        print(f"Signup Failed: {signup_resp.text}")
        return None

    # Signin
    print("2. Signin...")
    signin_data = {
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    signin_resp = requests.post(f"{BASE_URL}/auth/signin", data=signin_data)
    print(f"Signin Status: {signin_resp.status_code}")
    if signin_resp.status_code != 200:
        print(f"Signin Failed: {signin_resp.text}")
        return None
    
    token = signin_resp.json().get("access_token")
    
    # /users/me
    print("3. /users/me...")
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = requests.get(f"{BASE_URL}/auth/users/me", headers=headers)
    print(f"Me Status: {me_resp.status_code}, Email: {me_resp.json().get('email')}")
    if me_resp.status_code != 200:
        return None

    return token

def test_todos(token):
    print("\nTesting Todo CRUD APIs...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create
    print("1. Create Todo...")
    todo_data = {"title": "Verify Phase II", "description": "Ensure everything works", "completed": False}
    create_resp = requests.post(f"{BASE_URL}/todos/", json=todo_data, headers=headers)
    print(f"Create Status: {create_resp.status_code}")
    if create_resp.status_code != 200:
        return False
    
    todo_id = create_resp.json().get("id")
    
    # Read
    print("2. Read Todos...")
    read_resp = requests.get(f"{BASE_URL}/todos/", headers=headers)
    print(f"Read Status: {read_resp.status_code}, Count: {len(read_resp.json())}")
    
    # Update
    print("3. Update Todo...")
    update_data = {"description": "Updated Description"}
    update_resp = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data, headers=headers)
    print(f"Update Status: {update_resp.status_code}")
    
    # Toggle
    print("4. Toggle Todo...")
    toggle_resp = requests.patch(f"{BASE_URL}/todos/{todo_id}/complete", headers=headers)
    print(f"Toggle Status: {toggle_resp.status_code}, Completed: {toggle_resp.json().get('completed')}")
    
    # Delete
    print("5. Delete Todo...")
    delete_resp = requests.delete(f"{BASE_URL}/todos/{todo_id}", headers=headers)
    print(f"Delete Status: {delete_resp.status_code}")
    
    return True

if __name__ == "__main__":
    if not test_root():
        print("Server not reachable. Exiting.")
        sys.exit(1)
    
    token = test_auth()
    if token:
        if test_todos(token):
            print("\nVerification Successful!")
        else:
            print("\nTodo CRUD Verification Failed.")
    else:
        print("\nAuthentication Verification Failed.")
