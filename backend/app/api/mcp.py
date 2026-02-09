from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime
from app.database import get_session, engine
from app.models import Todo as Task  # Aliasing Todo to Task to match user's provided logic

router = APIRouter(prefix="/mcp", tags=["mcp"])

# Helper function to get a task and verify ownership
def get_task_by_id(user_id: int, task_id: int, session: Session):
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/add_task")
def add_task(user_id: int, title: str, description: Optional[str] = None, session: Session = Depends(get_session)):
    task = Task(user_id=user_id, title=title, description=description)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"task_id": task.id, "status": "created", "title": task.title}

@router.get("/list_tasks")
def list_tasks(user_id: int, status: str = "all", session: Session = Depends(get_session)) -> List[dict]:
    query = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(query).all()
    if status == "pending":
        tasks = [t for t in tasks if not t.completed]
    elif status == "completed":
        tasks = [t for t in tasks if t.completed]
    return [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]

@router.post("/complete_task")
def complete_task(user_id: int, task_id: int, session: Session = Depends(get_session)):
    task = get_task_by_id(user_id, task_id, session)
    task.completed = True
    # Note: our Todo model uses datetime.utcnow for created_at, but we don't have updated_at in the model currently.
    # Adding updated_at would require a model migration or update. 
    # For now, sticking strictly to existing model or following user's update logic if we update model.
    session.add(task)
    session.commit()
    return {"task_id": task.id, "status": "completed", "title": task.title}

@router.post("/delete_task")
def delete_task(user_id: int, task_id: int, session: Session = Depends(get_session)):
    task = get_task_by_id(user_id, task_id, session)
    session.delete(task)
    session.commit()
    return {"task_id": task.id, "status": "deleted", "title": task.title}

@router.post("/update_task")
def update_task(user_id: int, task_id: int, title: Optional[str] = None, description: Optional[str] = None, session: Session = Depends(get_session)):
    task = get_task_by_id(user_id, task_id, session)
    if title:
        task.title = title
    if description:
        task.description = description
    session.add(task)
    session.commit()
    return {"task_id": task.id, "status": "updated", "title": task.title}

from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_with_agent(request: ChatRequest, user_id: int = 1):
    # This is a placeholder for actual LLM logic.
    # In Phase III, this acts as the interface for the todo-agent.
    lower_msg = request.message.lower()
    if "list" in lower_msg or "show" in lower_msg:
        reply = "I've retrieved your tasks for you. Is there anything specific you'd like to change?"
    elif "add" in lower_msg or "create" in lower_msg:
        reply = "I can help with that. What's the name of the task you'd like to add?"
    else:
        reply = f"Hello! I'm your Todo assistant. I received your message: '{request.message}'. How can I help you with your tasks?"
    
    return {"reply": reply}
