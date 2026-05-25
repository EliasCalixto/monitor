const PALETTE = [
  "#8dbad6", "#9bc2e7", "#8ea9db", "#abb9d4",
  "#b9f5c4", "#fd9a9a", "#f8ccad", "#fef2cb",
  "#c4a7e7", "#a7c4e7", "#e7a7c4", "#a7e7c4",
];

const REPO_URL = "https://github.com/EliasCalixto/monitor";

const state = {
  data: null,
  currentDb: null,
  search: "",
  sortKey: null,
  sortDir: 1,
  chart1: null,
  chart2: null,
};

const $ = (sel) => document.querySelector(sel);

function setStatus(msg, isError = false) {
  const el = $("#status");
  if (!msg) {
    el.classList.remove("show");
    return;
  }
  el.textContent = msg;
  el.classList.toggle("error", isError);
  el.classList.add("show");
  if (!isError) setTimeout(() => el.classList.remove("show"), 3500);
}

async function loadData() {
  setStatus("Cargando data.json…");
  try {
    const res = await fetch(`./data.json?ts=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    state.data = data;
    onDataReady();
    setStatus("");
  } catch (e) {
    console.error(e);
    setStatus(
      "No se pudo cargar data.json. ¿Ya corrió el workflow 'Sync Notion data'? Ve a Actions y ejecútalo manualmente la primera vez.",
      true,
    );
  }
}

function onDataReady() {
  const { databases, generated_at } = state.data;
  if (generated_at) {
    const d = new Date(generated_at);
    $("#generated-at").textContent = `Actualizado ${d.toLocaleString()}`;
  }
  const dbSelect = $("#db-select");
  dbSelect.innerHTML = "";
  if (!databases || databases.length === 0) {
    setStatus("No se encontraron databases en la página Monitor.", true);
    return;
  }
  databases.forEach((db, i) => {
    const opt = document.createElement("option");
    opt.value = String(i);
    opt.textContent = db.title || "Untitled";
    dbSelect.appendChild(opt);
  });
  dbSelect.onchange = () => selectDb(Number(dbSelect.value));
  selectDb(0);
}

function selectDb(index) {
  state.currentDb = state.data.databases[index];
  state.sortKey = null;
  state.sortDir = 1;
  state.search = "";
  $("#search").value = "";
  renderAll();
}

function isNumericField(db, key) {
  const t = db.schema[key];
  return t === "number" || t === "formula" || t === "rollup" || t === "unique_id";
}

function isCategoricalField(db, key) {
  const t = db.schema[key];
  return t === "select" || t === "status" || t === "multi_select";
}

function isDateField(db, key) {
  const t = db.schema[key];
  return t === "date" || t === "created_time" || t === "last_edited_time";
}

function getValue(row, key) {
  const v = row[key];
  if (v && typeof v === "object" && !Array.isArray(v) && "start" in v) {
    return v.start;
  }
  return v;
}

function getNumeric(row, key) {
  const v = getValue(row, key);
  if (typeof v === "number") return v;
  if (typeof v === "string" && v.trim() !== "") {
    const n = Number(v);
    if (!Number.isNaN(n)) return n;
  }
  return null;
}

function getDate(row, key) {
  const v = getValue(row, key);
  if (!v) return null;
  const d = new Date(v);
  return Number.isNaN(d.getTime()) ? null : d;
}

function formatCell(value, type) {
  if (value === null || value === undefined || value === "") return "—";
  if (Array.isArray(value)) {
    if (value.length === 0) return "—";
    if (typeof value[0] === "object" && value[0] !== null && "url" in value[0]) {
      return value
        .map((f) => `<a href="${f.url}" target="_blank" rel="noreferrer">${escapeHtml(f.name || "file")}</a>`)
        .join(", ");
    }
    return value.map((v) => `<span class="tag">${escapeHtml(String(v))}</span>`).join("");
  }
  if (typeof value === "object") {
    if ("start" in value) {
      const s = value.start ? new Date(value.start).toLocaleDateString() : "";
      const e = value.end ? ` → ${new Date(value.end).toLocaleDateString()}` : "";
      return `${s}${e}`;
    }
    return escapeHtml(JSON.stringify(value));
  }
  if (typeof value === "boolean") {
    return value
      ? `<span class="checkbox-true">✓</span>`
      : `<span class="checkbox-false">·</span>`;
  }
  if (typeof value === "number") {
    return value.toLocaleString(undefined, { maximumFractionDigits: 2 });
  }
  if (type === "url" && typeof value === "string" && value.startsWith("http")) {
    return `<a href="${value}" target="_blank" rel="noreferrer">${escapeHtml(value)}</a>`;
  }
  if (type === "email" && typeof value === "string") {
    return `<a href="mailto:${value}">${escapeHtml(value)}</a>`;
  }
  if (typeof value === "string" && (type === "created_time" || type === "last_edited_time")) {
    return new Date(value).toLocaleString();
  }
  return escapeHtml(String(value));
}

function escapeHtml(s) {
  return s
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderAll() {
  renderKpis();
  renderChart1();
  renderChart2();
  renderTable();
}

function renderKpis() {
  const db = state.currentDb;
  const grid = $("#kpi-grid");
  grid.innerHTML = "";

  const rows = db.rows;
  const cards = [];
  cards.push(kpiCard("Filas", rows.length.toLocaleString(), db.title));

  const numericKeys = Object.keys(db.schema).filter((k) => isNumericField(db, k));
  for (const key of numericKeys.slice(0, 5)) {
    let sum = 0;
    let count = 0;
    for (const r of rows) {
      const n = getNumeric(r, key);
      if (n !== null) {
        sum += n;
        count += 1;
      }
    }
    const avg = count ? sum / count : 0;
    cards.push(
      kpiCard(
        `Σ ${key}`,
        sum.toLocaleString(undefined, { maximumFractionDigits: 2 }),
        `prom ${avg.toLocaleString(undefined, { maximumFractionDigits: 2 })} (${count})`,
      ),
    );
  }

  if (numericKeys.length === 0) {
    const catKeys = Object.keys(db.schema).filter((k) => isCategoricalField(db, k));
    for (const key of catKeys.slice(0, 3)) {
      const counts = new Map();
      for (const r of rows) {
        const v = r[key];
        const items = Array.isArray(v) ? v : v ? [v] : [];
        for (const it of items) counts.set(it, (counts.get(it) || 0) + 1);
      }
      const top = [...counts.entries()].sort((a, b) => b[1] - a[1])[0];
      cards.push(kpiCard(key, top ? top[0] : "—", top ? `${top[1]} filas` : ""));
    }
  }

  for (const c of cards) grid.appendChild(c);
}

function kpiCard(label, value, sub) {
  const el = document.createElement("div");
  el.className = "kpi";
  el.innerHTML = `
    <div class="kpi-label">${escapeHtml(label)}</div>
    <div class="kpi-value">${escapeHtml(String(value))}</div>
    ${sub ? `<div class="kpi-sub">${escapeHtml(sub)}</div>` : ""}
  `;
  return el;
}

function populateSelect(sel, options, defaultValue) {
  sel.innerHTML = "";
  for (const opt of options) {
    const o = document.createElement("option");
    o.value = opt;
    o.textContent = opt;
    sel.appendChild(o);
  }
  if (defaultValue && options.includes(defaultValue)) {
    sel.value = defaultValue;
  } else if (options.length > 0) {
    sel.value = options[0];
  }
}

function renderChart1() {
  const db = state.currentDb;
  const sel = $("#chart1-field");
  const candidates = Object.keys(db.schema).filter(
    (k) => isCategoricalField(db, k) || isNumericField(db, k),
  );
  if (candidates.length === 0) {
    if (state.chart1) state.chart1.destroy();
    $("#chart1-title").textContent = "Sin columnas para graficar";
    return;
  }
  const current = sel.value && candidates.includes(sel.value) ? sel.value : candidates[0];
  populateSelect(sel, candidates, current);
  sel.onchange = () => drawChart1(sel.value);
  drawChart1(current);
}

function drawChart1(key) {
  const db = state.currentDb;
  const counts = new Map();
  const numeric = isNumericField(db, key);

  if (numeric) {
    const numericKeys = Object.keys(db.schema).filter(
      (k) => isCategoricalField(db, k),
    );
    const groupBy = numericKeys[0];
    if (groupBy) {
      for (const r of db.rows) {
        const v = r[groupBy];
        const items = Array.isArray(v) ? v : v ? [v] : ["(sin valor)"];
        const num = getNumeric(r, key) || 0;
        for (const it of items) {
          counts.set(it, (counts.get(it) || 0) + num);
        }
      }
      $("#chart1-title").textContent = `Σ ${key} por ${groupBy}`;
    } else {
      const numericVals = db.rows.map((r) => getNumeric(r, key)).filter((v) => v !== null);
      const bins = 8;
      if (numericVals.length === 0) {
        $("#chart1-title").textContent = `${key} — sin datos`;
      } else {
        const min = Math.min(...numericVals);
        const max = Math.max(...numericVals);
        const step = (max - min) / bins || 1;
        for (let i = 0; i < bins; i++) {
          const lo = min + i * step;
          const hi = lo + step;
          const label = `${lo.toFixed(1)}–${hi.toFixed(1)}`;
          counts.set(label, numericVals.filter((v) => v >= lo && (i === bins - 1 ? v <= hi : v < hi)).length);
        }
        $("#chart1-title").textContent = `Distribución de ${key}`;
      }
    }
  } else {
    for (const r of db.rows) {
      const v = r[key];
      const items = Array.isArray(v) ? v : v != null && v !== "" ? [v] : ["(sin valor)"];
      for (const it of items) counts.set(it, (counts.get(it) || 0) + 1);
    }
    $("#chart1-title").textContent = `Distribución de ${key}`;
  }

  const entries = [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12);
  const labels = entries.map((e) => String(e[0]));
  const values = entries.map((e) => e[1]);
  const colors = labels.map((_, i) => PALETTE[i % PALETTE.length]);

  if (state.chart1) state.chart1.destroy();
  const ctx = document.getElementById("chart1");
  state.chart1 = new Chart(ctx, {
    type: labels.length > 6 ? "bar" : "doughnut",
    data: { labels, datasets: [{ data: values, backgroundColor: colors, borderWidth: 0 }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: labels.length > 6 ? "none" : "right", labels: { font: { size: 11 } } },
      },
      scales: labels.length > 6 ? { y: { beginAtZero: true } } : {},
    },
  });
}

function renderChart2() {
  const db = state.currentDb;
  const selDate = $("#chart2-date");
  const selValue = $("#chart2-value");
  const dateKeys = Object.keys(db.schema).filter((k) => isDateField(db, k));
  const numKeys = Object.keys(db.schema).filter((k) => isNumericField(db, k));

  if (dateKeys.length === 0 || numKeys.length === 0) {
    if (state.chart2) state.chart2.destroy();
    $("#chart2-title").textContent = "Necesita columna de fecha + número";
    selDate.innerHTML = "";
    selValue.innerHTML = "";
    return;
  }
  populateSelect(selDate, dateKeys, selDate.value);
  populateSelect(selValue, numKeys, selValue.value);
  selDate.onchange = () => drawChart2(selDate.value, selValue.value);
  selValue.onchange = () => drawChart2(selDate.value, selValue.value);
  drawChart2(selDate.value, selValue.value);
}

function drawChart2(dateKey, valueKey) {
  const db = state.currentDb;
  const points = [];
  for (const r of db.rows) {
    const d = getDate(r, dateKey);
    const v = getNumeric(r, valueKey);
    if (d && v !== null) points.push({ x: d, y: v });
  }
  points.sort((a, b) => a.x - b.x);

  $("#chart2-title").textContent = `${valueKey} vs ${dateKey}`;
  if (state.chart2) state.chart2.destroy();
  const ctx = document.getElementById("chart2");
  state.chart2 = new Chart(ctx, {
    type: "line",
    data: {
      labels: points.map((p) => p.x.toLocaleDateString()),
      datasets: [
        {
          label: valueKey,
          data: points.map((p) => p.y),
          borderColor: "#0071e3",
          backgroundColor: "rgba(0,113,227,0.12)",
          fill: true,
          tension: 0.3,
          pointRadius: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: false } },
    },
  });
}

function renderTable() {
  const db = state.currentDb;
  const thead = $("#data-table thead");
  const tbody = $("#data-table tbody");
  const keys = Object.keys(db.schema);
  const q = state.search.toLowerCase();

  let rows = db.rows;
  if (q) {
    rows = rows.filter((r) =>
      keys.some((k) => {
        const v = r[k];
        if (v == null) return false;
        return JSON.stringify(v).toLowerCase().includes(q);
      }),
    );
  }
  if (state.sortKey) {
    const k = state.sortKey;
    const dir = state.sortDir;
    rows = [...rows].sort((a, b) => {
      const va = getValue(a, k);
      const vb = getValue(b, k);
      if (va == null && vb == null) return 0;
      if (va == null) return 1;
      if (vb == null) return -1;
      if (typeof va === "number" && typeof vb === "number") return (va - vb) * dir;
      return String(va).localeCompare(String(vb)) * dir;
    });
  }

  thead.innerHTML =
    "<tr>" +
    keys
      .map((k) => {
        let cls = "";
        if (state.sortKey === k) cls = state.sortDir === 1 ? "sorted-asc" : "sorted-desc";
        return `<th data-key="${escapeHtml(k)}" class="${cls}">${escapeHtml(k)}</th>`;
      })
      .join("") +
    "</tr>";

  tbody.innerHTML = rows
    .map(
      (r) =>
        "<tr>" +
        keys
          .map((k) => {
            const numeric = isNumericField(db, k);
            return `<td class="${numeric ? "num" : ""}">${formatCell(r[k], db.schema[k])}</td>`;
          })
          .join("") +
        "</tr>",
    )
    .join("");

  $("#row-count").textContent = `${rows.length} de ${db.rows.length} filas`;

  thead.querySelectorAll("th").forEach((th) => {
    th.onclick = () => {
      const k = th.dataset.key;
      if (state.sortKey === k) state.sortDir = -state.sortDir;
      else {
        state.sortKey = k;
        state.sortDir = 1;
      }
      renderTable();
    };
  });
}

document.addEventListener("DOMContentLoaded", () => {
  $("#repo-link").href = REPO_URL;
  $("#refresh").onclick = loadData;
  $("#search").addEventListener("input", (e) => {
    state.search = e.target.value;
    renderTable();
  });
  const tryLoad = () => {
    if (typeof Chart === "undefined") {
      setTimeout(tryLoad, 50);
      return;
    }
    loadData();
  };
  tryLoad();
});
