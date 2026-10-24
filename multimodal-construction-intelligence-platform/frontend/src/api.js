
const API_BASE_URL = 'https://multimodal-construction-intelligence-bgii.onrender.com';

async function req(path, opts = {}) {
  const r = await fetch(`${API_BASE_URL}${path}`, opts);
  const d = await r.json().catch(() => ({}));

  if (!r.ok) {
    throw new Error(
      d.detail || 'Request failed. Please check the backend.'
    );
  }

  return d;
}

export const getDashboard = () => req('/api/dashboard');

export const getAnalyses = () => req('/api/analyses');

export const getHealth = () => req('/api/health');

export const postForm = (path, form) =>
  req(path, { method: 'POST', body: form });

export const postJson = (path, body) =>
  req(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
