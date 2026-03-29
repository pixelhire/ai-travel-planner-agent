// ================================
// DOM
// ================================

const sendBtn = document.getElementById("sendBtn");
const queryInput = document.getElementById("query");
const tripList = document.getElementById("tripList");
const newTripBtn = document.getElementById("newTripBtn");
const chatContainer = document.getElementById("chatContainer");
let hasShownFinal = false;

// ================================
// STATE
// ================================

let trips = [];
let currentTrip = null;
let streamingInterval = null;
let lastPlanCount = 0;

// ================================
// INIT
// ================================

document.addEventListener("DOMContentLoaded", async () => {
  let storedTripId = sessionStorage.getItem("trip_id");

  if (storedTripId) {
    currentTrip = storedTripId;
    await openTrip(currentTrip);
  } else {
    await createTrip(true);
  }

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
  } catch (err) {
    console.error("Failed loading trips", err);
  }
}

// ================================
// CREATE TRIP
// ================================

async function createTrip(setSession = false) {
  try {
    const res = await fetch("/trips", { method: "POST" });
    const trip = await res.json();

    trips.unshift(trip);
    renderTrips();

    currentTrip = trip.id;

    if (setSession) {
      sessionStorage.setItem("trip_id", trip.id);
    }

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
  sessionStorage.setItem("trip_id", id);

  // ✅ reset UI state
  chatContainer.innerHTML = "";
  lastPlanCount = 0;
  hasShownFinal = false;

  try {
    const res = await fetch(`/trips/${id}`);
    const trip = await res.json();

    // =========================================================
    // ✅ SYNC STATE (important for streaming logic)
    // =========================================================
    lastPlanCount = trip.plans?.length || 0;

    // =========================================================
    // 🔥 RENDER EXISTING DATA (FIXED - NO DUPLICATES)
    // =========================================================

    if (trip.history?.length) {
      const history = trip.history;

      history.forEach((item, index) => {
        const isLast = index === history.length - 1;

        // ✅ skip last history item if it's same as final_plan
        if (
          isLast &&
          trip.final_plan?.output &&
          item.output === trip.final_plan.output
        ) {
          return;
        }

        if (item.input) addUserMessage(item.input);
        if (item.output) addBotMessage(item.output);
      });
    }

    // ✅ render latest final plan ONLY ONCE
    if (trip.final_plan?.output) {
      if (trip.final_plan.input) {
        addUserMessage(trip.final_plan.input); // ✅ restore query
      }

      addBotMessage(trip.final_plan.output);
      hasShownFinal = true;
    }

    // =========================================================
    // 🔥 BACKWARD COMPAT (OLD STRUCTURE)
    // =========================================================
    else if (trip.plans && trip.plans.length > 0) {
      trip.plans.forEach((p) => {
        if (p.plan?.input) addUserMessage(p.plan.input);
        if (p.plan?.output) addBotMessage(p.plan.output);
      });
    }
  } catch (err) {
    console.error("Load trip failed", err);
  }

  // ✅ start live updates AFTER initial render
  startStreaming();

  renderTrips();
}

function renderExistingTrip(trip) {
  const chat = document.getElementById("chatContainer");
  chat.innerHTML = "";

  // ✅ render history
  if (trip.history) {
    trip.history.forEach((item) => {
      addUserMessage(item.input);
      addBotMessage(item.output);
    });
  }

  // ✅ render latest final plan
  if (trip.final_plan?.output) {
    addUserMessage(trip.final_plan.input);
    addBotMessage(trip.final_plan.output);
  }
}

// ================================
// STREAMING (🔥 CORE FEATURE)
// ================================

function startStreaming() {
  if (streamingInterval) clearInterval(streamingInterval);

  streamingInterval = setInterval(async () => {
    if (!currentTrip) return;

    try {
      const res = await fetch(`/trips/${currentTrip}`);
      const trip = await res.json();

      // ✅ SUPPORT BOTH NEW + OLD STRUCTURE
      const expected =
        trip?.status?.expected_tasks || trip.expected_tasks || [];

      const completed =
        trip?.status?.completed_tasks || trip.completed_tasks || [];

      // ✅ update progress UI
      if (completed.length === expected.length) {
        removeLoading(); // ✅ remove when done
      } else {
        let statusText = expected
          .map((task) =>
            completed.includes(task)
              ? `✅ ${task} ready`
              : `⏳ ${task} generating...`
          )
          .join("\n");

        updateLoading(statusText);
      }

      // =========================================================
      // 🔥 NEW STRUCTURE (PRIMARY): final_plan
      // =========================================================
      if (
        trip.final_plan?.output &&
        !hasShownFinal &&
        completed.length === expected.length &&
        trip.final_plan.input === trip.last_query
      ) {
        removeLoading(); // ✅ remove progress UI

        addBotMessage(trip.final_plan.output);

        hasShownFinal = true;
        return;
      }

      // =========================================================
      // 🔥 BACKWARD COMPAT (OLD): plans[]
      // =========================================================
      if (trip.plans && trip.plans.length > lastPlanCount) {
        const newPlan = trip.plans[trip.plans.length - 1];

        removeLoading();

        if (newPlan.plan?.input) {
          addUserMessage(newPlan.plan.input);
        }

        if (newPlan.plan?.output) {
          addBotMessage(newPlan.plan.output);
        } else {
          addBotMessage("Generating response...");
        }

        lastPlanCount = trip.plans.length;
        hasShownFinal = true;
        return;
      }
    } catch (err) {
      console.error("Streaming error", err);
    }
  }, 1000);
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

// ================================
// DELETE / RENAME
// ================================

async function deleteTrip(id) {
  const confirmDelete = confirm("Delete this trip?");
  if (!confirmDelete) return;

  try {
    await fetch(`/trips/${id}`, { method: "DELETE" });
    await loadTrips();
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
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newName }),
    });

    const trip = trips.find((t) => t.id === id);
    if (trip) trip.title = newName;

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

  // ✅ ensure trip exists
  if (!currentTrip) {
    await createTrip(true);
  }

  // ✅ reset state BEFORE anything
  hasShownFinal = false;
  lastPlanCount = 0;

  queryInput.value = "";

  // ✅ show user message
  addUserMessage(query);

  // 🔥 REMOVE any stale loading or ghost state
  removeLoading();

  // ✅ show fresh loading
  showLoading();

  try {
    await fetch("/plan-trip", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        trip_id: currentTrip,
        query: query,
      }),
    });

    // ❌ DO NOT wait here (streaming handles UI)
  } catch (err) {
    removeLoading();
    addBotMessage("Error generating trip.");
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

function updateLoading(text) {
  let el = document.getElementById("loading");

  // ✅ show only if still processing
  if (!el && text.includes("⏳")) {
    showLoading();
    el = document.getElementById("loading");
  }

  if (el) el.textContent = text;
}
