import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

const EditPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const control = location.state;
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    title: "",
    description: "",
    status: "ACTIVE",
    riskLevel: "MEDIUM",
    score: "",
    assignedTo: "",
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (control) setForm(control);
  }, [control]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: "" });
  };

  const validate = () => {
    const newErrors = {};
    if (!form.title.trim()) newErrors.title = "Title is required";
    if (!form.description.trim()) newErrors.description = "Description is required";
    if (!form.assignedTo.trim()) newErrors.assignedTo = "Assigned To is required";
    if (!form.score || isNaN(form.score) || form.score < 0 || form.score > 100)
      newErrors.score = "Score must be between 0 and 100";
    return newErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);
    setTimeout(() => {
      const controls = JSON.parse(localStorage.getItem("controls")) || [];
      const updated = controls.map((item) =>
        item.id === control.id ? { ...item, ...form, score: Number(form.score) } : item
      );
      localStorage.setItem("controls", JSON.stringify(updated));
      setLoading(false);
      navigate("/");
    }, 600);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-2xl mx-auto p-4 md:p-6">

        <div className="mb-6">
          <h2 className="text-2xl font-bold text-[#1B4F8A]">Edit Control</h2>
          <p className="text-gray-500 text-sm mt-1">Update the details of this control</p>
        </div>

        <div className="bg-white rounded-2xl shadow p-6 md:p-8">
          <form onSubmit={handleSubmit} className="space-y-5">

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">
                Title <span className="text-red-500">*</span>
              </label>
              <input
                name="title"
                value={form.title}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              />
              {errors.title && <p className="text-red-500 text-xs mt-1">⚠️ {errors.title}</p>}
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">
                Description <span className="text-red-500">*</span>
              </label>
              <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
                rows={3}
                className="w-full border border-gray-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition resize-none"
              />
              {errors.description && <p className="text-red-500 text-xs mt-1">⚠️ {errors.description}</p>}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Status</label>
                <select
                  name="status"
                  value={form.status}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white transition"
                >
                  <option value="ACTIVE">Active</option>
                  <option value="INACTIVE">Inactive</option>
                  <option value="PENDING">Pending</option>
                  <option value="OVERDUE">Overdue</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Risk Level</label>
                <select
                  name="riskLevel"
                  value={form.riskLevel}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white transition"
                >
                  <option value="LOW">Low</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="HIGH">High</option>
                  <option value="CRITICAL">Critical</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">
                  Score (0–100) <span className="text-red-500">*</span>
                </label>
                <input
                  name="score"
                  type="number"
                  value={form.score}
                  onChange={handleChange}
                  min="0"
                  max="100"
                  className="w-full border border-gray-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
                />
                {errors.score && <p className="text-red-500 text-xs mt-1">⚠️ {errors.score}</p>}
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">
                  Assigned To <span className="text-red-500">*</span>
                </label>
                <input
                  name="assignedTo"
                  value={form.assignedTo}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
                />
                {errors.assignedTo && <p className="text-red-500 text-xs mt-1">⚠️ {errors.assignedTo}</p>}
              </div>
            </div>

            <div className="flex gap-3 pt-2">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-[#1B4F8A] hover:bg-blue-800 disabled:bg-gray-400 text-white py-3 rounded-xl font-semibold transition flex items-center justify-center gap-2 text-sm"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Updating...
                  </>
                ) : "✅ Update Control"}
              </button>
              <button
                type="button"
                onClick={() => navigate("/")}
                className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 py-3 rounded-xl font-semibold transition text-sm"
              >
                Cancel
              </button>
            </div>

          </form>
        </div>
      </div>
    </div>
  );
};

export default EditPage;