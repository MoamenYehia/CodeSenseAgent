# CodeSense AI: Frontend Build Prompt

> **How to use:** Put the backend handoff README in your repo as `docs/HANDOFF.md`, open Copilot Chat (Agent mode) in VS Code, and paste everything below the line. If you want it to persist, also save it as `.github/copilot-instructions.md`.

---

## ROLE

You are a senior frontend engineer and product designer building the marketing site and AI sales-chat frontend for **CodeSense AI**, a B2B SaaS that does AI-powered code review and security analysis on every pull request. Your standard is a production-grade, award-quality SaaS website, not a template and not a generic chatbot demo.

Read `docs/HANDOFF.md` first. It is the source of truth for the backend, the API contract, the pricing, plan limits, and the escalation flow. **Never invent prices, features, discounts, guarantees, customer logos, testimonials, statistics, or compliance claims** beyond what that document states. Where a section would normally contain social proof, omit it or use a clearly labeled placeholder.

## TECH STACK

- Vite + React 18 + TypeScript (strict mode) + React Router v6
- Tailwind CSS with the design tokens below defined in `tailwind.config` / CSS variables
- `lucide-react` for icons, `framer-motion` only for short, restrained transitions (respect `prefers-reduced-motion`)
- Fonts via `@fontsource`: **Fraunces** (display headings), **Inter** (UI/body), **JetBrains Mono** (code, repo names, technical metadata only)
- No UI kit that overrides the palette. Build components by hand, or use headless primitives (Radix) styled with Tailwind.
- No `any` types for API data. No API keys in the frontend. API base URL comes from `import.meta.env.VITE_API_BASE_URL` (default `http://localhost:8000/api/v1`). Provide `.env.example`.

## BRAND & DESIGN SYSTEM

**Personality:** warm, editorial, confident, and trustworthy. Think "a premium engineering publication meets developer tooling". This is a **light, warm theme**, deliberately different from the usual dark-blue-and-neon dev-tool look. (This palette replaces the dark/cyan direction suggested in the README section 8; all other README direction on tone, accessibility, and restraint still applies.)

### Color palette (use exactly these brand colors)

| Token | Hex | Role |
|---|---|---|
| `crimson` | `#790D16` | Primary brand, CTAs, key links, hero emphasis, dark feature sections |
| `sand` | `#E5D3AF` | Secondary surfaces, highlighted cards, badges, dividers, "popular" plan accent |
| `cream` | `#F5EFE1` | Main page background |
| `mist` | `#AEC4D4` | Cool accent: illustrations, chart/diagram fills, info badges, integration chips, assistant-message accent |

**Derived neutrals and states** (you may derive these from the palette; do not introduce new hues beyond them):

- `ink` `#231416`: primary text (warm near-black). `ink-soft` `#5A4A4C`: secondary text.
- `crimson-deep` `#4E0A10`: hover/pressed state and darkest sections. `crimson-tint` `#F3DEDF`: subtle crimson backgrounds.
- `paper` `#FBF8F0`: elevated card surface on cream. `line` `#DCCFB4`: borders (a sand shade).
- `success` `#2F6B4F` (completed), `warning` `#B7791F` on `#FBEFD3` (human review required), `error` `#B42318` on `#FDECEA` (errors only). Brand crimson is **never** used to signal errors; errors always pair red with an icon and text.

### Contrast rules (WCAG AA minimum)

- Body text: `ink` on `cream`/`paper`. Never `mist` or `sand` as text color on light backgrounds.
- `mist` and `sand` are **surface/decoration colors**; text on them is always `ink`.
- On `crimson` or `crimson-deep` backgrounds, use `cream` text; `mist` is allowed for secondary text there.
- Primary button: `crimson` bg, `cream` text, hover `crimson-deep`. Secondary button: transparent bg, 1.5px `crimson` border, `crimson` text, hover `crimson-tint`. Visible 2px focus ring in `crimson` with a 2px `cream` offset on every interactive element.

### Visual language

