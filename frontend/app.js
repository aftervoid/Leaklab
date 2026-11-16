const title = document.querySelector("#status-title");
const detail = document.querySelector("#status-detail");
const indicator = document.querySelector("#status-indicator");

async function checkApi() {
  try {
    const response = await fetch("/api/health", { headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    title.textContent = "API is online";
    detail.textContent = `Environment: ${data.environment} · Data policy: ${data.data_policy}`;
    indicator.classList.add("online");
  } catch (error) {
    title.textContent = "API is not reachable";
    detail.textContent = "Start the local server with: uvicorn leaklab.api:app --reload";
    indicator.classList.add("offline");
  }
}

checkApi();
