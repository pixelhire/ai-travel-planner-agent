// ================================
// DOM
// ================================

const sendBtn = document.getElementById("sendBtn");
const queryInput = document.getElementById("query");
const tripList = document.getElementById("tripList");
const newTripBtn = document.getElementById("newTripBtn");
const chatContainer = document.getElementById("chatContainer");

// ================================
// STATE
// ================================

let trips = [];
let currentTrip = null;

// ================================
// INIT
// ================================

document.addEventListener("DOMContentLoaded", () => {
  loadTrips();
});

// ================================
// LOAD TRIPS
// ================================

async function loadTrips() {
  try {
    const res = await fetch("/trips");
    trips = await res.json();

    renderTrips();

    if (trips.length > 0) {
      openTrip(trips[0].id);
    }
  } catch (err) {
    console.error("Failed loading trips", err);
  }
}

// ================================
// CREATE TRIP
// ================================

async function createTrip() {
  try {
    const res = await fetch("/trips", { method: "POST" });
    const trip = await res.json();

    trips.unshift(trip);
    renderTrips();

    openTrip(trip.id);
  } catch (err) {
    console.error("Create trip failed", err);
  }
}

newTripBtn.addEventListener("click", createTrip);

// ================================
// OPEN TRIP
// ================================

async function openTrip(id) {
  currentTrip = id;

  chatContainer.innerHTML = "";

  try {
    const res = await fetch(`/trips/${id}`);
    const trip = await res.json();

    if (trip.plans && trip.plans.length > 0) {
      trip.plans.forEach((p) => {
        if (p.plan.input) {
          addUserMessage(p.plan.input);
        }

        if (p.plan.output) {
          addBotMessage(p.plan.output);
        }
      });
    }
  } catch (err) {
    console.error("Load trip failed", err);
  }

  renderTrips();
}

// ================================
// RENDER SIDEBAR
// ================================

function renderTrips() {
  tripList.innerHTML = "";

  trips.forEach((trip) => {
    const li = document.createElement("li");
    li.classList.add("trip-item");

    if (trip.id === currentTrip) {
      li.classList.add("active");
    }

    const title = document.createElement("span");
    title.classList.add("trip-title");
    title.textContent = trip.title || "Trip";

    title.onclick = () => openTrip(trip.id);

    const actions = document.createElement("div");
    actions.classList.add("trip-actions");

    const renameBtn = document.createElement("button");
    renameBtn.classList.add("icon-btn");
    renameBtn.innerHTML = "✏️";

    renameBtn.onclick = (e) => {
      e.stopPropagation();
      renameTrip(trip.id);
    };

    const deleteBtn = document.createElement("button");
    deleteBtn.classList.add("icon-btn");
    deleteBtn.innerHTML = "🗑";

    deleteBtn.onclick = (e) => {
      e.stopPropagation();
      deleteTrip(trip.id);
    };

    actions.appendChild(renameBtn);
    actions.appendChild(deleteBtn);

    li.appendChild(title);
    li.appendChild(actions);

    tripList.appendChild(li);
  });
}

async function deleteTrip(id) {
  const confirmDelete = confirm("Delete this trip?");
  if (!confirmDelete) return;

  try {
    await fetch(`/trips/${id}`, { method: "DELETE" });

    await loadTrips(); // reload fresh list
  } catch (err) {
    console.error("Delete failed", err);
  }
}

async function renameTrip(id) {
  const newName = prompt("Enter new trip name");

  if (!newName) return;

  try {
    await fetch(`/trips/${id}/rename`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: newName,
      }),
    });

    const trip = trips.find((t) => t.id === id);

    if (trip) {
      trip.title = newName;
    }

    renderTrips();
  } catch (err) {
    console.error("Rename failed", err);
  }
}

// ================================
// SEND QUERY
// ================================

sendBtn.addEventListener("click", generatePlan);

queryInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    generatePlan();
  }
});

async function generatePlan() {
  const query = queryInput.value.trim();
  if (!query) return;

  queryInput.value = "";

  addUserMessage(query);
  showLoading();

  try {
    const res = await fetch("/plan-trip", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        trip_id: currentTrip,
        query: query,
      }),
    });

    const data = await res.json();

    removeLoading();

    const raw = JSON.stringify(data.result, null, 2);

    addBotMessage(raw);

    await saveTripPlan(data.result);
  } catch (err) {
    removeLoading();
    addBotMessage("Error generating trip.");
  }
}

// ================================
// SAVE PLAN
// ================================

async function saveTripPlan(plan) {
  try {
    await fetch(`/trips/${currentTrip}/plan`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        trip_id: currentTrip,
        plan: plan,
      }),
    });
  } catch (err) {
    console.error("Save failed", err);
  }
}

// ================================
// CHAT UI
// ================================

function addUserMessage(text) {
  const div = document.createElement("div");
  div.className = "message user";
  div.textContent = text;

  chatContainer.appendChild(div);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addBotMessage(text) {
  const div = document.createElement("div");
  div.className = "message bot";

  const pre = document.createElement("pre");
  pre.textContent = text;

  div.appendChild(pre);

  chatContainer.appendChild(div);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showLoading() {
  const div = document.createElement("div");
  div.className = "message bot";
  div.id = "loading";

  div.textContent = "✈️ Planning trip...";

  chatContainer.appendChild(div);
}

function removeLoading() {
  const el = document.getElementById("loading");
  if (el) el.remove();
}