- Generous whitespace, 12-col grid, max content width ~1200px, section vertical rhythm 96-128px desktop / 64px mobile.
- Headlines in Fraunces (large, tight tracking, one emphasized word in `crimson` italic); UI text in Inter.
- Cards: `paper` background, 1px `line` border, 16px radius, soft warm shadow (`0 1px 2px rgba(35,20,22,.06), 0 8px 24px rgba(35,20,22,.06)`). Highlighted plan uses `sand` background with a `crimson` border.
- Subtle background texture: a faint dotted or grid pattern in `sand` at low opacity on hero and a few sections. No neon glows, no purple gradients.
- Alternate sections between `cream` and a full-bleed `crimson` section (cream text) for rhythm. The Security page hero and the final CTA band use `crimson`.
- Transitions 150-250ms. Message bubbles fade/slide in a few pixels. Nothing bouncing or looping.

## PAGES & ROUTES

Use a shared layout (`Header`, `Footer`, floating chat launcher) with React Router. All routes scroll to top on navigation and update `document.title`.

| Route | Page |
|---|---|
| `/` | Home |
| `/platform` | Platform |
| `/pricing` | Pricing |
| `/security` | Security |
| `/how-it-works` | How it works |
| `/chat` | Full-page chat with the AI Sales Engineer |
| `*` | Friendly 404 with links back |

### Header (all pages)

- Wordmark **CodeSense AI** with a simple custom SVG mark (a code bracket combined with a check or sense-wave shape, in `crimson`).
- Nav: `Platform`, `Plans`, `Security`, `How it works` (route links; `Plans` goes to `/pricing`).
- Prominent CTA button: **Talk to an AI Sales Engineer** (shorten to **Start conversation** on small screens). It opens the chat drawer; on `/chat` it focuses the composer.
- Sticky, cream background with blur and a bottom border on scroll. Compact mobile menu (accessible disclosure/drawer, focus trapped, closes on route change and Escape).

### Home (`/`)

1. **Hero:** Headline: *AI-powered code review and security analysis for every pull request.* One supporting paragraph (what it catches, where it runs, works inside the PR workflow). Primary CTA opens chat; secondary CTA scrolls to the plans section. Right side: a **designed mockup** of a pull request review card (file path in mono, a diff snippet, an inline finding such as a hardcoded secret flagged with severity badge, a suggested fix, a "reviewed in under 60 seconds" style chip is allowed only if framed as Team-plan priority review). Add a tiny caption "Illustrative preview". The mockup is static HTML/CSS; the UI itself performs no analysis.
2. **Integration strip:** GitHub, GitLab, Bitbucket chips (text + simple icons). Small note: "Availability depends on plan" linking to `/pricing`.
3. **Capability grid:** the 4 cards (see Platform).
4. **How it works teaser:** 3 steps with link to `/how-it-works`.
5. **Pricing teaser:** the 3 plan cards with the billing toggle (reuse the `PricingSection` component).
6. **Security teaser:** crimson full-bleed band summarizing deployment options and compliance (Enterprise-scoped), link to `/security`.
7. **Final CTA band:** "Not sure which plan fits? Ask our AI Sales Engineer." with chat CTA.

### Platform (`/platform`)

Four detailed capability sections, alternating layout, each with a small designed mockup using palette colors (`mist` fills for diagrams):

1. **Real-time pull request code reviews**
2. **Automated refactoring suggestions**
3. **Dependency and secret scanning**
4. **Architecture and performance guardrails**

Then an **Integrations** section for GitHub, GitLab, and Bitbucket that preserves plan restrictions exactly: Solo = GitHub; Team = GitHub, GitLab Cloud, Bitbucket Cloud; Enterprise = cloud and self-hosted Git integrations. Render this as a compact matrix. End with a CTA to chat.

Write concise, credible copy for each capability from the descriptions above; do not add metrics or capabilities not in the handoff.

### Pricing (`/pricing`)

- `BillingToggle` (Monthly / Yearly) as an accessible switch or segmented control. Yearly shows the yearly price with its own label; do **not** compute or advertise a "savings" percentage or discount (none is documented).
- Three `PricingCard`s. Use the data **exactly**:

