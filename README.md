# GitLab AI Content & Documentation Engine

An AI-powered content production platform that turns technical inputs — code changes, product briefs, API specs, and release notes — into review-ready documentation, release notes, and developer blogs, through a governed multi-agent workflow with human approval at every stage.

<!--
  📸 SCREENSHOT: add a hero screenshot or short GIF of the app here
  (recommended: the home page or the dashboard). Save it to
  docs/screenshots/hero.png and reference it like this:
  ![App overview](docs/screenshots/hero.png)
-->

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Folder Structure](#folder-structure)
- [Content Workflow](#content-workflow)
- [User Roles](#user-roles)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Deployment](#deployment)
- [Team](#team)

---

## Overview

Product releases move faster than documentation can keep up. The **AI Content & Documentation Engine** closes that gap: a writer submits a content request, a five-agent AI crew drafts and refines it, and the content moves through a controlled review chain — **Technical Reviewer → Doc Lead → Admin** — before it's published. Every step is logged, every draft is versioned, and nothing goes live without a human sign-off.

## Key Features

- **Multi-agent AI drafting** — five specialized CrewAI agents (context reading, writing, technical review, tone optimization, publishing prep) turn raw technical input into a structured draft
- **Source-grounded content** — drafts carry `source_references` back to the material they were generated from
- **Role-based review workflow** — Writer → Technical Reviewer → Doc Lead → Admin, each with scoped permissions
- **Version history** — every regenerated draft is saved, nothing is overwritten
- **Retrieval-augmented context** — a Chroma vector store surfaces relevant prior docs and style guidance before drafting starts
- **Audit logging** — every job creation, review action, and publish event is recorded
- **Published document viewer** — a clean, read-only page for anyone to read a published document
- **Admin dashboard** — pipeline health, pending reviews, and one-click publish

## Screenshots

<!--
  📸 ADD YOUR SCREENSHOTS HERE. Suggested shots to capture, in order:
    1. Home / landing page
    2. Login page
    3. Content intake form (Generate page)
    4. Draft editor with a generated draft
    5. Review panel (Accept / Request Revision / Reject)
    6. Admin dashboard ("Ready to Publish" section)
    7. Published document viewer page

  Save files under docs/screenshots/ using the names below, and these
  links will render automatically once the images exist.
-->

| | |
|---|---|
| **Home page** | ![Home page](docs/screenshots/home.png) |
| **Content intake** | ![Content intake](docs/screenshots/generate.png) |
| **Draft & review** | ![Draft review](docs/screenshots/draft-review.png) |
| **Admin dashboard** | ![Admin dashboard](docs/screenshots/dashboard.png) |
| **Published viewer** | ![Published viewer](docs/screenshots/published.png) |

> **Where to add screenshots:** create a `docs/screenshots/` folder in the repository root (if it doesn't already exist) and drop your `.png`/`.jpg` files there using the filenames above. GitHub/GitLab renders them automatically wherever they're referenced in this file — no extra setup needed.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, React 18, Tailwind CSS, Framer Motion |
| Backend / API | FastAPI, Uvicorn, Pydantic |
| Agent Orchestration | CrewAI |
| LLM | Gemini API |
| Vector Retrieval | ChromaDB |
| Database | PostgreSQL (via Supabase) / SQLAlchemy |
| Auth | Custom email/password + role-based access |
| Integrations | GitLab API (`python-gitlab`) |

## Folder Structure

```
main/
├── Backend/
│   ├── main.py                # FastAPI app — all API routes
│   ├── models.py               # Pydantic request/response schemas
│   ├── agents/
│   │   └── crew.py             # CrewAI 5-agent content workflow
│   ├── auth/                   # Login, signup, verification, sessions
│   ├── database/
│   │   ├── crud.py             # Job/user CRUD helpers
│   │   ├── models_db.py        # SQLAlchemy models
│   │   └── audit_log.py        # Structured audit logging
│   ├── retrieval/
│   │   ├── chroma_store.py     # Vector store setup
│   │   └── ingest_knowledge.py # Load style guides/templates into Chroma
│   └── services/
│       ├── context_builder.py  # Builds context packs for agents
│       └── gitlab_service.py   # GitLab repository integration
│
├── Frontend/
│   ├── app/                    # Next.js App Router pages
│   │   ├── login/ signup/      # Auth pages
│   │   ├── generate/           # Content intake form
│   │   ├── drafts/             # Draft list + review workspace
│   │   ├── documents/[status]/ # Documents filtered by status
│   │   ├── published/[job_id]/ # Read-only published document viewer
│   │   └── dashboard/          # Role-specific dashboards
│   └── components/
│       ├── home/                # Landing page sections
│       ├── drafts/               # Draft editor, review panel
│       ├── dashboard/ analytics/ # Dashboard widgets, charts
│       └── layout/               # Navbar, shared layout
│
├── data/
│   ├── sample_inputs/          # Example technical inputs
│   ├── sample_docs/             # Example existing docs (for retrieval)
│   ├── style_guides/            # GitLab voice/style guidance
│   └── content_templates/       # Reusable content templates
│
├── docs/
│   ├── architecture.md
│   ├── api_documentation.md
│   ├── workflow_states.md
│   ├── demo_script.md
│   └── screenshots/             # 📸 add screenshots here
│
├── tests/
│   ├── functional_tests/
│   ├── ai_output_tests/
│   └── edge_cases/
│
└── deployment/
    ├── vercel_notes.md
    ├── backend_deployment.md
    └── environment_setup.md
```

## Content Workflow

A content job moves through the following statuses:

```
intake → drafting → ready_for_human_review → doc_lead_review → approved → published
                          │                        │
                          ▼                        ▼
                        failed                   failed   (on reject)
                          │                        │
                          ▼                        ▼
                      drafting                  drafting   (on request_revision)
```

| Status | Meaning | Who acts next |
|---|---|---|
| `intake` | Job created, AI not yet run | — |
| `drafting` | AI agents generating the draft | — |
| `ready_for_human_review` | Draft ready | Technical Reviewer |
| `doc_lead_review` | Passed technical review | Doc Lead |
| `approved` | Doc Lead accepted | Admin |
| `published` | Live and readable | — |
| `failed` | Rejected, or the AI workflow errored | Writer (resubmits) |

See [`docs/workflow_states.md`](docs/workflow_states.md) for the full reference.

## User Roles

| Role | Can do |
|---|---|
| **Writer** | Create content jobs, run the AI workflow, submit drafts for review |
| **Technical Reviewer** | Accept / reject / request revision on drafts in `ready_for_human_review` |
| **Doc Lead** | Accept / reject / request revision on drafts in `doc_lead_review` |
| **Admin** | Publish approved documents, delete jobs, manage users, view all analytics |

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A PostgreSQL database (e.g. a free [Supabase](https://supabase.com) project)
- A [Gemini API key](https://aistudio.google.com/app/apikey)

### 1. Backend setup

```bash
cd Backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then fill in GEMINI_API_KEY and DATABASE_URL

uvicorn main:app --reload
```

Backend runs at `http://127.0.0.1:8000` — visit `/docs` for the interactive API explorer.

### 2. Frontend setup

```bash
cd Frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`.

## Environment Variables

Set these in `Backend/.env` (see `Backend/.env.example`):

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Gemini API key used by the CrewAI agents |
| `GOOGLE_API_KEY` | Same key, some libraries read this name instead |
| `DATABASE_URL` | PostgreSQL connection string (Supabase: Project Settings → Database → Connection string) |
| `GITLAB_URL` | Base URL of your GitLab instance, used by the GitLab integration |
| `GITLAB_TOKEN` | GitLab personal access token |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USERNAME` / `SMTP_PASSWORD` / `SMTP_FROM` | SMTP credentials used to send signup verification and password-reset emails |
| `FRONTEND_ORIGINS` | Comma-separated list of allowed frontend origins for CORS (e.g. your Vercel URL). Defaults to `http://localhost:3000,http://127.0.0.1:3000` if unset |

<!--
  🔗 DEPLOYMENT: once deployed, add the live links here:
  - Frontend: https://your-app.vercel.app
  - Backend:  https://your-api.onrender.com
-->

## API Reference

| Endpoint | Purpose |
|---|---|
| `POST /api/content-jobs` | Create a new content job |
| `POST /api/agent-workflow/run` | Run the 5-agent drafting workflow |
| `GET /api/content-jobs/{job_id}` | Fetch a job's full state |
| `POST /api/drafts/{job_id}/review` | Accept / reject / request revision |
| `POST /api/publish/export` | Publish an approved document (Admin only) |
| `GET /api/metrics` | Pipeline throughput and status counts |
| `GET /api/dashboard` | Role-specific dashboard data |

Full request/response shapes are in [`docs/api_documentation.md`](docs/api_documentation.md) and the live `/docs` explorer.

## Testing

```bash
cd tests
pytest functional_tests/
pytest ai_output_tests/
pytest edge_cases/
```

## Deployment

- **Frontend** — deploy `Frontend/` to [Vercel](https://vercel.com) (see [`deployment/vercel_notes.md`](deployment/vercel_notes.md))
- **Backend** — deploy `Backend/` to [Render](https://render.com) or [Railway](https://railway.app) (see [`deployment/backend_deployment.md`](deployment/backend_deployment.md))
- **Database** — hosted on [Supabase](https://supabase.com)

<!--
  🎥 DEMO VIDEO: once recorded, add the Google Drive link here
  (make sure sharing is set to "Anyone with the link can view").
-->

## Team

<!--
  👥 TEAM: list each teammate and what they owned, e.g.
  | Name | Contribution |
  |---|---|
  | ... | Backend & AI workflow |
  | ... | Frontend & design |
-->

| Name | Contribution |
|---|---|
| _Add name_ | _Add contribution_ |
| _Add name_ | _Add contribution_ |

---

<p align="center">Built for GitLab's release-driven documentation workflow.</p>