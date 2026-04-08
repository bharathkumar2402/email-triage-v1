from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

from server.environment import EmailTriageEnvironment

app = FastAPI()

# Initialize environment
env = EmailTriageEnvironment()


# ---------------- HEALTH CHECK ----------------

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}


# ---------------- RESET ----------------

@app.post("/reset")
def reset():
    observation = env.reset()
    return observation.dict()


# ---------------- STEP ----------------

class ActionRequest(BaseModel):
    urgency: str
    key_action: str
    sender_intent: str
    response: str = ""
    confidence: float = 0.5


@app.post("/step")
def step(action: ActionRequest):
    result = env.step(action.dict())
    return {
        "observation": result.observation.dict(),
        "reward": result.reward.dict(),
        "done": result.done,
        "info": result.info
    }


# ---------------- STATE ----------------

@app.get("/state")
def state():
    return env.state()



def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()