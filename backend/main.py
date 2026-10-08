import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api.routes import router as api_router

load_dotenv()

# Initialize FastAPI app instance
app = FastAPI(
    title="CodeSense AI - Sales Agent Service",
    description="Production-ready FastAPI service wrapping a stateful LangGraph Sales Agent with Human-in-the-Loop guardrails.",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows frontends (React, Next.js, Vue, or mobile apps) hosted on different domains to make HTTP requests to this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # In production, replace "*" with your frontend domain (e.g., https://mycompany.com)
    allow_credentials=True,
    allow_methods=["*"],        # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

# Register routes with /api/v1 URL prefix
app.include_router(api_router, prefix="/api/v1", tags=["Sales Agent"])


# Root health-check endpoint
@app.get("/", tags=["Health Check"])
async def root_health_check():
    return {
        "status": "online",
        "service": "CodeSense AI Sales Agent API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)