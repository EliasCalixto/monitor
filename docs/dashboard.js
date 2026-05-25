const RESUMEN_COLUMNS = [
  "Cash",
  "Total Papa",
  "Cash Total",
  "Tot. Savings",
  "Tot. Income",
  "Tot. Expenses",
];

const CATEGORY_COLORS = {
  Savings: "#8dbad6",
  Setup: "#9bc2e7",
  Home: "#8ea9db",
  Studies: "#abb9d4",
  Enjoy: "#b9f5c4",
  Losses: "#fd9a9a",
  Fixed: "#f8ccad",
  Cashout: "#fef2cb",
};

const CATEGORY_ORDER = [
  "Savings",
  "Setup",
  "Home",
  "Studies",
  "Enjoy",
  "Losses",
  "Fixed",
  "Cashout",
];

const FALLBACK_PALETTE = [
  "#8dbad6", "#9bc2e7", "#8ea9db", "#abb9d4",
  "#b9f5c4", "#fd9a9a", "#f8ccad", "#fef2cb",
];

const state = {
  data: null,
  expenses: [],
  incomes: [],
  fixedExpenses: [],
  selectedCategories: new Set(CATEGORY_ORDER),
  period: "all",
  dateFrom: null,
  dateTo: null,
  sort: { exp: { key: null, dir: -1 }, inc: { key: null, dir: -1 }, fix: { key: null, dir: -1 } },
  charts: {},
};

const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

function setStatus(msg, isError = false) {
  const el = $("#status");
  if (!msg) {
    el.classList.remove("show");
    return;
  }
  el.textContent = msg;
  el.classList.toggle("error", isError);
  el.classList.add("show");
  if (!isError) setTimeout(() => el.classList.remove("show"), 3000);
}

