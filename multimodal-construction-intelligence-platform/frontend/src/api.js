
const API_BASE_URL =
  "https://multimodal-construction-intelligence-bgii.onrender.com";

async function req(path, opts = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, opts);
  } catch (error) {
    console.error("Network or CORS error:", error);

    throw new Error(
      "Cannot connect to the backend. Check the backend deployment and CORS settings."
    );
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : `Backend request failed (${response.status}).`
    );
  }

  return data;
}

export const getDashboard = () => req("/api/dashboard");

export const getAnalyses = () => req("/api/analyses");

export const getHealth = () => req("/api/health");

export const postForm = (path, form) =>
  req(path, {
    method: "POST",
    body: form,
  });

export const postJson = (path, body) =>
  req(path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
