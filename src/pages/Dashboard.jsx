import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, CartesianGrid, Legend
} from "recharts";
import Navbar from "../components/Navbar";

const COLORS = ["#1B4F8A", "#22c55e", "#f97316", "#ef4444", "#a855f7"];

const Dashboard = () => {
  const [controls, setControls] = useState([]);
  const [kpis, setKpis] = useState({ total: 0, active: 0, overdue: 0, critical: 0 });
  const [statusData, setStatusData] = useState([]);
  const [riskData, setRiskData] = useState([]);
  const [scoreData, setScoreData] = useState([]);

  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem("controls")) || [];
    setControls(stored);

    setKpis({
      total: stored.length,
      active: stored.filter((c) => c.status === "ACTIVE").length,
      overdue: stored.filter((c) => c.status === "OVERDUE").length,
      critical: stored.filter((c) => c.riskLevel === "CRITICAL").length,
    });

    const statusMap = {};
    stored.forEach((c) => {
      statusMap[c.status] = (statusMap[c.status] || 0) + 1;
    });
    setStatusData(Object.keys(statusMap).map((key) => ({ name: key, count: statusMap[key] })));

    const riskMap = {};
    stored.forEach((c) => {
      riskMap[c.riskLevel] = (riskMap[c.riskLevel] || 0) + 1;
    });
    setRiskData(Object.keys(riskMap).map((key) => ({ name: key, count: riskMap[key] })));

    setScoreData(
      stored.map((c) => ({
        name: c.title.length > 10 ? c.title.substring(0, 10) + "..." : c.title,
        score: Number(c.score),
      }))
    );
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">

      {/* ✅ Responsive Navbar */}
      <Navbar />

      <div className="max-w-7xl mx-auto p-4 md:p-6">

        <h2 className="text-2xl font-bold text-[#1B4F8A] mb-6">
          Dashboard Analytics
        </h2>

        {/* ✅ KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-2xl shadow p-5 border-l-4 border-blue-500">
            <p className="text-sm text-gray-500">Total Controls</p>
            <p className="text-3xl font-bold text-[#1B4F8A]">{kpis.total}</p>
          </div>
          <div className="bg-white rounded-2xl shadow p-5 border-l-4 border-green-500">
            <p className="text-sm text-gray-500">Active</p>
            <p className="text-3xl font-bold text-green-600">{kpis.active}</p>
          </div>
          <div className="bg-white rounded-2xl shadow p-5 border-l-4 border-red-500">
            <p className="text-sm text-gray-500">Overdue</p>
            <p className="text-3xl font-bold text-red-600">{kpis.overdue}</p>
          </div>
          <div className="bg-white rounded-2xl shadow p-5 border-l-4 border-purple-500">
            <p className="text-sm text-gray-500">Critical Risk</p>
            <p className="text-3xl font-bold text-purple-600">{kpis.critical}</p>
          </div>
        </div>

        {/* ✅ Charts Row 1 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">

          <div className="bg-white rounded-2xl shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Controls by Status</h3>
            {statusData.length === 0 ? (
              <p className="text-gray-400 text-center py-10">No data yet</p>
            ) : (
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={statusData}>
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#1B4F8A" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>

          <div className="bg-white rounded-2xl shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Controls by Risk Level</h3>
            {riskData.length === 0 ? (
              <p className="text-gray-400 text-center py-10">No data yet</p>
            ) : (
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={riskData}
                    dataKey="count"
                    nameKey="name"
                    outerRadius={90}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {riskData.map((entry, index) => (
                      <Cell key={index} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>

        </div>

        {/* ✅ Line Chart */}
        <div className="bg-white rounded-2xl shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Control Scores Overview</h3>
          {scoreData.length === 0 ? (
            <p className="text-gray-400 text-center py-10">No data yet</p>
          ) : (
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={scoreData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#1B4F8A"
                  strokeWidth={2}
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

      </div>
    </div>
  );
};

export default Dashboard;