function fmtMoney(n) {
  if (n == null || Number.isNaN(n)) return "—";
  return n.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fmtDate(d) {
  if (!d) return "—";
  const dt = d instanceof Date ? d : new Date(d);
  if (Number.isNaN(dt.getTime())) return String(d);
  return dt.toLocaleDateString();
}

function getRowDate(row, key) {
  const v = row[key];
  if (!v) return null;
  const start = typeof v === "object" ? v.start : v;
  if (!start) return null;
  const d = new Date(start);
  return Number.isNaN(d.getTime()) ? null : d;
}

function findDb(title) {
  return (state.data?.databases || []).find(
    (d) => (d.title || "").toLowerCase() === title.toLowerCase(),
  );
}

async function loadData() {
  setStatus("Cargando data.json…");
  try {
    const res = await fetch(`./data.json?ts=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    state.data = await res.json();
    onDataReady();
    setStatus("");
  } catch (e) {
    console.error(e);
    setStatus(
      "No se pudo cargar data.json. ¿Ya corrió el workflow 'Sync Notion data'?",
      true,
    );
  }
}

function onDataReady() {
  const { generated_at, databases } = state.data;
  if (generated_at) {
    $("#generated-at").textContent = `Actualizado ${new Date(generated_at).toLocaleString()}`;
  }

  const expDb = findDb("Expenses");
  const incDb = findDb("Incomes");
  const fixDb = findDb("Fixed Expenses");

  if (!expDb || !incDb || !fixDb) {
    const missing = [
      !expDb && "Expenses",
      !incDb && "Incomes",
      !fixDb && "Fixed Expenses",
    ].filter(Boolean).join(", ");
    setStatus(`Faltan databases: ${missing}`, true);
  }

  state.expenses = (expDb?.rows || []).map((r) => ({
    id: r._id,
    url: r._url,
    name: r.Name || "",
    category: r.Category || "—",
    date: getRowDate(r, "Date Created"),
    price: typeof r.Price === "number" ? r.Price : 0,
  }));

  state.incomes = (incDb?.rows || []).map((r) => ({
    id: r._id,
    url: r._url,
    name: r.Name || "",
    date: getRowDate(r, "Date Received"),
    income: typeof r.Income === "number" ? r.Income : 0,
  }));

  state.fixedExpenses = (fixDb?.rows || []).map((r) => ({
    id: r._id,
    url: r._url,
    name: r.Name || "",
    type: r.Type || "—",
    price: typeof r.Price === "number" ? r.Price : 0,
  }));

  buildCategoryChips();
  renderResumen();
  applyAndRender();
}

function renderResumen() {
  const grid = $("#resumen-grid");
  const titleEl = $("#resumen-title");
  grid.innerHTML = "";

  const db = findDb("New database") || findDb("Resumen");
  if (!db || !db.rows || db.rows.length === 0) {
    titleEl.textContent = "Resumen";
    return;
  }

  const row = db.rows[0];
  titleEl.textContent = row.Name || "Resumen";

  for (const col of RESUMEN_COLUMNS) {
    const value = row[col];
    if (typeof value !== "number" || Number.isNaN(value)) continue;
    grid.appendChild(resumenCard(col, value));
  }
}

function resumenCard(label, value) {
  const el = document.createElement("div");
  let klass = "kpi";
  let valClass = "";
  if (label === "Cash" || label === "Cash Total") {
    if (value < 0) {
      klass += " expense";
      valClass = "negative";
    } else {
      klass += " income";
      valClass = "positive";
    }
  } else if (label === "Tot. Income") {
    klass += " income";
  } else if (label === "Tot. Expenses") {
    klass += " expense";
  } else if (label === "Tot. Savings") {
    klass += " net";
  } else {
    klass += " fixed";
  }
  el.className = klass;
  el.innerHTML = `
    <div class="kpi-label">${escapeHtml(label)}</div>
    <div class="kpi-value ${valClass}">${fmtMoney(value)}</div>
  `;
  return el;
}

function buildCategoryChips() {
  const present = new Set(state.expenses.map((e) => e.category).filter(Boolean));
  const ordered = [
    ...CATEGORY_ORDER.filter((c) => present.has(c)),
    ...[...present].filter((c) => !CATEGORY_ORDER.includes(c)),
  ];
  state.selectedCategories = new Set(ordered);

  const wrap = $("#category-chips");
  wrap.innerHTML = "";
  for (const cat of ordered) {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "chip";
    chip.dataset.cat = cat;
    chip.textContent = cat;
    chip.style.background = CATEGORY_COLORS[cat] || "#cccccc";
    chip.addEventListener("click", () => {
      if (state.selectedCategories.has(cat)) {
        state.selectedCategories.delete(cat);
        chip.classList.add("off");
      } else {
        state.selectedCategories.add(cat);
        chip.classList.remove("off");
      }
      applyAndRender();
    });
    wrap.appendChild(chip);
  }
}

function computePeriod() {
  const now = new Date();
  const start = new Date(now.getFullYear(), now.getMonth(), 1);
  switch (state.period) {
    case "this-month":
      return { from: start, to: null };
    case "last-month": {
      const from = new Date(now.getFullYear(), now.getMonth() - 1, 1);
      const to = new Date(now.getFullYear(), now.getMonth(), 0, 23, 59, 59);
      return { from, to };
    }
    case "3m":
      return { from: new Date(now.getFullYear(), now.getMonth() - 2, 1), to: null };
    case "6m":
      return { from: new Date(now.getFullYear(), now.getMonth() - 5, 1), to: null };
    case "year":
      return { from: new Date(now.getFullYear(), 0, 1), to: null };
    case "custom":
      return {
        from: state.dateFrom ? new Date(state.dateFrom) : null,
        to: state.dateTo ? new Date(`${state.dateTo}T23:59:59`) : null,
      };
    case "all":
    default:
      return { from: null, to: null };
  }
}

function inPeriod(date, from, to) {
  if (!date) return false;
  if (from && date < from) return false;
  if (to && date > to) return false;
  return true;
}

function applyAndRender() {
  const { from, to } = computePeriod();
  const filteredExpenses = state.expenses.filter(
    (e) => inPeriod(e.date, from, to) && state.selectedCategories.has(e.category),
  );
  const filteredIncomes = state.incomes.filter((i) => inPeriod(i.date, from, to));

  renderExpenseByCategory(filteredExpenses);
  renderExpenseOverTime(filteredExpenses);
  renderExpenseTable(filteredExpenses);

  renderIncomeOverTime(filteredIncomes);
  renderIncomeTable(filteredIncomes);

  renderFixedExpenses();
}

function destroyChart(key) {
  if (state.charts[key]) {
    state.charts[key].destroy();
    state.charts[key] = null;
  }
}

function renderExpenseByCategory(expenses) {
  destroyChart("expByCat");
  const totals = new Map();
  for (const e of expenses) totals.set(e.category, (totals.get(e.category) || 0) + e.price);
  const present = [...totals.keys()].sort((a, b) => {
    const ia = CATEGORY_ORDER.indexOf(a);
    const ib = CATEGORY_ORDER.indexOf(b);
    if (ia === -1 && ib === -1) return a.localeCompare(b);
    if (ia === -1) return 1;
    if (ib === -1) return -1;
    return ia - ib;
  });
  const labels = present;
  const values = labels.map((l) => totals.get(l));
  const colors = labels.map((l, i) => CATEGORY_COLORS[l] || FALLBACK_PALETTE[i % FALLBACK_PALETTE.length]);

  const ctx = document.getElementById("exp-by-category");
  state.charts.expByCat = new Chart(ctx, {
    type: "doughnut",
    data: { labels, datasets: [{ data: values, backgroundColor: colors, borderWidth: 0 }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "62%",
      plugins: {
        legend: { position: "right", labels: { font: { size: 12 }, boxWidth: 14, padding: 10 } },
        tooltip: {
          callbacks: {
            label: (c) => `${c.label}: ${fmtMoney(c.parsed)} (${((c.parsed / values.reduce((a, b) => a + b, 0)) * 100).toFixed(1)}%)`,
          },
        },
      },
    },
  });
}

function monthKey(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
}

function renderExpenseOverTime(expenses) {
  destroyChart("expOverTime");
  const byMonth = new Map();
  for (const e of expenses) {
    if (!e.date) continue;
    const k = monthKey(e.date);
    if (!byMonth.has(k)) byMonth.set(k, {});
    byMonth.get(k)[e.category] = (byMonth.get(k)[e.category] || 0) + e.price;
  }
  const months = [...byMonth.keys()].sort();
  const cats = [...new Set(expenses.map((e) => e.category))].sort((a, b) => {
    const ia = CATEGORY_ORDER.indexOf(a);
    const ib = CATEGORY_ORDER.indexOf(b);
    return (ia === -1 ? 999 : ia) - (ib === -1 ? 999 : ib);
  });

  const datasets = cats.map((cat, i) => ({
    label: cat,
    data: months.map((m) => byMonth.get(m)[cat] || 0),
    backgroundColor: CATEGORY_COLORS[cat] || FALLBACK_PALETTE[i % FALLBACK_PALETTE.length],
    borderColor: CATEGORY_COLORS[cat] || FALLBACK_PALETTE[i % FALLBACK_PALETTE.length],
    borderWidth: 0,
  }));

  const ctx = document.getElementById("exp-over-time");
  state.charts.expOverTime = new Chart(ctx, {
    type: "bar",
    data: { labels: months, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } },
        tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${fmtMoney(c.parsed.y)}` } },
      },
      scales: {
        x: { stacked: true, grid: { display: false } },
        y: { stacked: true, ticks: { callback: (v) => fmtMoney(v) } },
      },
    },
  });
}

