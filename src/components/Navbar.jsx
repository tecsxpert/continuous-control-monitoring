// Day 13 — Responsive Navbar with hamburger menu
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Navbar = ({ title = "🛡️ Control Monitoring" }) => {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("loggedIn");
    localStorage.removeItem("user");
    navigate("/login");
  };

  const navLinks = [
    { label: "📋 List", path: "/" },
    { label: "📊 Dashboard", path: "/dashboard" },
    { label: "📈 Analytics", path: "/analytics" },
    { label: "📄 AI Report", path: "/report" },
    { label: "+ Add Control", path: "/add" },
  ];

  return (
    <nav className="bg-[#1B4F8A] text-white shadow">

      {/* ✅ Main navbar row */}
      <div className="px-6 py-4 flex justify-between items-center">

        {/* Logo */}
        <h1
          className="text-xl font-bold cursor-pointer"
          onClick={() => navigate("/")}
        >
          {title}
        </h1>

        {/* ✅ Desktop menu — hidden on mobile */}
        <div className="hidden md:flex gap-3 items-center">
          {navLinks.map((link) => (
            <button
              key={link.path}
              onClick={() => navigate(link.path)}
              className="bg-white bg-opacity-10 hover:bg-opacity-20 text-white px-3 py-1.5 rounded-lg text-sm font-semibold transition"
            >
              {link.label}
            </button>
          ))}
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white px-3 py-1.5 rounded-lg text-sm font-semibold transition"
          >
            Logout
          </button>
        </div>

        {/* ✅ Mobile hamburger button — shown only on mobile */}
        <button
          className="md:hidden text-white text-2xl focus:outline-none"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          {menuOpen ? "✕" : "☰"}
        </button>

      </div>

      {/* ✅ Mobile dropdown menu */}
      {menuOpen && (
        <div className="md:hidden bg-[#163d6e] px-6 py-4 space-y-2">
          {navLinks.map((link) => (
            <button
              key={link.path}
              onClick={() => {
                navigate(link.path);
                setMenuOpen(false);
              }}
              className="block w-full text-left text-white px-4 py-2 rounded-lg hover:bg-white hover:bg-opacity-10 text-sm font-semibold transition"
            >
              {link.label}
            </button>
          ))}
          <button
            onClick={handleLogout}
            className="block w-full text-left text-red-300 hover:text-red-200 px-4 py-2 rounded-lg hover:bg-white hover:bg-opacity-10 text-sm font-semibold transition"
          >
            Logout
          </button>
        </div>
      )}

    </nav>
  );
};

export default Navbar;