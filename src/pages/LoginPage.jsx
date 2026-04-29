import { useState } from "react";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    if (username.trim() === "" || password.trim() === "") {
      setError("Please enter both username and password");
      return;
    }

    setLoading(true);
    setError("");

    // ✅ Simulate login delay
    setTimeout(() => {
      localStorage.setItem("loggedIn", "true");
      localStorage.setItem("user", username);
      setLoading(false);
      navigate("/");
    }, 800);
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md mx-4">

        {/* ✅ Logo */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-[#1B4F8A] rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
            <span className="text-3xl">🛡️</span>
          </div>
          <h1 className="text-2xl font-bold text-[#1B4F8A]">
            Control Monitoring
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            Sign in to your account
          </p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">

          {/* ✅ Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-300 text-red-600 text-sm px-4 py-3 rounded-xl">
              ⚠️ {error}
            </div>
          )}

          {/* ✅ Username */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">
              Username
            </label>
            <input
              placeholder="Enter your username"
              className="border border-gray-300 p-3 w-full rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 text-sm transition"
              value={username}
              onChange={(e) => { setUsername(e.target.value); setError(""); }}
            />
          </div>

          {/* ✅ Password */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              placeholder="Enter your password"
              className="border border-gray-300 p-3 w-full rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 text-sm transition"
              value={password}
              onChange={(e) => { setPassword(e.target.value); setError(""); }}
            />
          </div>

          {/* ✅ Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="bg-[#1B4F8A] hover:bg-blue-800 disabled:bg-gray-400 text-white w-full py-3 rounded-xl font-semibold transition flex items-center justify-center gap-2 text-sm"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Signing in...
              </>
            ) : "Sign In"}
          </button>

        </form>

        {/* ✅ Footer */}
        <div className="mt-6 pt-4 border-t border-gray-100 text-center">
          <p className="text-xs text-gray-400">
            Continuous Control Monitoring System
          </p>
          <p className="text-xs text-gray-300 mt-1">
            Version 1.0 — Capstone Project 2026
          </p>
        </div>

      </div>
    </div>
  );
};

export default LoginPage;