**Solo Developer**: `$29/month` or `$290/year`
- One developer seat
- Up to 3 private repositories, unlimited public repositories
- GitHub integration
- Standard response time: within 5 minutes
- Weekly security digest
- Community Discord and email support, 48-hour response SLA
- 14-day free trial, no credit card

**Team** (mark as "Most popular" only if you style it as a recommendation badge, no claims): `$199/month` or `$1,990/year`
- Up to 15 developer seats, additional seats available up to 25
- Unlimited public and private repositories
- GitHub, GitLab Cloud, and Bitbucket Cloud
- Priority PR reviews under 60 seconds
- Slack and Discord webhooks
- Custom rules and dependency vulnerability patching
- Business support, 4-hour response SLA
- 14-day free trial, no credit card

**Enterprise**: custom annual contract, **starting at `$1,500/month`** (no toggle price; show "Custom annual contract")
- Unlimited seats, repositories, and organizations
- Cloud and self-hosted Git integrations
- Multi-tenant cloud, single-tenant VPC, or air-gapped on-premises deployment
- SOC2 Type II, ISO 27001, and HIPAA compliance reports
- Zero-data-retention policy
- Dedicated Customer Success Manager and Solutions Architect
- 99.95% uptime SLA and 30-minute priority incident response
- Custom LLM fine-tuning
- Requires a technical discovery call before deployment

- Card CTAs: Solo and Team = "Start 14-day free trial" (opens chat with a prefilled/sent prompt such as "I'd like to start a free trial of the Team plan"); Enterprise = "Request an enterprise discovery call" (opens chat with that intent).
- Below the cards: a **plan comparison table** (sticky first column, horizontally scrollable on mobile, real `<table>` semantics) and a short **FAQ** (accordion) built only from facts in the handoff: free trial without a credit card, seat limits, which Git providers per plan, deployment options, what Enterprise requires. Include a "Not sure? Ask the AI" link.
- Store all plan data in one typed file `src/data/plans.ts` and render everything from it, so cards and the table never drift apart.

### Security (`/security`)

Crimson hero. Sections: **Deployment options** (multi-tenant cloud, single-tenant VPC, air-gapped on-premises), **Compliance** (SOC2 Type II, ISO 27001, HIPAA reports), **Data handling** (zero-data-retention policy), **Product security features** (dependency and secret scanning). Clearly label Enterprise-scoped items as "Enterprise". Do not claim certifications for Solo or Team. CTA: "Request an enterprise discovery call" opens chat. Mention that compliance and on-premises requests may be reviewed by a human sales director (this matches the escalation flow).

### How it works (`/how-it-works`)

A vertical stepper/timeline (4-5 steps) with a mockup per step: connect your Git provider → open a pull request → get a review with findings and fixes → route alerts to your team (Slack/Discord on Team, weekly digest on Solo) → scale to enterprise deployment if needed. Add a short section on **how the AI Sales Engineer helps**: answers questions, recommends a plan, and moves you toward a trial or demo. Be honest that sales questions are handled by an AI assistant and that some enterprise requests are escalated to a human.

### Footer

Wordmark, short description, link columns (Product, Company-neutral links only to pages that exist), "Talk to an AI Sales Engineer" CTA, and a one-line privacy note about what the chat collects. No fake social links or addresses; use `#` placeholders only if clearly marked with a TODO comment.

## CHAT EXPERIENCE (primary feature)

Build `ChatProvider` (React context + `useReducer`) so the **same conversation persists across route changes**. The chat appears in two forms that share state:

- **Floating launcher + drawer** on every page: bottom-right button (labeled "Ask our AI Sales Engineer") that opens a large panel on desktop (~420-480px wide, tall) and a **full-screen sheet on mobile**.
- **`/chat` page**: a full-height, two-column layout on desktop (conversation + a side panel with the recommended plan summary and quick links; collapses on mobile).

### Components

`ChatSection`, `ChatHeader` (title "CodeSense AI Sales Engineer", status dot, "New conversation" button, close button in drawer), `MessageList`, `MessageBubble`, `SuggestedPrompts`, `EscalationCard`, `ErrorBanner`, `TypingIndicator`, `MessageComposer`.

### Behavior (all required)

