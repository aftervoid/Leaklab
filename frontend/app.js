const $ = (selector) => document.querySelector(selector);
const number = (value) => Number(value || 0).toLocaleString();
const titles = { overview: "Overview", research: "Password research", datasets: "Dataset center", system: "System status" };
let datasetIndex = null;
let toastTimer;

function notify(message) {
  const toast = $("#toast");
  toast.textContent = message;
  toast.classList.add("visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("visible"), 2600);
}

async function getJson(url) {
  const response = await fetch(url, { headers: { Accept: "application/json" } });
  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try { detail = (await response.json()).detail || detail; } catch {}
    throw new Error(detail);
  }
  return response.json();
}

function showView(name) {
  if (!titles[name]) return;
  document.querySelectorAll(".view").forEach((view) => view.classList.toggle("active", view.id === `view-${name}`));
  document.querySelectorAll(".nav-link").forEach((link) => link.classList.toggle("active", link.dataset.view === name));
  $("#page-title").textContent = titles[name];
}

function renderBars(container, values) {
  container.replaceChildren();
  const entries = Object.entries(values || {});
  if (!entries.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No aggregate values available.";
    container.append(empty);
    return;
  }
  const max = Math.max(...entries.map(([, value]) => Number(value) || 0), 1);
  for (const [label, rawValue] of entries) {
    const value = Number(rawValue) || 0;
    const row = document.createElement("div");
    row.className = "bar-row";
    const heading = document.createElement("div");
    heading.className = "bar-label";
    const name = document.createElement("span");
    name.textContent = label.replaceAll("_", " ");
    const amount = document.createElement("strong");
    amount.textContent = number(value);
    heading.append(name, amount);
    const track = document.createElement("div");
    track.className = "bar-track";
    const fill = document.createElement("span");
    fill.style.width = `${Math.max(0, Math.min(100, (value / max) * 100))}%`;
    track.append(fill);
    row.append(heading, track);
    container.append(row);
  }
}

function renderDatasetTable(datasets) {
  const body = $("#dataset-table");
  body.replaceChildren();
  if (!datasets.length) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 5;
    cell.className = "muted";
    cell.textContent = "No daily datasets found in this local checkout.";
    row.append(cell);
    body.append(row);
    return;
  }
  for (const item of datasets) {
    const row = document.createElement("tr");
    const values = [
      item.dataset_date || "—",
      number(item.record_count),
      number(item.password_sample_count),
      item.split_complete ? "Complete" : "Pending",
      item.seed ?? "—",
    ];
    values.forEach((value, index) => {
      const cell = document.createElement("td");
      cell.textContent = value;
      if (index === 3) {
        const status = document.createElement("span");
        status.className = item.split_complete ? "table-status complete" : "table-status pending";
        status.textContent = value;
        cell.replaceChildren(status);
      }
      row.append(cell);
    });
    body.append(row);
  }
}

function renderLatest(item) {
  const target = $("#latest-dataset");
  target.replaceChildren();
  if (!item) {
    target.textContent = "No generated daily dataset was found.";
    return;
  }
  const date = document.createElement("strong");
  date.className = "snapshot-date";
  date.textContent = item.dataset_date;
  const details = document.createElement("p");
  details.textContent = `${number(item.record_count)} profile records · ${number(item.password_sample_count)} password samples`;
  const chunks = document.createElement("p");
  chunks.className = "muted";
  chunks.textContent = `${number(item.records_chunks)} profile chunks · ${number(item.password_chunks)} password chunks`;
  target.append(date, details, chunks);
  $("#dataset-state").textContent = item.split_complete ? "Split complete" : "Split pending";
  $("#dataset-state").className = item.split_complete ? "state-pill success" : "state-pill warning";
}

async function loadDatasets() {
  const data = await getJson("/api/datasets");
  datasetIndex = data;
  const datasets = data.datasets || [];
  const latest = data.latest;
  $("#metric-datasets").textContent = number(data.dataset_count);
  $("#metric-records").textContent = latest ? number(latest.record_count) : "—";
  $("#metric-passwords").textContent = latest ? number(latest.password_sample_count) : "—";
  $("#metric-average").textContent = latest ? `${latest.average_length} chars` : "—";
  $("#metric-datasets-note").textContent = latest ? `Latest: ${latest.dataset_date}` : "No datasets indexed";
  $("#dataset-total").textContent = `${number(data.dataset_count)} datasets`;
  $("#system-index").textContent = `${number(data.dataset_count)} indexed`;
  renderLatest(latest);
  renderDatasetTable(datasets);
}

async function runAnalysis() {
  const count = Number($("#sample-count").value);
  $("#analyze-button").disabled = true;
  $("#analyze-button").textContent = "Analyzing…";
  try {
    const data = await getJson(`/api/password-lab/summary?count=${count}`);
    $("#research-count").textContent = number(data.samples_analyzed);
    $("#research-average").textContent = `${data.average_length} chars`;
    $("#research-pattern-count").textContent = number(Object.keys(data.patterns || {}).length);
    renderBars($("#pattern-chart"), data.patterns);
    renderBars($("#rating-chart"), data.ratings);
    notify("Synthetic sample analysis completed.");
  } catch (error) {
    notify(error.message);
  } finally {
    $("#analyze-button").disabled = false;
    $("#analyze-button").innerHTML = 'Run analysis <span>↗</span>';
  }
}

async function loadSystem() {
  const [health, config] = await Promise.all([getJson("/api/health"), getJson("/api/config")]);
  $("#api-state").textContent = "Operational";
  $("#api-state").className = "state-pill success";
  $("#system-environment").textContent = health.environment;
  $("#system-policy").textContent = health.data_policy;
  $("#system-version").textContent = config.version;
  $("#system-default").textContent = number(config.default_records);
}

async function refreshDashboard() {
  $("#refresh-button").classList.add("spinning");
  try {
    await Promise.all([loadDatasets(), loadSystem()]);
    $("#last-updated").textContent = `Updated ${new Date().toLocaleTimeString()}`;
  } catch (error) {
    $("#api-state").textContent = "Unavailable";
    $("#api-state").className = "state-pill warning";
    notify(`Could not refresh dashboard: ${error.message}`);
  } finally {
    $("#refresh-button").classList.remove("spinning");
  }
}

document.querySelectorAll("[data-view]").forEach((button) => button.addEventListener("click", () => showView(button.dataset.view)));
document.querySelectorAll("[data-go]").forEach((button) => button.addEventListener("click", () => showView(button.dataset.go)));
$("#analyze-button").addEventListener("click", runAnalysis);
$("#refresh-button").addEventListener("click", refreshDashboard);
$("#datasets-reload").addEventListener("click", () => loadDatasets().then(() => notify("Dataset index refreshed.")).catch((error) => notify(error.message)));

refreshDashboard();
runAnalysis();
