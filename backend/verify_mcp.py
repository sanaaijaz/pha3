
import requests
import sys

BASE_URL = "http://127.0.0.1:8002/mcp"
USER_ID = 1  # Using the user ID created during Phase II verification

def test_mcp_tools():
    print("Testing MCP Tools...")
    
    # 1. Add Task
    print("\n1. Add Task...")
    resp = requests.post(f"{BASE_URL}/add_task", params={"user_id": USER_ID, "title": "MCP Test Task", "description": "Testing Phase III"})
    print(f"Status: {resp.status_code}, Response: {resp.json()}")
    if resp.status_code != 200: return False
    task_id = resp.json().get("task_id")
    
    # 2. List Tasks
    print("\n2. List Tasks...")
    resp = requests.get(f"{BASE_URL}/list_tasks", params={"user_id": USER_ID})
    print(f"Status: {resp.status_code}, Count: {len(resp.json())}")
    if resp.status_code != 200: return False
    
    # 3. Update Task
    print("\n3. Update Task...")
    resp = requests.post(f"{BASE_URL}/update_task", params={"user_id": USER_ID, "task_id": task_id, "description": "Updated via MCP"})
    print(f"Status: {resp.status_code}, Response: {resp.json()}")
    if resp.status_code != 200: return False
    
    # 4. Complete Task
    print("\n4. Complete Task...")
    resp = requests.post(f"{BASE_URL}/complete_task", params={"user_id": USER_ID, "task_id": task_id})
    print(f"Status: {resp.status_code}, Response: {resp.json()}")
    if resp.status_code != 200: return False
    
    # 5. Delete Task
    print("\n5. Delete Task...")
    resp = requests.post(f"{BASE_URL}/delete_task", params={"user_id": USER_ID, "task_id": task_id})
    print(f"Status: {resp.status_code}, Response: {resp.json()}")
    if resp.status_code != 200: return False
    
    return True

if __name__ == "__main__":
    if test_mcp_tools():
        print("\nMCP Tools Verification Successful!")
    else:
        print("\nMCP Tools Verification Failed.")
        sys.exit(1)
