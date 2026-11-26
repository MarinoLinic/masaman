const byId = id => document.getElementById(id);
const stage = byId("stage");
const canvas = byId("chart");
const context = canvas.getContext("2d");
const tooltip = byId("tooltip");
const status = byId("status");
const legend = byId("legend");
const entries = byId("entries");
const search = byId("search");
const toggle = byId("toggle-legend");
const keyDialog = byId("key-dialog");
const compact = matchMedia("(max-width: 820px)");
const zoomButtons = ["out", "in", "fit", "actual"].map(byId);
const reader = document.createElement("canvas");
reader.width = reader.height = 1;
const pixel = reader.getContext("2d", { willReadFrequently: true });
const image = new Image();
const palette = new Map();
const rows = new Map();
const pins = [];
const pointers = new Map();
const view = { width: 0, height: 0, scale: 1, fit: 1, x: 0, y: 0 };
let ready = false;
let frame = 0;
let active = null;
let hovered = null;
let moved = false;
let gestureStart = null;
let sampled;
let statusTimer;

const clamp = (value, min, max) => Math.max(min, Math.min(value, max));

function swatch(color) {
  const element = document.createElement("span");
  element.className = "swatch";
  element.style.setProperty("--swatch", color);
  element.setAttribute("aria-hidden", "true");
  return element;
}

function setLegend(open) {
  toggle.setAttribute("aria-expanded", open);
  legend.hidden = !open;
  if (open) revealActive();
}

function revealActive() {
  const row = rows.get(active);
  if (!row || legend.hidden || row.hidden || row.closest("section").hidden) return;
  const top = row.getBoundingClientRect().top - entries.getBoundingClientRect().top;
  if (top < 34 || top + row.offsetHeight > entries.clientHeight) {
    entries.scrollTop += top - 38;
  }
}

function markActive(entry, reveal = false) {
  rows.get(active)?.classList.remove("active");
  active = entry;
  rows.get(active)?.classList.add("active");
  if (reveal) revealActive();
}

function buildLegend(groups) {
  for (const group of groups) {
    const section = document.createElement("section");
    const heading = document.createElement("h3");
    heading.textContent = group.name;
    const list = document.createElement("ul");

    for (const entry of group.entries) {
      const row = document.createElement("li");
      row.append(swatch(entry.color), entry.label);
      rows.set(entry, row);
      for (const color of [entry.color, ...(entry.aliases ?? [])]) {
        const key = Number.parseInt(color.slice(1), 16);
        // An exact color shared by different legend entries is ambiguous.
        palette.set(key, palette.has(key) && palette.get(key) !== entry ? null : entry);
      }
      list.append(row);
    }

    section.append(heading, list);
    entries.append(section);
  }

  const empty = document.createElement("p");
  empty.textContent = "No matching legend entries.";
  empty.hidden = true;
  entries.append(empty);
  search.addEventListener("input", () => {
    const query = search.value.trim().toLowerCase();
    let count = 0;
    for (const section of entries.querySelectorAll("section")) {
      const groupMatches = section.querySelector("h3").textContent.toLowerCase().includes(query);
      let matches = 0;
      for (const row of section.querySelectorAll("li")) {
        row.hidden = !(groupMatches || row.textContent.toLowerCase().includes(query));
        if (!row.hidden) matches++;
      }
      section.hidden = !matches;
      count += matches;
    }
    empty.hidden = count > 0;
    entries.scrollTop = 0;
  });
}

function layout() {
  const { width, height, fit } = view;
  const center = sourcePoint(width / 2, height / 2);
  const fitted = Math.abs(view.scale - fit) < 1e-8;
  view.width = canvas.clientWidth;
  view.height = canvas.clientHeight;
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  canvas.width = Math.max(1, Math.round(view.width * dpr));
  canvas.height = Math.max(1, Math.round(view.height * dpr));

  if (!ready || !view.width || !view.height) return;
  const inset = Math.min(42, view.width * .06, view.height * .06);
  view.fit = Math.min(1, (view.width - inset) / image.naturalWidth, (view.height - inset) / image.naturalHeight);
  if (fitted || !width || !height) {
    fitChart();
  } else {
    view.scale = clamp(view.scale, view.fit, maxScale());
    view.x = view.width / 2 - center.x * view.scale;
    view.y = view.height / 2 - center.y * view.scale;
    update();
  }
}

