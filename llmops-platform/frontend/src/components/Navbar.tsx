'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { authService } from '@/lib/auth';
import { LogOut, Activity, MessageSquare, BarChart3, Upload, User, Sparkles } from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();
  const user = authService.getCurrentUser();

  const navItems = [
    { href: '/dashboard', label: 'Dashboard', icon: BarChart3 },
    { href: '/chat', label: 'Chat', icon: MessageSquare },
    { href: '/upload', label: 'Upload', icon: Upload },
  ];

  return (
    <nav className="glass sticky top-0 z-50 border-b border-gray-200/50">
      <div className="container mx-auto px-6">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <Link href="/dashboard" className="flex items-center space-x-3 group">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl blur-lg opacity-50 group-hover:opacity-75 transition-opacity"></div>
              <div className="relative bg-gradient-to-r from-blue-600 to-purple-600 p-2.5 rounded-2xl shadow-lg">
                <Activity className="h-6 w-6 text-white" />
              </div>
            </div>
            <div>
              <span className="text-xl font-bold gradient-text">LLMOps Monitor</span>
              <div className="flex items-center space-x-1 text-xs text-gray-500">
                <Sparkles className="h-3 w-3" />
                <span>Powered by Groq</span>
              </div>
            </div>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={
                    isActive
                      ? 'nav-link-active'
                      : 'nav-link-inactive'
                  }
                >
                  <div className="flex items-center space-x-2">
                    <Icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </div>
                </Link>
              );
            })}
          </div>

          {/* User Section */}
          <div className="flex items-center space-x-4">
            <div className="hidden sm:flex items-center space-x-3 px-4 py-2 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border border-blue-100">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center shadow-sm">
                <User className="h-4 w-4 text-white" />
              </div>
              <div className="text-sm">
                <div className="font-semibold text-gray-700">
                  {user?.username || 'User'}
                </div>
                <div className="text-xs text-gray-500 capitalize">
                  {user?.role || 'member'}
                </div>
              </div>
            </div>
            
            <button
              onClick={() => authService.logout()}
              className="flex items-center space-x-2 px-4 py-2 rounded-xl text-sm font-medium text-gray-600 hover:bg-red-50 hover:text-red-600 transition-all duration-200 border border-gray-200 hover:border-red-200"
            >
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
