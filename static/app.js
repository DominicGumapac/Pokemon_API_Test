// Same origin as the Flask app, so relative URLs work with no CORS setup.
// If you host this page elsewhere, set e.g. "http://127.0.0.1:5000" (and enable flask-cors on the API).
const API = "";
const STATS = ["hp", "attack", "defense", "speed"];
const STAT_MAX = 160;
const TYPE_COLORS = {
  grass:"#4a9d4a", poison:"#9a5bb5", fire:"#e2662b", water:"#3f7fd6", electric:"#c9a012",
  normal:"#8a8a78", fairy:"#d06a9a", fighting:"#b23a32", rock:"#9c8a3d", ground:"#a8874a",
  ghost:"#6a5a9a", dragon:"#5a49d0", psychic:"#d4497a", ice:"#4fa9b8", bug:"#8a9a1f",
  flying:"#7a8fd6", steel:"#6f8590", dark:"#5a4a42"
};
let all = [];
let editingId = null;
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

async function api(path, opts = {}) {
  const res = await fetch(API + path, { headers: { "Content-Type": "application/json" }, ...opts });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.error || res.statusText);
  return body;
}

function toast(msg) {
  const t = $("#toast");
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => t.classList.remove("show"), 2600);
}

async function load() {
  try {
    all = await api("/pokemon");
    render();
  } catch (e) {
    $("#list").innerHTML = '<p class="status">Can\'t reach the API. Make sure <code>python app.py</code> is running, then reload.</p>';
  }
}

function render() {
  const q = $("#search").value.trim().toLowerCase();
  const key = $("#sort").value;
  const rows = all
    .filter(p => !q || p.name.toLowerCase().includes(q) || p.type.toLowerCase().includes(q))
    .sort((a, b) => key === "name" ? a.name.localeCompare(b.name) : key === "id" ? a.id - b.id : b[key] - a[key]);
  if (!rows.length) {
    $("#list").innerHTML = '<p class="empty">' + (all.length ? "No Pokémon match your search." : "No Pokémon yet. Add your first one.") + "</p>";
    return;
  }
  $("#list").innerHTML = rows.map(p => `
    <article class="card">
      <div class="top"><h2 class="name">${esc(p.name)}</h2><span class="id">#${p.id}</span></div>
      <div class="types">${p.type.split("/").map(t => {
        const c = TYPE_COLORS[t.trim().toLowerCase()] || "#6b7773";
        return `<span class="chip" style="background:${c}">${esc(t.trim())}</span>`;
      }).join("")}</div>
      <div>${STATS.map(s => `
        <div class="stat"><span>${s[0].toUpperCase() + s.slice(1)}</span>
        <div class="bar"><i style="width:${Math.min(100, p[s] / STAT_MAX * 100)}%"></i></div>
        <span>${p[s]}</span></div>`).join("")}</div>
      <div class="actions">
        <button data-edit="${p.id}">Edit</button>
        <button class="danger" data-del="${p.id}">Delete</button>
      </div>
    </article>`).join("");
}

function openForm(p) {
  editingId = p ? p.id : null;
  $("#dlgTitle").textContent = p ? "Edit " + p.name : "Add Pokémon";
  $("#formError").textContent = "";
  const f = $("#form");
  ["name", "type", ...STATS].forEach(k => f.elements[k].value = p ? p[k] : "");
  $("#dlg").showModal();
  f.elements.name.focus();
}

$("#addBtn").onclick = () => openForm(null);
$("#cancel").onclick = () => $("#dlg").close();
$("#search").oninput = render;
$("#sort").onchange = render;

$("#list").onclick = async e => {
  const edit = e.target.closest("[data-edit]");
  const del = e.target.closest("[data-del]");
  if (edit) openForm(all.find(p => p.id === +edit.dataset.edit));
  if (del) {
    const p = all.find(x => x.id === +del.dataset.del);
    if (!confirm(`Delete ${p.name}? This can't be undone.`)) return;
    try {
      await api("/pokemon/" + p.id, { method: "DELETE" });
      toast(`Deleted ${p.name}`);
      load();
    } catch (err) { toast(err.message); }
  }
};

$("#form").onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const data = { name: f.elements.name.value.trim(), type: f.elements.type.value.trim() };
  STATS.forEach(s => data[s] = Number(f.elements[s].value));
  try {
    await api(editingId ? "/pokemon/" + editingId : "/pokemon", {
      method: editingId ? "PUT" : "POST",
      body: JSON.stringify(data)
    });
    $("#dlg").close();
    toast(editingId ? `Saved ${data.name}` : `Added ${data.name}`);
    load();
  } catch (err) {
    $("#formError").textContent = err.message;
  }
};

load();