function fitChart() {
  view.scale = view.fit;
  view.x = (view.width - image.naturalWidth * view.scale) / 2;
  view.y = (view.height - image.naturalHeight * view.scale) / 2;
  update();
}

function maxScale() {
  return Math.max(4, view.fit * 4);
}

function bound(offset, size, available) {
  if (view.scale === view.fit) return (available - size) / 2;
  // Allow a small margin so a wheel or pinch can stay anchored near an edge.
  const margin = Math.min(64, size * .16, available * .16);
  const space = available - size;
  return clamp(offset, Math.min(0, space) - margin, Math.max(0, space) + margin);
}

function update() {
  view.x = bound(view.x, image.naturalWidth * view.scale, view.width);
  view.y = bound(view.y, image.naturalHeight * view.scale, view.height);
  hideTooltip();
  if (!frame) frame = requestAnimationFrame(draw);
}

function draw() {
  frame = 0;
  const { x, y, scale, width, height } = view;
  context.setTransform(canvas.width / width, 0, 0, canvas.height / height, 0, 0);
  context.clearRect(0, 0, width, height);
  context.imageSmoothingEnabled = scale < 1;
  const left = Math.max(0, Math.floor(-x / scale));
  const top = Math.max(0, Math.floor(-y / scale));
  const right = Math.min(image.naturalWidth, Math.ceil((width - x) / scale));
  const bottom = Math.min(image.naturalHeight, Math.ceil((height - y) / scale));
  const sw = right - left;
  const sh = bottom - top;
  if (sw > 0 && sh > 0) {
    context.drawImage(image, left, top, sw, sh, x + left * scale, y + top * scale, sw * scale, sh * scale);
  }
  for (const pin of pins) placePin(pin);
  byId("scale").textContent = `${(scale / view.fit).toFixed(1).replace(/\.0$/, "")}×`;
  byId("out").disabled = scale <= view.fit;
  byId("in").disabled = scale >= maxScale();
}

function sourcePoint(x, y) {
  return { x: (x - view.x) / view.scale, y: (y - view.y) / view.scale };
}

function point(event) {
  const rect = canvas.getBoundingClientRect();
  return { x: event.clientX - rect.left, y: event.clientY - rect.top };
}

function zoomTo(scale, anchor, target = anchor) {
  if (!ready) return;
  const source = sourcePoint(anchor.x, anchor.y);
  view.scale = clamp(scale, view.fit, maxScale());
  view.x = target.x - source.x * view.scale;
  view.y = target.y - source.y * view.scale;
  update();
}

function zoomCenter(scale) {
  zoomTo(scale, { x: view.width / 2, y: view.height / 2 });
}

function lookup(source) {
  const x = Math.floor(source.x);
  const y = Math.floor(source.y);
  if (!ready || x < 0 || y < 0 || x >= image.naturalWidth || y >= image.naturalHeight) return null;
  if (sampled?.x === x && sampled.y === y) return sampled.entry;
  pixel.clearRect(0, 0, 1, 1);
  pixel.drawImage(image, x, y, 1, 1, 0, 0, 1, 1);
  const [r, g, b, alpha] = pixel.getImageData(0, 0, 1, 1).data;
  const entry = alpha === 255 ? palette.get((r << 16) | (g << 8) | b) ?? null : null;
  sampled = { x, y, entry };
  return entry;
}

function placeLabel(element, x, y) {
  const left = x + 13 + element.offsetWidth > view.width ? x - element.offsetWidth - 12 : x + 13;
  const top = y + 13 + element.offsetHeight > view.height ? y - element.offsetHeight - 12 : y + 13;
  element.style.left = `${clamp(left, 4, Math.max(4, view.width - element.offsetWidth - 4))}px`;
  element.style.top = `${clamp(top, 4, Math.max(4, view.height - element.offsetHeight - 4))}px`;
}