function sortRows(rows, key, dir, getters) {
  if (!key) return rows;
  const get = getters[key];
  return [...rows].sort((a, b) => {
    const va = get(a);
    const vb = get(b);
    if (va == null && vb == null) return 0;
    if (va == null) return 1;
    if (vb == null) return -1;
    if (va instanceof Date && vb instanceof Date) return (va - vb) * dir;
    if (typeof va === "number" && typeof vb === "number") return (va - vb) * dir;
    return String(va).localeCompare(String(vb)) * dir;
  });
}

function buildSortableTable(tableSel, sortKey, columns, rows, getters, opts = {}) {
  const sortState = state.sort[sortKey];
  const sorted = sortRows(rows, sortState.key, sortState.dir, getters);

  const thead = $(`${tableSel} thead`);
  const tbody = $(`${tableSel} tbody`);

  thead.innerHTML =
    "<tr>" +
    columns
      .map((col) => {
        let cls = "";
        if (sortState.key === col.key) cls = sortState.dir === 1 ? "sorted-asc" : "sorted-desc";
        if (col.num) cls += " num";
        return `<th data-key="${col.key}" class="${cls.trim()}">${col.label}</th>`;
      })
      .join("") +
    "</tr>";

  tbody.innerHTML = sorted
    .map(
      (r) =>
        "<tr>" +
        columns.map((col) => `<td class="${col.num ? "num" : ""}">${col.render(r)}</td>`).join("") +
        "</tr>",
    )
    .join("");

  thead.querySelectorAll("th").forEach((th) => {
    th.onclick = () => {
      const k = th.dataset.key;
      if (sortState.key === k) sortState.dir = -sortState.dir;
      else {
        sortState.key = k;
        sortState.dir = 1;
      }
      applyAndRender();
    };
  });

  if (opts.countEl) {
    $(opts.countEl).textContent = `${sorted.length} ${opts.countLabel || "filas"}`;
  }
}

