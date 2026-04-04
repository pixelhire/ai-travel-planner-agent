// ================================
// DOM
// ================================

const sendBtn = document.getElementById("sendBtn");
const queryInput = document.getElementById("query");
const tripList = document.getElementById("tripList");
const newTripBtn = document.getElementById("newTripBtn");
const chatContainer = document.getElementById("chatContainer");

let hasShownFinal = false;
let activeQuery = null;
let activeResponseEl = null;
let hasContent = false;

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
      sessionStorage.setItem("trip_id", currentTrip);
    }

    // ✅ clear UI for new trip
    chatContainer.innerHTML = "";

    // ✅ LOAD EMPTY CHAT FOR NEW TRIP
    chatContainer.innerHTML = "";
    activeResponseEl = null;
    hasShownFinal = false;
  } catch (err) {
    console.error("Create trip failed", err);
  }
}

newTripBtn.addEventListener("click", async () => {
  await createTrip(true);

  // ✅ FORCE LOAD EMPTY CHAT
  chatContainer.innerHTML = "";
  activeResponseEl = null;
  hasShownFinal = false;
  renderTrips();
});

// ================================
// OPEN TRIP
// ================================

async function openTrip(id) {
  // ✅ STOP STREAMING
  if (streamingInterval) {
    clearInterval(streamingInterval);
    streamingInterval = null;
  }

  currentTrip = id;
  sessionStorage.setItem("trip_id", currentTrip);

  // ✅ CLEAR UI FIRST
  chatContainer.innerHTML = "";

  lastPlanCount = 0;
  hasShownFinal = false;
  activeResponseEl = null;

  try {
    const res = await fetch(`/trips/${id}`);
    const trip = await res.json();

    lastPlanCount = trip.plans?.length || 0;

    // ✅ RENDER history
    if (trip.history?.length) {
      trip.history.forEach((item) => {
        if (item.input) addUserMessage(item.input);
        if (item.output) addBotMessage(item.output);
      });
      hasContent = true;
    }

    // ✅ RENDER final plan
    // ✅ render final_plan ONLY if not already in history
    if (trip.final_plan?.output) {
      const lastHistory = trip.history?.[trip.history.length - 1];

      const isDuplicate =
        lastHistory && lastHistory.output === trip.final_plan.output;

      if (!isDuplicate) {
        if (trip.final_plan.input) {
          addUserMessage(trip.final_plan.input);
        }

        addBotMessage(trip.final_plan.output);
        hasShownFinal = true;
        hasContent = true;
      }
      hasContent = true;
    }

    // ✅ BACKWARD COMPAT
    else if (trip.plans && trip.plans.length > 0) {
      trip.plans.forEach((p) => {
        if (p.plan?.input) addUserMessage(p.plan.input);
        if (p.plan?.output) addBotMessage(p.plan.output);
      });
      hasContent = true;
    }

    // ✅ EMPTY STATE (SAFE + CORRECT)
    if (!hasContent) {
      const div = document.createElement("div");
      div.className = "message bot empty-state";
      div.textContent = "Start planning your trip...";
      chatContainer.appendChild(div);
    }
  } catch (err) {
    console.error("Load trip failed", err);
  }

  renderTrips();
}

// ================================
// STREAMING
// ================================

function startStreaming() {
  if (streamingInterval) clearInterval(streamingInterval);

  streamingInterval = setInterval(async () => {
    if (!currentTrip) return;

    try {
      const res = await fetch(`/trips/${currentTrip}`);
      const trip = await res.json();

      const expected =
        trip?.status?.expected_tasks || trip.expected_tasks || [];

      const completed =
        trip?.status?.completed_tasks || trip.completed_tasks || [];

      if (completed.length !== expected.length) {
        let statusText = expected
          .map((task) =>
            completed.includes(task)
              ? `✅ ${task} ready`
              : `⏳ ${task} generating...`
          )
          .join("\n");

        updateLoading(statusText);
      }

      // ✅ FIX: remove activeQuery condition
      if (trip.final_plan?.output && !hasShownFinal) {
        if (activeResponseEl) {
          activeResponseEl.textContent = trip.final_plan.output;
          activeResponseEl = null;
        } else {
          addBotMessage(trip.final_plan.output);
        }

        hasShownFinal = true;

        clearInterval(streamingInterval);
        streamingInterval = null;
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

    title.onclick = (e) => {
      e.stopPropagation();
      openTrip(trip.id);
    };

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

  if (!currentTrip) {
    await createTrip(true);
  }

  hasShownFinal = false;
  lastPlanCount = 0;

  queryInput.value = "";

  const emptyState = chatContainer.querySelector(".empty-state");
  if (emptyState) {
    emptyState.remove();
  }

  addUserMessage(query);

  // ✅ FIX: create placeholder properly
  const botEl = addBotMessage("✈️ Planning trip...");
  activeResponseEl = botEl.querySelector("pre");

  try {
    await fetch("/plan-trip", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        trip_id: currentTrip,
        query: query,
      }),
    });

    activeQuery = query;

    startStreaming();
  } catch (err) {
    console.error("API ERROR", err);
    addBotMessage("Error generating trip.");
  }
}

// ================================
// CHAT UI
// ================================

function addUserMessage(text) {
  const emptyState = chatContainer.querySelector(".empty-state");
  if (emptyState) emptyState.remove();

  const div = document.createElement("div");
  div.className = "message user";
  div.textContent = text;
  chatContainer.appendChild(div);
  scrollToBottom();
}

function addBotMessage(text) {
  const emptyState = chatContainer.querySelector(".empty-state");
  if (emptyState) emptyState.remove();

  const div = document.createElement("div");
  div.className = "message bot";

  const pre = document.createElement("pre");
  // 🔥 CLEAN "content='...'" garbage
  let cleanedText = text;

  // remove content='...'
  if (cleanedText.startsWith("content=")) {
    const match = cleanedText.match(/content=['"](.*)['"]/s);
    if (match && match[1]) {
      cleanedText = match[1];
    }
  }

  // remove escaped newlines
  cleanedText = cleanedText.replace(/\\n/g, "\n");

  pre.textContent = cleanedText;

  div.appendChild(pre);
  chatContainer.appendChild(div);
  scrollToBottom();

  return div;
}

function updateLoading(text) {
  if (activeResponseEl) {
    activeResponseEl.textContent = text;
    scrollToBottom();
  }
}

function scrollToBottom() {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}