function hideTooltip() {
  hovered = null;
  tooltip.hidden = true;
  canvas.classList.remove("match");
}

function hover(at) {
  const entry = lookup(sourcePoint(at.x, at.y));
  if (!entry) {
    hideTooltip();
    return;
  }
  if (entry !== hovered) {
    tooltip.replaceChildren(swatch(entry.color), entry.label);
    tooltip.hidden = false;
    canvas.classList.add("match");
    hovered = entry;
  }
  placeLabel(tooltip, at.x, at.y);
}

function report(message) {
  clearTimeout(statusTimer);
  status.textContent = message;
  status.hidden = false;
  statusTimer = setTimeout(() => { status.hidden = true; }, 2200);
}

function pinAt(at) {
  const source = sourcePoint(at.x, at.y);
  const entry = lookup(source);
  if (!entry) {
    report("No matching legend color here.");
    return;
  }

  status.hidden = true;
  const existing = pins.find(pin => pin.entry === entry &&
    Math.hypot(pin.source.x - source.x, pin.source.y - source.y) * view.scale < 12);
  if (existing) {
    markActive(entry, true);
    return;
  }

  const label = document.createElement("div");
  label.className = "pin";
  const remove = document.createElement("button");
  remove.type = "button";
  remove.textContent = "×";
  remove.setAttribute("aria-label", `Remove pin for ${entry.label}`);
  label.append(swatch(entry.color), entry.label, remove);
  const dot = document.createElement("span");
  dot.className = "pin-dot";
  dot.setAttribute("aria-hidden", "true");

  const pin = { source, entry, label, dot };
  remove.addEventListener("click", () => {
    dropPin(pin);
    canvas.focus({ preventScroll: true });
  });
  byId("pins").append(dot, label);
  pins.push(pin);
  placePin(pin);
  hideTooltip();
  markActive(entry, true);
}

function placePin(pin) {
  const x = view.x + pin.source.x * view.scale;
  const y = view.y + pin.source.y * view.scale;
  pin.dot.hidden = pin.label.hidden = x < 0 || y < 0 || x > view.width || y > view.height;
  if (pin.label.hidden) return;
  pin.dot.style.left = `${x}px`;
  pin.dot.style.top = `${y}px`;
  placeLabel(pin.label, x, y);
}

function dropPin(pin) {
  pin.dot.remove();
  pin.label.remove();
  pins.splice(pins.indexOf(pin), 1);
  markActive(pins.at(-1)?.entry ?? null);
}

function pinch(points) {
  const [a, b] = points;
  return { center: { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }, distance: Math.hypot(a.x - b.x, a.y - b.y) };
}

canvas.addEventListener("pointerdown", event => {
  if (!ready || event.button !== 0 || pointers.size >= 2) return;
  const at = point(event);
  if (!pointers.size) {
    gestureStart = at;
    moved = false;
  } else {
    moved = true;
  }
  pointers.set(event.pointerId, at);
  canvas.setPointerCapture(event.pointerId);
  hideTooltip();
});

canvas.addEventListener("pointermove", event => {
  const at = point(event);
  if (!pointers.size) {
    if (event.pointerType !== "touch") hover(at);
    return;
  }
  if (!pointers.has(event.pointerId)) return;

  const previous = pointers.get(event.pointerId);
  const pair = pointers.size === 2 ? pinch(pointers.values()) : null;
  pointers.set(event.pointerId, at);
  if (pair) {
    const next = pinch(pointers.values());
    zoomTo(view.scale * next.distance / Math.max(1, pair.distance), pair.center, next.center);
  } else {
    if (!moved && Math.hypot(at.x - gestureStart.x, at.y - gestureStart.y) < 4) return;
    const from = moved ? previous : gestureStart;
    moved = true;
    view.x += at.x - from.x;
    view.y += at.y - from.y;
    update();
  }
  canvas.classList.add("dragging");
});

