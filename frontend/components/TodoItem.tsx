"use client";

import { Todo } from '@/app/page';
import { Trash2, Edit2, CheckCircle, Circle, X } from 'lucide-react';
import { useState } from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface TodoItemProps {
    todo: Todo;
    onToggle: (id: number) => void;
    onDelete: (id: number) => void;
    onUpdate: (id: number, title: string, description: string) => void;
}

export function cn(...inputs: (string | undefined | null | false)[]) {
    return twMerge(clsx(inputs));
}

export default function TodoItem({ todo, onToggle, onDelete, onUpdate }: TodoItemProps) {
    const [isEditing, setIsEditing] = useState(false);
    const [editTitle, setEditTitle] = useState(todo.title);
    const [editDesc, setEditDesc] = useState(todo.description || '');

    const handleSave = () => {
        onUpdate(todo.id, editTitle, editDesc);
        setIsEditing(false);
    };

    return (
        <div className={cn(
            "group relative bg-slate-800/40 backdrop-blur-sm border border-white/5 rounded-xl p-4 transition-all duration-300 hover:bg-slate-800/60 hover:border-white/10 hover:shadow-lg hover:shadow-purple-500/10",
            todo.completed && "opacity-75"
        )}>
            {isEditing ? (
                <div className="space-y-3">
                    <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="w-full bg-slate-900/50 border border-white/10 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                        placeholder="Task title"
                        autoFocus
                    />
                    <textarea
                        value={editDesc}
                        onChange={(e) => setEditDesc(e.target.value)}
                        className="w-full bg-slate-900/50 border border-white/10 rounded-lg px-3 py-2 text-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500/50 resize-none min-h-[60px]"
                        placeholder="Description (optional)"
                    />
                    <div className="flex justify-end gap-2">
                        <button
                            onClick={() => setIsEditing(false)}
                            className="px-3 py-1.5 text-xs font-medium text-slate-400 hover:text-white transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            onClick={handleSave}
                            className="bg-purple-600 hover:bg-purple-700 text-white px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
                        >
                            Save Changes
                        </button>
                    </div>
                </div>
            ) : (
                <div className="flex items-start gap-4">
                    <button
                        onClick={() => onToggle(todo.id)}
                        className={cn(
                            "mt-1 flex-shrink-0 transition-colors duration-300",
                            todo.completed ? "text-purple-400" : "text-slate-500 hover:text-purple-400"
                        )}
                    >
                        {todo.completed ? <CheckCircle className="w-6 h-6" /> : <Circle className="w-6 h-6" />}
                    </button>

                    <div className="flex-grow min-w-0">
                        <h3 className={cn(
                            "text-lg font-medium transition-all duration-300 truncate pr-8",
                            todo.completed ? "text-slate-500 line-through decoration-slate-600" : "text-slate-100"
                        )}>
                            {todo.title}
                        </h3>
                        {todo.description && (
                            <p className={cn(
                                "text-sm mt-1 transition-all duration-300 line-clamp-2",
                                todo.completed ? "text-slate-600" : "text-slate-400"
                            )}>
                                {todo.description}
                            </p>
                        )}
                        <p className="text-xs text-slate-600 mt-2">
                            Created {new Date(todo.created_at).toLocaleDateString()}
                        </p>
                    </div>

                    <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity absolute top-4 right-4 bg-slate-800/80 rounded-lg p-1">
                        <button
                            onClick={() => setIsEditing(true)}
                            className="p-1.5 text-slate-400 hover:text-indigo-400 hover:bg-indigo-400/10 rounded-md transition-all"
                            title="Edit"
                        >
                            <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                            onClick={() => onDelete(todo.id)}
                            className="p-1.5 text-slate-400 hover:text-red-400 hover:bg-red-400/10 rounded-md transition-all"
                            title="Delete"
                        >
                            <Trash2 className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