function renderExpenseTable(expenses) {
  const getters = {
    date: (r) => r.date,
    name: (r) => r.name,
    category: (r) => r.category,
    price: (r) => r.price,
  };
  const columns = [
    { key: "date", label: "Fecha", num: false, render: (r) => fmtDate(r.date) },
    {
      key: "category",
      label: "Categoría",
      num: false,
      render: (r) => {
        const color = CATEGORY_COLORS[r.category] || "#dddddd";
        return `<span class="category-tag" style="background:${color}">${escapeHtml(r.category)}</span>`;
      },
    },
    {
      key: "name",
      label: "Nombre",
      num: false,
      render: (r) =>
        r.url
          ? `<a href="${r.url}" target="_blank" rel="noreferrer">${escapeHtml(r.name)}</a>`
          : escapeHtml(r.name),
    },
    { key: "price", label: "Precio", num: true, render: (r) => fmtMoney(r.price) },
  ];
  buildSortableTable("#exp-table", "exp", columns, expenses, getters, {
    countEl: "#exp-count",
    countLabel: "gastos",
  });
}

function renderIncomeOverTime(incomes) {
  destroyChart("incOverTime");
  const byMonth = new Map();
  for (const i of incomes) {
    if (!i.date) continue;
    const k = monthKey(i.date);
    byMonth.set(k, (byMonth.get(k) || 0) + i.income);
  }
  const months = [...byMonth.keys()].sort();
  const values = months.map((m) => byMonth.get(m));

  const ctx = document.getElementById("inc-over-time");
  state.charts.incOverTime = new Chart(ctx, {
    type: "bar",
    data: {
      labels: months,
      datasets: [
        {
          label: "Ingresos",
          data: values,
          backgroundColor: "#b9f5c4",
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (c) => fmtMoney(c.parsed.y) } },
      },
      scales: {
        x: { grid: { display: false } },
        y: { ticks: { callback: (v) => fmtMoney(v) } },
      },
    },
  });
}

