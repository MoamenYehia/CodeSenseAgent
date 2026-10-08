# CodeSense AI UI Handoff

This document is a product and implementation brief for building the frontend of
CodeSense AI. It is written so it can be given directly to Claude or another UI
implementation agent.

## 1. Product summary

CodeSense AI is an AI-powered B2B sales engineer for a code review and security
analysis platform. A visitor can ask about features, integrations, pricing,
security, deployment options, and policies. The assistant qualifies the lead,
recommends a plan, records useful lead information, and helps the visitor move
toward a demo or trial.

The frontend should feel like a polished modern developer/SaaS product rather
than a generic chatbot:

- Technical, trustworthy, and professional.
- Clear about pricing and plan differences.
- Helpful and conversational, not pushy.
- Privacy-conscious when collecting company or contact information.
- Fully usable on desktop and mobile.

## 2. Current backend

The repository is organized as a small monorepo:

```text
backend/   FastAPI, LangGraph, tools, local retrieval data
frontend/  Vite, React, TypeScript, Tailwind UI
docs/      Product, frontend, and build handoff documentation
```

The backend is a FastAPI application running locally by default at:

```text
http://localhost:8000
```

API routes are mounted under `/api/v1`.

From the repository root, start the backend from `backend/`:

```text
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Use Python 3.11 for the backend environment. The LangChain and Chroma
dependencies may not yet be compatible with every newer Python release.

Interactive API documentation is available when the backend is running:

```text
http://localhost:8000/docs
```

The frontend must not hard-code API keys. The backend owns all model,
enrichment, retrieval, and CRM integrations.

## 3. Required frontend experience

Build a single-page application with these areas:

### A. Header

- CodeSense AI logo/wordmark.
- Navigation links or anchor buttons for `Platform`, `Plans`, `Security`, and
  `How it works`.
- A prominent `Talk to an AI Sales Engineer` or `Start conversation` CTA.
- A compact mobile navigation menu.

### B. Hero section

Explain the product in one sentence, for example:

> AI-powered code review and security analysis for every pull request.

Include:

- A short supporting paragraph.
- A primary CTA that opens or focuses the chat.
- A secondary CTA that scrolls to plans or platform capabilities.
- A visual preview of the assistant reviewing a pull request or finding a
  security issue. This can be a designed mockup; do not claim that the UI
  itself performs code analysis.

### C. Platform capabilities

Show cards for:

1. Real-time pull request code reviews.
2. Automated refactoring suggestions.
3. Dependency and secret scanning.
4. Architecture and performance guardrails.

Mention support for GitHub, GitLab, and Bitbucket, while preserving the plan
restrictions described below.

### D. Pricing section

Use three comparison cards:

#### Solo Developer

- `$29/month` or `$290/year`.
- One developer seat.
- Up to 3 private repositories and unlimited public repositories.
- GitHub integration.
- Standard response time: within 5 minutes.
- Weekly security digest.
- Community Discord and email support with a 48-hour response SLA.
- 14-day free trial without a credit card.

#### Team

- `$199/month` or `$1,990/year`.
- Up to 15 developer seats, with additional seats available up to 25.
- Unlimited public and private repositories.
- GitHub, GitLab Cloud, and Bitbucket Cloud.
- Priority PR reviews under 60 seconds.
- Slack and Discord webhooks.
- Custom rules and dependency vulnerability patching.
- Business support with a 4-hour response SLA.
- 14-day free trial without a credit card.

#### Enterprise

- Custom annual contract, starting at `$1,500/month`.
- Unlimited seats, repositories, and organizations.
- Cloud and self-hosted Git integrations.
- Multi-tenant cloud, single-tenant VPC, or air-gapped on-premises deployment.
- SOC2 Type II, ISO 27001, and HIPAA compliance reports.
- Zero-data-retention policy.
- Dedicated Customer Success Manager and Solutions Architect.
- 99.95% uptime SLA and 30-minute priority incident response.
- Custom LLM fine-tuning.
- Requires a technical discovery call before deployment.

Include a monthly/yearly toggle if practical. Do not invent prices, features,
discounts, or guarantees beyond the information in this document.

### E. Chat panel

The chat is the primary interactive feature. It should support:

- Empty state with suggested questions.
- User and assistant message bubbles.
- Timestamps or relative times.
- Loading state while waiting for the API.
- Error state with a retry action.
- Auto-scroll to the newest message.
- Enter to send and Shift+Enter for a newline.
- Disabled send button for empty or in-flight messages.
- Responsive layout: a large chat panel on desktop and a full-screen or
  bottom-sheet experience on mobile.

Suggested starter prompts:

- `Which plan is best for a 10-person engineering team?`
- `Do you support GitLab and self-hosted deployments?`
- `What security and compliance features do you offer?`
- `Can I try CodeSense without a credit card?`

## 4. Conversation and thread behavior

Every conversation needs a stable `thread_id`. Generate it once when a new
conversation starts, store it in frontend state, and reuse it for every
message in that conversation. A UUID is preferred; a readable fallback such as
`session-<timestamp>` is acceptable.

The current API uses in-memory LangGraph checkpointing, so the frontend should
preserve the thread ID during the active browser session but should not promise
durable conversation history across backend restarts.

When starting a new conversation:

1. Generate a new thread ID.
2. Clear the visible messages.
3. Send subsequent messages with that same ID.

## 5. API contract

Set the API base URL through an environment variable, for example:

```text
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Send a chat message

