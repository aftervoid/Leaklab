const title = document.querySelector("#status-title");
const detail = document.querySelector("#status-detail");
const indicator = document.querySelector("#status-indicator");
const researchTitle = document.querySelector("#research-title");
const researchDetail = document.querySelector("#research-detail");

async function checkApi() {
  try {
    const response = await fetch("/api/health", { headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    title.textContent = "API is online";
    detail.textContent = `Environment: ${data.environment} · Data policy: ${data.data_policy}`;
    indicator.classList.add("online");
  } catch {
    title.textContent = "API is not reachable";
    detail.textContent = "Start the local server with: uvicorn leaklab.api:app --reload";
    indicator.classList.add("offline");
  }
}

async function loadResearchSummary() {
  try {
    const response = await fetch("/api/password-lab/summary?count=1000");
    if (!response.ok) throw new Error("Summary request failed");
    const data = await response.json();
    researchTitle.textContent = `${data.samples_analyzed.toLocaleString()} synthetic samples analyzed`;
    researchDetail.textContent = `Average length: ${data.average_length} characters · Patterns: ${Object.entries(data.patterns).map(([key, value]) => `${key.replaceAll("_", " ")} ${value}`).join(" · ")}`;
  } catch {
    researchTitle.textContent = "Sample analysis unavailable";
    researchDetail.textContent = "Check that the local API is running.";
  }
}

checkApi();
loadResearchSummary();
