# AI Travel Planner Agent

An AI-powered travel planning system that generates personalized trip itineraries through a conversational interface.

Users can create multiple trip sessions, ask follow-up questions, and iteratively refine travel plans while maintaining organized trip history.

The system combines an AI planning agent, persistent trip storage, and a lightweight chat-based UI to deliver structured travel itineraries.

---

# Architecture

User Query
↓
Trip Session Manager
↓
AI Travel Planning Agent
↓
LLM Reasoning
↓
Generate Travel Plan (input → output)
↓
Persist Plan to Trip Storage
↓
Render Conversation in UI

---

# System Architecture

Frontend UI (Vanilla JS)
↓
FastAPI Backend
↓
Travel Planning Agent
↓
Trip Session Storage (JSON)

---

# Agent Workflow

User creates or selects a trip session
↓
User sends travel request (destination, days, budget, etc.)
↓
Request is processed by the AI planning agent
↓
LLM generates a structured travel itinerary
↓
Plan is returned to the backend
↓
Plan is stored in trip session storage
↓
UI renders conversation as chat bubbles

---

# Features

✔ Conversational travel planning
✔ Multiple trip sessions
✔ Iterative itinerary refinement
✔ Persistent trip storage
✔ Trip rename and deletion
✔ Chat-style interaction interface
✔ Lightweight local storage architecture
✔ Simple deployment with no external database

---

# Tech Stack

Python
FastAPI
OpenAI API
Vanilla JavaScript
HTML
CSS
JSON file-based storage

---

# Data Model

Each trip session is stored as a JSON document.

Trip structure:

```json
{
  "id": "trip-id",
  "title": "Trip Name",
  "plans": [
    {
      "id": "plan-id",
      "plan": {
        "input": "User request",
        "output": "Generated itinerary"
      }
    }
  ]
}
```

Each plan represents a single interaction between the user and the AI travel agent.

---

# Project Structure

```
ai-travel-planner-agent

backend
 ├─ routes
 │   └─ trips_routes.py
 ├─ services
 │   └─ trip_service.py
 ├─ utils
 │   └─ config.py

frontend
 ├─ static
 │   ├─ app.js
 │   └─ styles.css
 └─ templates
     └─ index.html

trips
 └─ JSON trip storage
```

---

# Trip Session Management

Each trip acts as an independent session.

Trips allow users to:

• Organize multiple travel plans
• Iterate on travel ideas
• Maintain conversation context per trip

This design mirrors how modern AI systems structure conversations.

---

# UI Interaction Model

Sidebar

• Create new trips
• Rename existing trips
• Delete trips
• Navigate between trip sessions

Chat Interface

• User prompt input
• AI-generated itinerary response
• Persistent conversation per trip

---

# Storage Design

The system uses file-based JSON storage for simplicity and transparency.

Benefits:

• No external database required
• Easy debugging
• Human-readable trip history
• Lightweight local development

---

# Example Interaction

User

```
Plan a 6 day trip to Bali
```

Agent Response

```
Day 1: Arrival in Bali  
Day 2: Explore Ubud  
Day 3: Nusa Penida Day Trip  
Day 4: Tanah Lot & Canggu  
Day 5: Beach relaxation  
Day 6: Departure
```

User can refine the plan:

```
Make it budget friendly
```

The agent generates an updated itinerary while preserving the trip session.

---

# Running the Project

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Open the application in your browser:

```
http://localhost:8000
```

---

# Future Improvements

• Structured itinerary UI (days, activities, budget)
• Travel cost estimation
• Flight and hotel API integration
• Vector memory for travel context
• AI travel recommendation engine
• Multi-user authentication

---

<!-- # Author

Sagar S
AI Engineer / Systems Builder -->
