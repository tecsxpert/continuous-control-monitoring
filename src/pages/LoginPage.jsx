import { useState } from "react";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    if (username.trim() === "" || password.trim() === "") {
      setError("Please enter both username and password");
      return;
    }

    localStorage.setItem("loggedIn", "true");
    localStorage.setItem("user", username);
    navigate("/");
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-br from-blue-100 to-purple-100">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-96">

        {/* Logo / Title */}
        <div className="text-center mb-6">
          <div className="text-5xl mb-2">🛡️</div>
          <h1 className="text-2xl font-bold text-[#1B4F8A]">
            Control Monitoring
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            Sign in to your account
          </p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-300 text-red-600 text-sm px-4 py-2 rounded-lg">
              {error}
            </div>
          )}

          {/* Username */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <input
              placeholder="Enter your username"
              className="border border-gray-300 p-2 w-full rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
              value={username}
              onChange={(e) => {
                setUsername(e.target.value);
                setError("");
              }}
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              placeholder="Enter your password"
              className="border border-gray-300 p-2 w-full rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setError("");
              }}
            />
          </div>

          {/* Submit */}
          <button className="bg-[#1B4F8A] hover:bg-blue-800 text-white w-full py-2.5 rounded-lg font-semibold transition">
            Login
          </button>

        </form>

        <p className="text-center text-xs text-gray-400 mt-6">
          Continuous Control Monitoring System
        </p>

      </div>
    </div>
  );
};

export default LoginPage;