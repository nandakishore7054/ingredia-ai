"use client";

import { useAuth } from "@/context/AuthContext";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function ProfilePage() {
  const { user, logout } = useAuth();

  return (
    <ProtectedRoute>
      <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-2xl shadow-sm border border-gray-100">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">Profile</h1>

        <div className="mb-6">
          <p className="text-lg text-gray-700"><b>Name:</b> {user?.name}</p>
          <p className="text-lg text-gray-700"><b>Email:</b> {user?.email}</p>
        </div>

        <h2 className="text-xl font-semibold mt-8 mb-4 text-gray-800">❤️ Favorite Recipes</h2>
        <ul className="list-disc ml-6 space-y-1 text-gray-600">
          {user?.favorites?.map((f, i) => (
            <li key={i}>{f}</li>
          )) || <li>No favorites yet.</li>}
        </ul>

        <h2 className="text-xl font-semibold mt-8 mb-4 text-gray-800">📜 Cooking History</h2>
        <ul className="list-disc ml-6 space-y-1 text-gray-600">
          {user?.history?.map((h, i) => (
            <li key={i}>{h}</li>
          )) || <li>No history yet.</li>}
        </ul>

        <button
          onClick={logout}
          className="mt-8 bg-red-500 text-white px-6 py-2 rounded-full hover:bg-red-600 transition shadow-sm font-medium"
        >
          Logout
        </button>
      </div>
    </ProtectedRoute>
  );
}
