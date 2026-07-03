let queries = [];
let selectedQuery = null;

const statusEl = document.querySelector("#status");
const queryListEl = document.querySelector("#queryList");
const queryIdEl = document.querySelector("#queryId");
const queryTitleEl = document.querySelector("#queryTitle");
const queryDescriptionEl = document.querySelector("#queryDescription");
const paramsFormEl = document.querySelector("#paramsForm");
const resultsEl = document.querySelector("#results");
const runButton = document.querySelector("#runButton");
const copyButton = document.querySelector("#copyButton");

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

function setStatus(text, ok = true) {
  statusEl.textContent = text;
  statusEl.style.background = ok ? "#1d7a62" : "#9f3424";
}

function renderQueryList() {
  queryListEl.innerHTML = "";
  for (const query of queries) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `query-button${selectedQuery?.id === query.id ? " active" : ""}`;
    button.textContent = query.title;
    button.addEventListener("click", () => selectQuery(query.id));
    queryListEl.appendChild(button);
  }
}

function renderParams(query) {
  paramsFormEl.innerHTML = "";
  for (const param of query.params) {
    const label = document.createElement("label");
    label.textContent = param.name;
    const input = document.createElement("input");
    input.name = param.name;
    input.type = param.type === "number" ? "number" : "text";
    input.value = param.default ?? "";
    if (param.type === "number") {
      input.step = "any";
    }
    label.appendChild(input);
    paramsFormEl.appendChild(label);
  }
}

function selectQuery(queryId) {
  selectedQuery = queries.find((query) => query.id === queryId);
  if (!selectedQuery) return;
  queryIdEl.textContent = selectedQuery.id;
  queryTitleEl.textContent = selectedQuery.title;
  queryDescriptionEl.textContent = selectedQuery.description;
  renderParams(selectedQuery);
  renderQueryList();
  runSelectedQuery();
}

function buildQueryUrl() {
  const params = new URLSearchParams();
  for (const [key, value] of new FormData(paramsFormEl).entries()) {
    if (String(value).trim() !== "") {
      params.append(key, value);
    }
  }
  const suffix = params.toString() ? `?${params}` : "";
  return `/api/queries/${selectedQuery.id}${suffix}`;
}

async function runSelectedQuery() {
  if (!selectedQuery) return;
  runButton.disabled = true;
  runButton.textContent = "Execution...";
  try {
    const data = await fetchJson(buildQueryUrl());
    resultsEl.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    resultsEl.textContent = JSON.stringify({ error: error.message }, null, 2);
  } finally {
    runButton.disabled = false;
    runButton.textContent = "Executer";
  }
}

async function init() {
  try {
    await fetchJson("/api/health");
    setStatus("MongoDB OK");
  } catch (error) {
    setStatus("DB indisponible", false);
  }

  queries = await fetchJson("/api/queries");
  selectQuery(queries[0].id);
}

runButton.addEventListener("click", runSelectedQuery);
paramsFormEl.addEventListener("submit", (event) => {
  event.preventDefault();
  runSelectedQuery();
});
copyButton.addEventListener("click", async () => {
  await navigator.clipboard.writeText(resultsEl.textContent);
  copyButton.textContent = "Copie";
  window.setTimeout(() => {
    copyButton.textContent = "Copier JSON";
  }, 900);
});

init().catch((error) => {
  setStatus("Erreur", false);
  resultsEl.textContent = JSON.stringify({ error: error.message }, null, 2);
});