function finishPointer(event) {
  if (!pointers.delete(event.pointerId)) return;
  if (pointers.size) return;
  canvas.classList.remove("dragging");
  if (!moved && event.type === "pointerup") pinAt(point(event));
}

for (const event of ["pointerup", "pointercancel", "lostpointercapture"]) canvas.addEventListener(event, finishPointer);
canvas.addEventListener("pointerleave", hideTooltip);
canvas.addEventListener("wheel", event => {
  if (!ready || event.ctrlKey) return;
  event.preventDefault();
  const delta = event.deltaY * (event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? view.height : 1);
  zoomTo(view.scale * Math.exp(clamp(-delta * .0028, -.8, .8)), point(event));
}, { passive: false });

canvas.addEventListener("keydown", event => {
  if (!ready || event.ctrlKey || event.metaKey) return;
  switch (event.key) {
    case "+": case "=": zoomCenter(view.scale * 1.5); break;
    case "-": zoomCenter(view.scale / 1.5); break;
    case "Home": fitChart(); break;
    case "Enter": pinAt({ x: view.width / 2, y: view.height / 2 }); break;
    case "ArrowLeft": view.x += 85; update(); break;
    case "ArrowRight": view.x -= 85; update(); break;
    case "ArrowUp": view.y += 85; update(); break;
    case "ArrowDown": view.y -= 85; update(); break;
    default: return;
  }
  event.preventDefault();
});

document.addEventListener("keydown", event => {
  if (event.key === "Escape" && !keyDialog.open && event.target !== search) {
    while (pins.length) dropPin(pins.at(-1));
    hideTooltip();
  }
});
byId("out").addEventListener("click", () => zoomCenter(view.scale / 1.5));
byId("in").addEventListener("click", () => zoomCenter(view.scale * 1.5));
byId("fit").addEventListener("click", fitChart);
byId("actual").addEventListener("click", () => zoomCenter(1));
toggle.addEventListener("click", () => setLegend(legend.hidden));
compact.addEventListener("change", () => setLegend(!toggle.disabled && !compact.matches));
byId("show-key").addEventListener("click", () => keyDialog.showModal());
new ResizeObserver(layout).observe(stage);

async function initialize() {
  const inline = byId("chart-config").textContent.trim();
  let base = location.href;
  let config;
  if (inline) {
    config = JSON.parse(inline);
  } else {
    if (location.protocol === "file:") {
      throw new Error("Open the offline HTML export, or start the local preview from the README.");
    }
    const definition = new URL(new URLSearchParams(location.search).get("chart") || "charts/masaman.json", base);
    const response = await fetch(definition);
    if (!response.ok) throw new Error("The chart definition could not be loaded.");
    config = await response.json();
    base = definition.href;
  }

  document.title = byId("title").textContent = config.title;
  if (config.credit) {
    byId("credit").textContent = config.credit;
    byId("credit").hidden = false;
  }
  buildLegend(config.legend ?? []);
  if (config.key) {
    byId("key-image").src = new URL(config.key, base).href;
    byId("show-key").hidden = false;
  }
  if (config.original) {
    const original = byId("original");
    original.href = new URL(config.original, base).href;
    original.download = config.originalName || "original-chart.png";
    original.hidden = false;
  }

  image.src = new URL(config.image, base).href;
  await image.decode();
  // Confirm lookup is available before enabling any pointer or keyboard interactions.
  pixel.drawImage(image, 0, 0, 1, 1, 0, 0, 1, 1);
  pixel.getImageData(0, 0, 1, 1);
  ready = true;
  const hasLegend = rows.size > 0 || config.key || config.original;
  toggle.disabled = !hasLegend;
  setLegend(hasLegend && !compact.matches);
  zoomButtons.forEach(button => { button.disabled = false; });
  status.hidden = true;
  layout();
}

initialize().catch(error => {
  status.textContent = error.message;
  status.classList.add("error");
});