- **Empty state** with a short welcome and the 4 suggested prompts as buttons that send immediately:
  - `Which plan is best for a 10-person engineering team?`
  - `Do you support GitLab and self-hosted deployments?`
  - `What security and compliance features do you offer?`
  - `Can I try CodeSense without a credit card?`
- User bubbles in `crimson` with `cream` text; assistant bubbles in `paper` with a `line` border and a small `mist` avatar. Timestamps or relative times ("just now", "2 min ago") with `<time datetime>`.
- **Thread ID:** generate once with `crypto.randomUUID()` (fallback `session-${Date.now()}`), keep in state and `sessionStorage`, reuse for every message. "New conversation" generates a new ID, clears messages, and clears the draft.
- **Composer:** textarea that auto-grows (max ~6 lines). **Enter sends, Shift+Enter inserts a newline.** Ignore Enter during IME composition. Send button disabled when the trimmed message is empty or a request is in flight. Visible label (visually hidden if needed) and `aria-label`s.
- **Loading:** animated typing indicator in the assistant bubble position; composer stays visible but send is disabled; announce via an `aria-live="polite"` region.
- **Auto-scroll** to newest message, but don't yank the user if they scrolled up to read; show a "Jump to latest" pill instead.
- **Errors:** inline `ErrorBanner` with a friendly message and a **Retry** button that resends the failed message **without duplicating it** in the list. **Preserve the unsent draft** if the send failed. Distinct messages for: backend unavailable / network failure, request timeout (use `AbortController`, ~60s since LLM calls are slow), HTTP 4xx, HTTP 5xx, and empty/malformed responses. Default copy: *"We could not reach the sales engineer. Check that the API is running and try again."* Never show stack traces, env vars, keys, or raw exception text.
- **Statuses (case-insensitive):**
  - `COMPLETED`: render `response` as an assistant message.
  - `INTERRUPTED`: render the assistant's `response`, then an **`EscalationCard`** titled **"Human review required"** in amber styling with a distinct icon. Show `interrupt_details.message` and `interrupt_details.instructions` when present (strings only; never render objects, no `[object Object]`). Add a clear next step button: **"Request an enterprise discovery call"** (sends that message in the same thread). **Keep the composer enabled** so the visitor can continue the thread. Do **not** expose the approve-escalation action to visitors.
  - Unknown status or nullable fields: tolerate nulls, fall back to a safe generic message, and never crash.
- Render assistant text safely: support paragraphs, line breaks, lists, and bold via a small sanitizing Markdown renderer (no raw HTML injection, no `dangerouslySetInnerHTML` without sanitization).
- Do not claim durable history: a small note in the chat footer such as "This conversation lasts for your current session."
- Privacy hint under the composer: "Avoid sharing secrets or credentials in chat." Keep it short and unobtrusive.
- Fully keyboard accessible: focus moves to the composer when the drawer opens; Escape closes the drawer and returns focus to the launcher; focus is trapped in the full-screen mobile sheet.

### Side panel on `/chat` (desktop)

A "Your plan fit" card with static plan summaries and links to `/pricing`. Do **not** fabricate lead data; only show information derived from conversation text if you can do it reliably, otherwise show the static summaries.

## API LAYER

Keep it separate from components, in `src/api/`:

```ts
// src/api/types.ts
export interface ChatRequest { thread_id: string; message: string }
export interface InterruptDetails { status?: string | null; message?: string | null; instructions?: string | null }
export type ChatStatus = 'COMPLETED' | 'INTERRUPTED' | (string & {});
export interface ChatResponse {
  thread_id: string;
  status: ChatStatus;
  response: string | null;
  interrupt_details: InterruptDetails | null;
}
export interface ApproveEscalationRequest { thread_id: string; decision: string }
export interface ApproveEscalationResponse { thread_id: string; status: string; final_response: string | null }
```

