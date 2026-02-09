import pytest
import httpx
import asyncio

# Base URL for local testing
BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_full_flow():
    async with httpx.AsyncClient(base_url=BASE_URL) as ac:
        # Unique user for each run to avoid conflicts
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        email = f"user_{unique_id}@example.com"
        password = "password123"

        print(f"Testing with user: {email}")

        # 1. Signup
        user_data = {"email": email, "password": password}
        response = await ac.post("/auth/signup", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == email

        # 2. Login (OAuth2PasswordRequestForm uses 'username' field but we send email)
        login_data = {"username": email, "password": password}
        response = await ac.post("/auth/signin", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Create Todo
        todo_data = {"title": "Test Todo", "description": "This is a test todo"}
        response = await ac.post("/todos", json=todo_data, headers=headers)
        assert response.status_code == 200
        todo_item = response.json()
        assert todo_item["title"] == "Test Todo"
        todo_id = todo_item["id"]

        # 4. Get Todos
        response = await ac.get("/todos", headers=headers)
        assert response.status_code == 200
        todos = response.json()
        assert any(t["id"] == todo_id for t in todos)

        # 5. Update Todo (Complete)
        response = await ac.patch(f"/todos/{todo_id}/complete", headers=headers)
        assert response.status_code == 200
        updated_todo = response.json()
        assert updated_todo["completed"] is True

        # 6. Delete Todo
        response = await ac.delete(f"/todos/{todo_id}", headers=headers)
        assert response.status_code == 200
        
        # Verify deletion
        response = await ac.get("/todos", headers=headers)
        todos = response.json()
        assert not any(t["id"] == todo_id for t in todos)
