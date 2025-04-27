const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getSuggestions(profile) {
  const res = await fetch(`${API}/suggest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  return res.json();
}
