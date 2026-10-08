# CodeSense AI frontend

## Run locally

The frontend lives in `frontend/`. Run these commands from that directory:

```sh
cd frontend
npm install
npm run dev
```

Copy `frontend/.env.example` to `frontend/.env` and set
`VITE_API_BASE_URL` to the backend API (the default is
`http://localhost:8000/api/v1`). The browser sends only the public chat
payload `{ thread_id, message }`; no API keys are bundled.

## Backend contract

Start the backend from the repository root with:

```sh
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The typed client in `src/api` calls `POST /chat`, validates the response at runtime, and distinguishes network, timeout, client, server, and malformed-response failures. Pending review and approval methods are implemented for internal integration but approval is intentionally not exposed in the visitor UI.

Chat state is held in `ChatProvider`. A thread ID is persisted in `sessionStorage` for the current browser session; it is not durable history. Avoid sharing secrets or credentials in chat.

## Quality

`npm run build` runs strict TypeScript checking and the Vite production build.
