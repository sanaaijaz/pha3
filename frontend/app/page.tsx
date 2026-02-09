"use client";

import { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import Navbar from '@/components/Navbar';
import TodoItem from '@/components/TodoItem';
import ChatSidebar from '@/components/ChatSidebar';
import api from '@/lib/api';
import { Plus, Loader2, CheckCircle } from 'lucide-react';

export interface Todo {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
}

export default function Home() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);

  // New todo state
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  const fetchTodos = async () => {
    try {
      const res = await api.get('/todos/');
      // Sort: Incomplete first, then by date descending (newest first)
      const sorted = res.data.sort((a: Todo, b: Todo) => {
        if (a.completed === b.completed) {
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        }
        return a.completed ? 1 : -1;
      });
      setTodos(sorted);
    } catch (error) {
      console.error("Failed to fetch todos", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      fetchTodos();
    }
  }, [user]);

  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    try {
      const res = await api.post('/todos/', {
        title: newTitle,
        description: newDesc,
      });
      setTodos([res.data, ...todos]);
      setNewTitle('');
      setNewDesc('');
      setIsAdding(false);
    } catch (error) {
      console.error("Failed to add todo", error);
    }
  };

  const handleToggle = async (id: number) => {
    // Optimistic update
    const updatedTodos = todos.map(t =>
      t.id === id ? { ...t, completed: !t.completed } : t
    );
    setTodos(updatedTodos);

    try {
      await api.patch(`/todos/${id}/complete`);
      fetchTodos(); // Re-fetch to confirm sort order
    } catch (error) {
      console.error("Failed to toggle", error);
      fetchTodos(); // Revert on error
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure?")) return;
    try {
      await api.delete(`/todos/${id}`);
      setTodos(todos.filter(t => t.id !== id));
    } catch (error) {
      console.error("Failed to delete", error);
    }
  };

  const handleUpdate = async (id: number, title: string, description: string) => {
    try {
      await api.put(`/todos/${id}`, { title, description });
      setTodos(todos.map(t => t.id === id ? { ...t, title, description } : t));
    } catch (error) {
      console.error("Failed to update", error);
    }
  };

  if (authLoading || !user) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/20 via-slate-900 to-slate-900">
      <Navbar />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-24">

        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
          <div>
            <h1 className="text-3xl font-bold text-white tracking-tight">My Tasks</h1>
            <p className="text-slate-400 mt-1">
              You have {todos.filter(t => !t.completed).length} pending tasks
            </p>
          </div>

          <button
            onClick={() => setIsAdding(!isAdding)}
            className={`group flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium transition-all duration-300 shadow-lg ${isAdding
              ? "bg-slate-800 text-slate-300 hover:bg-slate-700"
              : "bg-indigo-600 text-white hover:bg-indigo-700 hover:shadow-indigo-500/25"
              }`}
          >
            <Plus className={`w-5 h-5 transition-transform duration-300 ${isAdding ? "rotate-45" : ""}`} />
            {isAdding ? "Cancel" : "Add New Task"}
          </button>
        </div>

        {/* Add Task Form with Animation */}
        <div className={`overflow-hidden transition-all duration-500 ease-in-out ${isAdding ? "max-h-96 opacity-100 mb-8" : "max-h-0 opacity-0"}`}>
          <form onSubmit={handleAddTodo} className="bg-slate-800/50 backdrop-blur-md border border-white/5 p-6 rounded-2xl shadow-xl">
            <div className="space-y-4">
              <div>
                <input
                  type="text"
                  placeholder="What needs to be done?"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full bg-slate-900/50 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all text-lg"
                  autoFocus
                />
              </div>
              <div>
                <textarea
                  placeholder="Add details (optional)"
                  value={newDesc}
                  onChange={(e) => setNewDesc(e.target.value)}
                  className="w-full bg-slate-900/50 border border-white/10 rounded-xl px-4 py-3 text-slate-300 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all resize-none h-24"
                />
              </div>
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={!newTitle.trim()}
                  className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-2.5 rounded-xl font-medium shadow-lg shadow-indigo-500/20 transition-all hover:scale-105 active:scale-95"
                >
                  Create Task
                </button>
              </div>
            </div>
          </form>
        </div>

        {/* Todo List */}
        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
          </div>
        ) : todos.length === 0 ? (
          <div className="text-center py-20 bg-slate-800/30 rounded-3xl border border-white/5 border-dashed">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-800 mb-4 text-slate-600">
              <CheckCircle className="w-8 h-8" />
            </div>
            <h3 className="text-xl font-medium text-slate-300">All caught up!</h3>
            <p className="text-slate-500 mt-2 max-w-sm mx-auto">
              You have no tasks on your list. Enjoy your free time or add a new task to get started.
            </p>
            <button
              onClick={() => setIsAdding(true)}
              className="mt-6 text-indigo-400 hover:text-indigo-300 font-medium hover:underline"
            >
              Create your first task
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {todos.map((todo) => (
              <TodoItem
                key={todo.id}
                todo={todo}
                onToggle={handleToggle}
                onDelete={handleDelete}
                onUpdate={handleUpdate}
              />
            ))}
          </div>
        )}
      </main>
      <ChatSidebar />
    </div>
  );
}
