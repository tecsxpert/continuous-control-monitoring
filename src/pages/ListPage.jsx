import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { SkeletonRow } from "../components/Skeleton";

const ListPage = () => {
  const [controls, setControls] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [riskFilter, setRiskFilter] = useState("ALL");
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    setTimeout(() => {
      const stored = JSON.parse(localStorage.getItem("controls")) || [];
      setControls(stored);
      setFiltered(stored);
      setLoading(false);
    }, 800);
  }, []);

  useEffect(() => {
    let result = controls;
    if (search.trim() !== "") {
      result = result.filter(
        (c) =>
          c.title.toLowerCase().includes(search.toLowerCase()) ||
          c.description.toLowerCase().includes(search.toLowerCase())
      );
    }
    if (statusFilter !== "ALL") result = result.filter((c) => c.status === statusFilter);
    if (riskFilter !== "ALL") result = result.filter((c) => c.riskLevel === riskFilter);
    setFiltered(result);
  }, [search, statusFilter, riskFilter, controls]);

  const handleDelete = (id) => {
    const confirm = window.confirm("Are you sure you want to delete?");
    if (!confirm) return;
    const updated = controls.filter((item) => item.id !== id);
    localStorage.setItem("controls", JSON.stringify(updated));
    setControls(updated);
  };

  const handleClearFilters = () => {
    setSearch("");
    setStatusFilter("ALL");
    setRiskFilter("ALL");
  };

  const handleExportCSV = () => {
    if (filtered.length === 0) { alert("No data to export!"); return; }
    const headers = ["ID", "Title", "Description", "Status", "Risk Level", "Score", "Assigned To"];
    const rows = filtered.map((c) => [c.id, `"${c.title}"`, `"${c.description}"`, c.status, c.riskLevel, c.score, `"${c.assignedTo}"`]);
    const csvContent = [headers.join(","), ...rows.map((r) => r.join(","))].join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "controls_export.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getStatusBadge = (status) => {
    const colors = {
      ACTIVE: "bg-green-100 text-green-700",
      INACTIVE: "bg-gray-100 text-gray-600",
      PENDING: "bg-yellow-100 text-yellow-700",
      OVERDUE: "bg-red-100 text-red-700",
    };
    return colors[status] || "bg-blue-100 text-blue-700";
  };

  const getRiskBadge = (risk) => {
    const colors = {
      LOW: "bg-green-100 text-green-700",
      MEDIUM: "bg-yellow-100 text-yellow-700",
      HIGH: "bg-orange-100 text-orange-700",
      CRITICAL: "bg-red-100 text-red-700",
    };
    return colors[risk] || "bg-gray-100 text-gray-600";
  };

  const isFilterActive = search !== "" || statusFilter !== "ALL" || riskFilter !== "ALL";

  return (
    <div className="min-h-screen bg-gray-50">

      {/* ✅ Responsive Navbar */}
      <Navbar />

      <div className="max-w-7xl mx-auto p-4 md:p-6">

        {/* ✅ Page Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 mb-6">
          <h2 className="text-2xl font-bold text-[#1B4F8A]">All Controls</h2>
          <div className="flex items-center gap-3 w-full md:w-auto">
            <span className="text-sm text-gray-500">
              Showing <span className="font-bold text-[#1B4F8A]">{filtered.length}</span> of <span className="font-bold">{controls.length}</span>
            </span>
            <button
              onClick={handleExportCSV}
              className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-semibold transition ml-auto md:ml-0"
            >
              ⬇️ Export CSV
            </button>
          </div>
        </div>

        {/* ✅ Search + Filter Bar */}
        <div className="bg-white rounded-2xl shadow p-4 mb-6">
          <div className="flex flex-col md:flex-row gap-3">
            <div className="flex-1 relative">
              <span className="absolute left-3 top-2.5 text-gray-400 text-sm">🔍</span>
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search by title or description..."
                className="w-full border border-gray-300 rounded-lg pl-8 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              {search && (
                <button onClick={() => setSearch("")} className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600 text-sm">✕</button>
              )}
            </div>

            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white"
            >
              <option value="ALL">All Status</option>
              <option value="ACTIVE">Active</option>
              <option value="INACTIVE">Inactive</option>
              <option value="PENDING">Pending</option>
              <option value="OVERDUE">Overdue</option>
            </select>

            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
              className="border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white"
            >
              <option value="ALL">All Risk Levels</option>
              <option value="LOW">Low</option>
              <option value="MEDIUM">Medium</option>
              <option value="HIGH">High</option>
              <option value="CRITICAL">Critical</option>
            </select>

            {isFilterActive && (
              <button onClick={handleClearFilters} className="bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 px-4 py-2 rounded-lg text-sm font-semibold transition">
                ✕ Clear
              </button>
            )}
          </div>

          {isFilterActive && (
            <div className="flex flex-wrap gap-2 mt-3">
              {search && <span className="bg-blue-100 text-blue-700 text-xs px-3 py-1 rounded-full">Search: "{search}"</span>}
              {statusFilter !== "ALL" && <span className="bg-green-100 text-green-700 text-xs px-3 py-1 rounded-full">Status: {statusFilter}</span>}
              {riskFilter !== "ALL" && <span className="bg-yellow-100 text-yellow-700 text-xs px-3 py-1 rounded-full">Risk: {riskFilter}</span>}
            </div>
          )}
        </div>

        {/* ✅ Loading Skeleton */}
        {loading ? (
          <div className="bg-white rounded-2xl shadow overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-[#1B4F8A] text-white">
                <tr>
                  {["#", "Title", "Description", "Status", "Risk", "Score", "Assigned To", "Actions"].map((h) => (
                    <th key={h} className="text-left px-4 py-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {[...Array(5)].map((_, i) => <SkeletonRow key={i} />)}
              </tbody>
            </table>
          </div>

        ) : controls.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-24 text-gray-400">
            <div className="text-7xl mb-4">📋</div>
            <p className="text-xl font-semibold mb-2 text-gray-600">No controls yet</p>
            <p className="text-sm mb-6">Start monitoring by adding your first control</p>
            <button onClick={() => navigate("/add")} className="bg-[#1B4F8A] text-white px-6 py-2.5 rounded-lg hover:bg-blue-800 transition font-semibold">
              + Add Your First Control
            </button>
          </div>

        ) : filtered.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-24 text-gray-400">
            <div className="text-7xl mb-4">🔍</div>
            <p className="text-xl font-semibold mb-2 text-gray-600">No results found</p>
            <p className="text-sm mb-6">Try a different search or clear filters</p>
            <button onClick={handleClearFilters} className="bg-[#1B4F8A] text-white px-6 py-2.5 rounded-lg hover:bg-blue-800 transition font-semibold">
              Clear All Filters
            </button>
          </div>

        ) : (
          <>
            {/* ✅ Desktop Table — hidden on mobile */}
            <div className="hidden md:block bg-white rounded-2xl shadow overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-[#1B4F8A] text-white">
                  <tr>
                    <th className="text-left px-4 py-3">#</th>
                    <th className="text-left px-4 py-3">Title</th>
                    <th className="text-left px-4 py-3">Description</th>
                    <th className="text-left px-4 py-3">Status</th>
                    <th className="text-left px-4 py-3">Risk Level</th>
                    <th className="text-left px-4 py-3">Score</th>
                    <th className="text-left px-4 py-3">Assigned To</th>
                    <th className="text-left px-4 py-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((control, index) => (
                    <tr key={control.id} className="border-b hover:bg-blue-50 transition">
                      <td className="px-4 py-3 text-gray-500">{index + 1}</td>
                      <td className="px-4 py-3 font-semibold text-gray-800">
                        {search
                          ? control.title.split(new RegExp(`(${search})`, "gi")).map((part, i) =>
                              part.toLowerCase() === search.toLowerCase()
                                ? <mark key={i} className="bg-yellow-200 rounded">{part}</mark>
                                : part
                            )
                          : control.title}
                      </td>
                      <td className="px-4 py-3 text-gray-600 max-w-xs truncate">{control.description}</td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getStatusBadge(control.status)}`}>{control.status}</span>
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getRiskBadge(control.riskLevel)}`}>{control.riskLevel}</span>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          <div className="w-16 bg-gray-200 rounded-full h-2">
                            <div className="bg-[#1B4F8A] h-2 rounded-full" style={{ width: `${control.score}%` }} />
                          </div>
                          <span className="text-gray-700 font-medium">{control.score}</span>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-gray-700">{control.assignedTo}</td>
                      <td className="px-4 py-3">
                        <div className="flex gap-2">
                          <button onClick={() => navigate("/detail", { state: control })} className="bg-[#1B4F8A] hover:bg-blue-800 text-white px-3 py-1 rounded-lg text-xs font-semibold transition">View</button>
                          <button onClick={() => navigate("/edit", { state: control })} className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded-lg text-xs font-semibold transition">Edit</button>
                          <button onClick={() => handleDelete(control.id)} className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-lg text-xs font-semibold transition">Delete</button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* ✅ Mobile Cards — shown only on mobile */}
            <div className="md:hidden space-y-4">
              {filtered.map((control, index) => (
                <div key={control.id} className="bg-white rounded-2xl shadow p-4">

                  {/* Card Header */}
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="font-bold text-gray-800 text-base flex-1 pr-2">
                      {index + 1}. {control.title}
                    </h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold shrink-0 ${getStatusBadge(control.status)}`}>
                      {control.status}
                    </span>
                  </div>

                  {/* Description */}
                  <p className="text-gray-500 text-sm mb-3 line-clamp-2">
                    {control.description}
                  </p>

                  {/* Details Row */}
                  <div className="grid grid-cols-2 gap-2 mb-3 text-sm">
                    <div>
                      <p className="text-gray-400 text-xs">Risk Level</p>
                      <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${getRiskBadge(control.riskLevel)}`}>
                        {control.riskLevel}
                      </span>
                    </div>
                    <div>
                      <p className="text-gray-400 text-xs">Assigned To</p>
                      <p className="font-semibold text-gray-700 text-xs">{control.assignedTo}</p>
                    </div>
                  </div>

                  {/* Score Bar */}
                  <div className="mb-3">
                    <div className="flex justify-between text-xs text-gray-500 mb-1">
                      <span>Score</span>
                      <span className="font-bold">{control.score}/100</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-[#1B4F8A] h-2 rounded-full"
                        style={{ width: `${control.score}%` }}
                      />
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex gap-2">
                    <button
                      onClick={() => navigate("/detail", { state: control })}
                      className="flex-1 bg-[#1B4F8A] hover:bg-blue-800 text-white py-2 rounded-lg text-xs font-semibold transition"
                    >
                      View
                    </button>
                    <button
                      onClick={() => navigate("/edit", { state: control })}
                      className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg text-xs font-semibold transition"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(control.id)}
                      className="flex-1 bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg text-xs font-semibold transition"
                    >
                      Delete
                    </button>
                  </div>

                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ListPage;