- `client.ts`: a typed `request<T>()` wrapper with timeout/abort, JSON parsing guards, and a typed `ApiError` (`kind: 'network' | 'timeout' | 'client' | 'server' | 'malformed'`, safe `userMessage`).
- `sendChatMessage(threadId, message)` → `POST ${BASE}/chat` with `{ thread_id, message }`.
- `checkPendingReview(threadId)` → `GET ${BASE}/pending_reviews/{thread_id}` (implemented and typed, unused in the public UI).
- `approveEscalation(threadId, decision)` → `POST ${BASE}/approve_escalation` (implemented and typed, **not wired to any public UI**).
- Runtime-validate the chat response shape (a small type guard or zod) before it touches state.

## PROJECT STRUCTURE

```text
src/
  api/            client.ts, chat.ts, types.ts
  components/
    layout/       Header, Footer, MobileNav, Layout, ScrollToTop
    ui/           Button, Badge, Card, Accordion, Switch, Section, Container
    home/         Hero, PrMockup, IntegrationStrip, CapabilityGrid, StepsTeaser, SecurityBand, FinalCta
    pricing/      BillingToggle, PricingCard, ComparisonTable, PricingFaq
    chat/         ChatProvider, ChatLauncher, ChatDrawer, ChatSection, ChatHeader, MessageList,
                  MessageBubble, SuggestedPrompts, EscalationCard, ErrorBanner, TypingIndicator, MessageComposer
  data/           plans.ts, capabilities.ts, integrations.ts, faq.ts
  hooks/          useChat, useAutoScroll, useMediaQuery
  pages/          Home, Platform, Pricing, Security, HowItWorks, Chat, NotFound
  lib/            cn.ts, time.ts, markdown.tsx, ids.ts
  styles/         globals.css (CSS variables for tokens)
```

## ACCESSIBILITY & QUALITY

- Semantic landmarks (`header`, `nav`, `main`, `footer`), a skip-to-content link, one `h1` per page, logical heading order.
- All controls reachable by keyboard with visible focus; labels on all inputs; `aria-live` for chat status; accessible names on icon buttons.
- Respect `prefers-reduced-motion`. Test contrast of every text/background pair against WCAG AA.
- Responsive from 360px up. No horizontal page scroll; wide tables scroll inside their own container.
- Performance: route-level code splitting (`React.lazy`), no layout shift in the hero, fonts with `font-display: swap`.
- ESLint + Prettier configured; `npm run build` and `tsc --noEmit` must pass with zero errors.

## BUILD ORDER (work in phases and stop to summarize after each)

1. Scaffold the project, Tailwind tokens, fonts, global styles, `Layout`, router, and the `ui/` primitives.
2. Data files (`plans.ts`, etc.) and the Pricing page, since it is the most data-critical.
3. Home, Platform, Security, How it works, and 404 pages with mockups.
4. API layer and types.
5. Chat: provider, drawer/launcher, `/chat` page, all states (loading, error/retry, empty, escalation).
6. Accessibility pass, responsive pass, and README for the frontend (how to run, env vars, how it talks to the backend).

## ACCEPTANCE CHECKLIST (verify before finishing)

- [ ] Palette uses `#790D16`, `#E5D3AF`, `#F5EFE1`, `#AEC4D4` as the brand colors; all text meets WCAG AA.
- [ ] Pricing numbers, limits, and features match the handoff exactly; no invented discounts or claims.
- [ ] Opening the site, a visitor understands the product within a few seconds.
- [ ] Chat starts without any manual thread ID; the same thread ID is reused for every message and survives route changes; "New conversation" creates a new one.
- [ ] `POST /api/v1/chat` receives `{ thread_id, message }` exactly.
- [ ] `COMPLETED` renders as an assistant message; `INTERRUPTED` renders the amber "Human review required" card (not an error) and the composer stays enabled.
- [ ] Loading, empty, retry (no duplicate message, draft preserved), timeout, 4xx, 5xx, and malformed-response states all work.
- [ ] Enter sends, Shift+Enter newlines, send disabled when empty or in flight.
- [ ] Works on mobile (full-screen chat sheet) and desktop.
- [ ] No secrets, stack traces, or raw errors reach the UI; the approve-escalation action is not exposed publicly.

Start with Phase 1 now. If any requirement is ambiguous, make the most reasonable assumption, note it in one line, and keep going rather than stopping to ask.
