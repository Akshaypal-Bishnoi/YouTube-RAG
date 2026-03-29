const API_BASE_URL = "https://youtube-rag-app.onrender.com";

let CURRENT_VIDEO_ID = null;

const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const messages = document.getElementById("messages");

function setStatus(active, text) {
  statusDot.classList.toggle("active", active);
  statusText.textContent = text;
}

function addMessage(role, text) {
  const msg = document.createElement("div");
  msg.className = "msg " + role;
  msg.textContent = text;
  messages.appendChild(msg);
  messages.scrollTop = messages.scrollHeight;
}

function extractVideoId(url) {
  try {
    const u = new URL(url);
    if (u.hostname.includes("youtube.com")) {
      return u.searchParams.get("v");
    }
    if (u.hostname === "youtu.be") {
      return u.pathname.slice(1);
    }
  } catch {
    return null;
  }
}

document.getElementById("loadVideo").addEventListener("click", async () => {
  const url = document.getElementById("videoUrl").value.trim();
  const videoId = extractVideoId(url);

  if (!videoId) {
    setStatus(false, "Invalid YouTube URL");
    return;
  }

  setStatus(false, "Indexing video…");

  try {
    const res = await fetch(`${API_BASE_URL}/index-video`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_id: videoId }),
    });

    const data = await res.json();

    if (!res.ok) {
      addMessage("bot", `❌ ${data.detail}`);
      setStatus(false, "Indexing failed");
      return;
    }

    CURRENT_VIDEO_ID = videoId;
    setStatus(true, "Video indexed");
    addMessage("bot", "✅ Video indexed successfully. Ask your question.");

  } catch {
    addMessage("bot", "❌ Backend not reachable.");
    setStatus(false, "Backend error");
  }
});

document.getElementById("sendBtn").addEventListener("click", askQuestion);

document.getElementById("questionInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    askQuestion();
  }
});

async function askQuestion() {
  if (!CURRENT_VIDEO_ID) {
    addMessage("bot", "⚠️ Please load a video first.");
    return;
  }

  const input = document.getElementById("questionInput");
  const question = input.value.trim();
  if (!question) return;

  input.value = "";
  addMessage("user", question);

  const thinking = document.createElement("div");
  thinking.className = "msg bot";
  thinking.textContent = "Thinking…";
  messages.appendChild(thinking);

  try {
    const res = await fetch(`${API_BASE_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        video_id: CURRENT_VIDEO_ID,
        question,
      }),
    });

    const data = await res.json();
    thinking.remove();

    if (!res.ok) {
      addMessage("bot", `❌ ${data.detail}`);
      return;
    }

    addMessage("bot", data.answer);

  } catch {
    thinking.remove();
    addMessage("bot", "❌ Failed to get response.");
  }
}

document.getElementById("loadExample").addEventListener("click", () => {
  document.getElementById("videoUrl").value =
    "https://www.youtube.com/watch?v=6TuUfeT1L10&t=4s";

  document.getElementById("questionInput").value =
    "Does life exist outside of Earth?";

  addMessage("bot", "Example loaded. Click 'Load & Index Video' to start.");
});