```http
POST /chat
Content-Type: application/json
```

Request:

```json
{
  "thread_id": "session-108",
  "message": "Which plan is best for my 10-person engineering team?"
}
```

Successful normal response:

```json
{
  "thread_id": "session-108",
  "status": "COMPLETED",
  "response": "The Team plan is the best fit ...",
  "interrupt_details": null
}
```

The UI should treat status values case-insensitively, but the current backend
returns `COMPLETED` and `INTERRUPTED`.

## 6. Human escalation flow

Some enterprise requests pause the AI workflow and require a human decision.
This is an expected product state, not a generic error.

Escalation can be triggered by requests involving items such as:

- On-premises, air-gapped, or VPC deployment.
- Custom enterprise contracts.
- Compliance or security reviews.
- A Sales Director review.

Interrupted response example:

```json
{
  "thread_id": "session-108",
  "status": "INTERRUPTED",
  "response": "Your request involves custom Enterprise requirements...",
  "interrupt_details": {
    "status": "Action Required",
    "message": "The reason of escalation is: Custom compliance or On-Premise deployment requested.",
    "instructions": "Accept the enterprise decision or override it."
  }
}
```

When the response is interrupted:

1. Render the assistant's `response`.
2. Render a visually distinct `Human review required` card.
3. Show `interrupt_details.message` and `interrupt_details.instructions`
   when present.
4. Keep the composer available so the user can continue the same thread if
   appropriate.
5. Do not display raw object syntax such as `[object Object]`.

### Resume an escalation

If the UI includes an internal sales-review experience, it can resume a paused
thread with:

```http
POST /approve_escalation
Content-Type: application/json
```

Request:

```json
{
  "thread_id": "session-108",
  "decision": "Approved for the enterprise plan"
}
```

Response:

```json
{
  "thread_id": "session-108",
  "status": "RESUMED_AND_COMPLETED",
  "final_response": "[Sales Director Review]: Approved for the enterprise plan"
}
```

This action should be hidden from ordinary visitors unless the product later
adds authentication and an internal sales dashboard. For the public UI, show
the escalation status and a clear next step such as `Request an enterprise
discovery call`.

### Check pending review

The backend also exposes:

```http
GET /pending_reviews/{thread_id}
```

This can be used for a future internal review dashboard or recovery flow. The
main `/chat` response is the source of truth immediately after sending a
message.

## 7. Error handling

Implement explicit states for:

- Backend unavailable.
- Request timeout.
- HTTP 4xx validation errors.
- HTTP 5xx processing errors.
- Empty or malformed API responses.

Use a friendly message such as:

> We could not reach the sales engineer. Check that the API is running and try
> again.

Provide a retry action and preserve the user's unsent draft. Never display
environment variables, stack traces, API keys, or raw internal exceptions.

## 8. Recommended visual direction

- Dark charcoal or deep navy foundation with an electric blue/cyan accent.
- High contrast and accessible text.
- Soft borders, restrained gradients, and subtle glow around important CTAs.
- Monospace styling only for code, repository names, and technical metadata.
- Use cards and badges to communicate plan limits and integration support.
- Use green for completed states, amber for review-required states, and red
  only for errors.
- Avoid excessive animations. Use short transitions for messages, loading, and
  section navigation.
- Meet WCAG-friendly contrast and keyboard navigation expectations.

## 9. Suggested frontend structure

Use the framework and component conventions already present in the frontend
project. If no frontend exists yet, a practical choice is React with
TypeScript and a utility CSS system.

Suggested components:

```text
App
├── Header
├── Hero
├── CapabilityGrid
├── PricingSection
│   ├── BillingToggle
│   └── PricingCard
├── ChatSection
│   ├── ChatHeader
│   ├── MessageList
│   ├── SuggestedPrompts
│   ├── EscalationCard
│   └── MessageComposer
└── Footer
```

Suggested API helpers:

```text
api/client
├── sendChatMessage(threadId, message)
├── checkPendingReview(threadId)
└── approveEscalation(threadId, decision)
```

Keep API calls separate from visual components. Define typed interfaces for
the request and response shapes. Do not use `any` for API responses.

## 10. Acceptance criteria

The UI is ready when:

- A user can open the page and understand CodeSense AI within a few seconds.
- A user can start a conversation without manually entering a thread ID.
- A message is sent to `POST /api/v1/chat` with the correct payload.
- Multiple messages reuse the same thread ID.
- `COMPLETED` responses render as assistant messages.
- `INTERRUPTED` responses render as a human-review state, not as an error.
- The UI handles loading, retry, empty, timeout, and server-error states.
- Pricing and plan restrictions match this document.
- The layout works on mobile and desktop.
- Keyboard navigation, focus states, labels, and contrast are handled.
- No secrets or backend stack traces are exposed to the browser UI.

## 11. Important backend notes

- The API currently enables permissive CORS for development. Production
  deployment should restrict allowed origins.
- The backend uses a memory checkpointer, so server restarts can remove active
  thread state.
- The frontend should rely on the documented response fields and tolerate
  nullable `response`, `interrupt_details`, and `final_response` values.
- Verify the API with the generated FastAPI docs before final integration, and
  keep the API base URL configurable.
