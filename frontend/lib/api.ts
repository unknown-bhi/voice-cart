// frontend/lib/api.ts

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

// Backend se aane wale response ka TypeScript interface (Pydantic schema ke mutabiq)
export interface SessionResponse {
  session_id: string;
  token: string;
  room_name: string;
  ws_url: string;
}

export async function createSession(userId: string): Promise<SessionResponse> {
  const res = await fetch(`${BACKEND_URL}/api/v1/session`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId }),
  });

  if (!res.ok) {
    if (res.status === 429) {
      throw new Error("You already have 2 active sessions. Please end one first.");
    }
    throw new Error("Failed to create session. Check if backend is running.");
  }

  return res.json();
}

export async function endSession(sessionId: string): Promise<void> {
  try {
    await fetch(`${BACKEND_URL}/api/v1/session/${sessionId}`, {
      method: "DELETE",
    });
  } catch (err) {
    console.error("Failed to end session on backend:", err);
  }
}