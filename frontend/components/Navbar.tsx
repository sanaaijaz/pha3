"use client";

import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { LogOut, LayoutList } from 'lucide-react';

export default function Navbar() {
    const { user, logout } = useAuth();

    if (!user) return null;

    return (
        <nav className="fixed top-0 w-full z-50 bg-slate-900/50 backdrop-blur-md border-b border-white/10">
            <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center gap-2">
                        <div className="bg-gradient-to-tr from-indigo-500 to-purple-500 p-2 rounded-lg">
                            <LayoutList className="w-6 h-6 text-white" />
                        </div>
                        <span className="text-xl font-bold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                            TaskFlow
                        </span>
                    </div>

                    <div className="flex items-center gap-4">
                        <span className="text-sm text-slate-400 hidden sm:block">{user.email}</span>
                        <button
                            onClick={logout}
                            className="bg-white/5 hover:bg-white/10 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 border border-white/5"
                        >
                            <LogOut className="w-4 h-4" />
                            <span className="hidden sm:inline">Logout</span>
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
}