function renderIncomeTable(incomes) {
  const getters = {
    date: (r) => r.date,
    name: (r) => r.name,
    income: (r) => r.income,
  };
  const columns = [
    { key: "date", label: "Fecha", num: false, render: (r) => fmtDate(r.date) },
    {
      key: "name",
      label: "Nombre",
      num: false,
      render: (r) =>
        r.url
          ? `<a href="${r.url}" target="_blank" rel="noreferrer">${escapeHtml(r.name)}</a>`
          : escapeHtml(r.name),
    },
    { key: "income", label: "Ingreso", num: true, render: (r) => fmtMoney(r.income) },
  ];
  buildSortableTable("#inc-table", "inc", columns, incomes, getters, {
    countEl: "#inc-count",
    countLabel: "ingresos",
  });
}

function renderFixedExpenses() {
  destroyChart("fixByType");
  const totals = new Map();
  for (const f of state.fixedExpenses) totals.set(f.type, (totals.get(f.type) || 0) + f.price);
  const labels = [...totals.keys()];
  const values = labels.map((l) => totals.get(l));
  const colors = labels.map((_, i) => FALLBACK_PALETTE[i % FALLBACK_PALETTE.length]);

  const ctx = document.getElementById("fixed-by-type");
  state.charts.fixByType = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{ label: "Total", data: values, backgroundColor: colors, borderRadius: 4 }],
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (c) => fmtMoney(c.parsed.x) } },
      },
      scales: {
        x: { ticks: { callback: (v) => fmtMoney(v) } },
        y: { grid: { display: false } },
      },
    },
  });

  const total = state.fixedExpenses.reduce((s, f) => s + f.price, 0);
  $("#fixed-total").textContent = `Total mensual: ${fmtMoney(total)}`;

  const getters = {
    name: (r) => r.name,
    type: (r) => r.type,
    price: (r) => r.price,
  };
  const columns = [
    { key: "type", label: "Tipo", num: false, render: (r) => escapeHtml(r.type) },
    {
      key: "name",
      label: "Nombre",
      num: false,
      render: (r) =>
        r.url
          ? `<a href="${r.url}" target="_blank" rel="noreferrer">${escapeHtml(r.name)}</a>`
          : escapeHtml(r.name),
    },
    { key: "price", label: "Precio", num: true, render: (r) => fmtMoney(r.price) },
  ];
  buildSortableTable("#fixed-table", "fix", columns, state.fixedExpenses, getters);
}

function escapeHtml(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function attachFilterListeners() {
  $("#period").addEventListener("change", (e) => {
    state.period = e.target.value;
    const showCustom = state.period === "custom";
    $("#date-from-group").hidden = !showCustom;
    $("#date-to-group").hidden = !showCustom;
    applyAndRender();
  });
  $("#date-from").addEventListener("change", (e) => {
    state.dateFrom = e.target.value || null;
    applyAndRender();
  });
  $("#date-to").addEventListener("change", (e) => {
    state.dateTo = e.target.value || null;
    applyAndRender();
  });
  $("#reset-filters").addEventListener("click", () => {
    state.period = "all";
    state.dateFrom = null;
    state.dateTo = null;
    $("#period").value = "all";
    $("#date-from").value = "";
    $("#date-to").value = "";
    $("#date-from-group").hidden = true;
    $("#date-to-group").hidden = true;
    state.selectedCategories = new Set(CATEGORY_ORDER);
    $$("#category-chips .chip").forEach((c) => c.classList.remove("off"));
    state.selectedCategories = new Set(
      [...$$("#category-chips .chip")].map((c) => c.dataset.cat),
    );
    applyAndRender();
  });
  $("#refresh").addEventListener("click", loadData);
}

function bootstrap() {
  attachFilterListeners();
  const tryLoad = () => {
    if (typeof Chart === "undefined") {
      setTimeout(tryLoad, 50);
      return;
    }
    loadData();
  };
  tryLoad();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", bootstrap, { once: true });
} else {
  bootstrap();
}
