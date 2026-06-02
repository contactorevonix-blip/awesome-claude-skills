---
name: greenfield-project-setup
description: Full senior engineer workflow for new projects from scratch — discovery, stack selection, architecture decisions, scaffolding, tooling configuration, and CI/CD setup.
---

# Greenfield Project Setup

A complete workflow for engineers starting a new project from zero. Goes beyond generating folders — it makes the right decisions upfront: what to build, how to structure it, which tools to use, and how to keep it maintainable as it grows.

## When to Use This Skill

- Starting a new project with no existing code
- Setting up a repository that a team will work on
- Evaluating which tech stack fits a new product requirement
- Needing a production-ready baseline with CI/CD, testing, and documentation from day one
- Ensuring mandatory files and security baselines are in place before any feature work
- Onboarding a new codebase with consistent engineering standards

## What This Skill Does

1. **Runs Discovery**: Asks the right questions to understand what is being built, who uses it, and what the constraints are — before touching any code.
2. **Selects the Stack**: Recommends a tech stack based on requirements, team familiarity, and scale — with reasoning, not opinion.
3. **Designs the Architecture**: Produces a high-level architectural decision (monolith, service, library, CLI, pipeline, etc.) and explains the trade-offs.
4. **Scaffolds the Structure**: Creates the full directory structure with all mandatory files and folders in place, with real content — not placeholders.
5. **Configures Tooling**: Sets up linters, formatters, test frameworks, and pre-commit hooks appropriate to the chosen stack.
6. **Sets up CI/CD**: Generates a working GitHub Actions pipeline that runs tests and linting on every pull request.
7. **Produces a Handoff Summary**: Delivers a clear summary of every decision made, every file created, and what to do next.

## How to Use

### Quick Start

```
Set up a new TypeScript REST API project called "billing-service"
```

### Full Workflow

```
I need to start a new project. It's a web app for managing subscriptions —
users can sign up, choose a plan, and get invoiced monthly.
Team of 3 engineers, we know TypeScript well. Help me set it up properly.
```

### With Constraints

```
New Python data pipeline project. Must run on AWS Lambda,
process CSV files, output to S3. No Docker. Set it up from scratch.
```

## Instructions

Follow these phases in order. Do not skip phases or merge them. After each phase, summarize what was decided and confirm with the user before proceeding to the next.

---

### Phase 1: Discovery

Ask these questions before doing anything else. Do not guess or assume.

**Required answers:**

- What are we building? (API, web app, CLI, library, data pipeline, ML service, monorepo)
- Who will use it? (internal team, external users, machines/other services)
- What is the expected scale? (prototype/MVP, production for hundreds, production for millions)
- What languages or frameworks does the team know well?
- Are there infrastructure constraints? (cloud provider, no Docker, specific runtime, serverless)
- Is this solo or a team project? If team, how many engineers?

**Optional but high-value:**

- Any existing services this must integrate with?
- Any compliance or security requirements? (GDPR, SOC2, HIPAA)
- Expected lifetime of the project? (throwaway prototype vs. 5-year product)

Summarize answers in a "Project Brief" block before moving to Phase 2:

```
Project Brief
─────────────
Type: [what is being built]
Purpose: [one sentence]
Users: [who uses it]
Scale: [MVP / production / unknown]
Stack preference: [what the team knows]
Infrastructure: [constraints if any]
Team: [solo / N engineers]
Compliance: [none / GDPR / SOC2 / etc.]
```

---

### Phase 2: Stack Decision

Based on the discovery answers, recommend a stack. Structure the recommendation as:

```
## Recommended Stack

Runtime:           [e.g., Node.js 22 LTS]
Language:          [e.g., TypeScript 5.x]
Framework:         [e.g., Fastify]
Database:          [e.g., PostgreSQL via Prisma]
Testing:           [e.g., Vitest + Supertest]
Linting:           [e.g., ESLint flat config + Prettier]
Container:         [e.g., Docker + docker-compose]
CI:                [e.g., GitHub Actions]

Why this stack:
- [Reason tied to a specific discovery answer]
- [Reason tied to scale or team familiarity]
- [Reason tied to infrastructure constraint]

Trade-offs accepted:
- [Trade-off 1 and why it is acceptable]
- [Trade-off 2 and why it is acceptable]
```

If the user has a preference that conflicts with their requirements, flag the conflict explicitly and explain the risk. Do not just say yes.

Reference stacks by project type:

**API / Backend service** → Node.js + TypeScript + Fastify or Python + FastAPI
**Full-stack web app** → React + Vite (frontend), Fastify or Express (backend), monorepo if same team owns both
**Data pipeline / ETL** → Python + Pydantic + boto3/psycopg3, plain Python (no framework overhead)
**ML service** → Python + FastAPI (serving) or plain Python (batch), uv for dependencies
**CLI tool** → Go (single binary, fast) or Python + Typer (scripting-friendly)
**Library / SDK** → Match the language of the consumers; minimize dependencies
**Monorepo** → Turborepo (Node) or Pants/Nx (polyglot)

Wait for user confirmation before Phase 3.

---

### Phase 3: Architecture Decision

Produce a one-page architecture decision before creating any files. Include:

1. **Pattern**: Monolith / Modular Monolith / Microservice / Serverless / Library / CLI / ETL Pipeline
2. **Layer structure**: How the code is divided (e.g., routes → controllers → services → repositories)
3. **Key boundaries**: What lives inside this project vs. what is external (other services, third-party APIs)
4. **Data model sketch**: Main entities and their relationships (if applicable)
5. **Security baseline**: How authentication is handled, where secrets live, what is never committed to git

Write this as a short document, not a bullet list. Use plain language. This becomes the `docs/architecture.md` file later.

Wait for user confirmation before Phase 4.

---

### Phase 4: Scaffold Structure

Create the full directory tree. Output it as a visual listing, then create each file with real, working content — not placeholder comments or TODO stubs.

**Mandatory files — no exceptions regardless of stack:**

| File | Purpose |
|------|---------|
| `README.md` | Entry point for every engineer: what it is, how to run it |
| `CLAUDE.md` | Instructions for Claude Code when working in this repo |
| `.gitignore` | Excludes secrets, build artifacts, OS files, dependencies |
| `.env.example` | All required env vars with placeholder values, no real secrets |
| `LICENSE` | Default MIT unless user specifies otherwise |

**Mandatory folders — no exceptions:**

```
src/                  All source code lives here
tests/                All tests, mirroring src/ structure
docs/                 Architecture decisions, API docs, diagrams
scripts/              Utility scripts: migrations, seeds, deploy helpers
.github/
  workflows/
    ci.yml            Runs on every PR: lint + test
```

**Stack-specific mandatory files:**

For Node.js / TypeScript:
```
package.json
tsconfig.json
eslint.config.js      Flat config format (ESLint 9+)
.prettierrc
.nvmrc                Pins Node version (e.g., 22)
```

For Python:
```
pyproject.toml        Project metadata + dependencies (uv or poetry)
ruff.toml             Linting and formatting configuration
pytest.ini            Test configuration and coverage settings
.python-version       Pins Python version (e.g., 3.12)
```

For Go:
```
go.mod
go.sum
.golangci.yml         Linting configuration
Makefile              Common tasks: build, test, lint, run
```

For Monorepo (Node):
```
turbo.json            Build orchestration
package.json          Workspace root with workspaces field
apps/                 Deployable applications
packages/             Shared code (types, utils, config)
```

---

### Phase 5: Tooling Configuration

Configure each tool with production-grade settings. Never use defaults without reviewing them.

**Linter:**
- Enable rules that catch real bugs, not just style
- For TypeScript: `strict: true`, `noUncheckedIndexedAccess: true`, `exactOptionalPropertyTypes: true` in tsconfig
- For Python with ruff: enable rule sets `E`, `W`, `F`, `I`, `N`, `UP`, `S` (security)
- Never disable a rule without a comment explaining why

**Formatter:**
- One configuration, no debate
- TypeScript: Prettier with `singleQuote: true`, `trailingComma: "all"`, `printWidth: 100`, `semi: false`
- Python: ruff format (replaces black, same style)
- Go: gofmt is non-negotiable, already built in

**Test framework:**
- Set coverage threshold: 80% minimum for new projects
- Wire test and coverage commands into `package.json` / `Makefile` / `pyproject.toml`
- Create one real passing test on day one — even if it just imports the main module and asserts it loads

**Pre-commit hooks:**
- Run linter and formatter check on staged files only (fast)
- Block commits that fail lint
- Node: husky + lint-staged
- Python: pre-commit framework with ruff hook

---

### Phase 6: CI/CD Setup

Generate a `.github/workflows/ci.yml` that:

1. Triggers on `push` to `main` and `pull_request` targeting `main`
2. Runs on `ubuntu-latest`
3. Steps in order:
   - Checkout code (`actions/checkout@v4`)
   - Setup runtime with version pinned from `.nvmrc` / `.python-version` / `go.mod`
   - Install dependencies with cache enabled
   - Run linter
   - Run formatter check (fails if code is not formatted)
   - Run tests with coverage report
   - Build step if the project produces a compiled artifact

Rules:
- Pin all action versions (e.g., `actions/setup-node@v4`). Never use `@latest`.
- Cache dependency installation (npm cache, pip cache, Go module cache)
- Fail fast: if lint fails, do not run tests. Surface the first error clearly.

---

### Phase 7: Documentation

Generate real content for each documentation file. No stubs, no TODOs.

**README.md must include:**
- Project name and one-line description
- Prerequisites with exact versions
- How to run locally — copy-pasteable commands only
- How to run tests
- Environment variables section (reference `.env.example`)
- Top-level project structure as a directory tree
- Contributing section pointing to how to open a PR

**CLAUDE.md must include:**
- What this project does (one paragraph, plain language)
- How to run tests (exact command)
- How to run the linter (exact command)
- Key architectural decisions (2-3 bullet points from Phase 3)
- Files or folders Claude should not modify without asking
- Project-specific conventions (naming patterns, import style, etc.)

**docs/architecture.md must include:**
- The architecture decision from Phase 3 written as a permanent record
- Date of the decision
- Context (why a decision was needed), Decision (what was chosen), Consequences (what this means going forward) — ADR format

---

### Phase 8: Handoff Summary

After all phases are complete, produce a summary in this format:

```
## Project Setup Complete

Project:    [name]
Stack:      [brief — e.g., TypeScript + Fastify + PostgreSQL]
Created:    [N files across N directories]

### Decisions made and why
- [Decision 1]: [reason tied to discovery]
- [Decision 2]: [reason tied to discovery]
- [Decision 3]: [reason tied to discovery]

### What to do next
1. Copy .env.example to .env and fill in the values
2. Run: [install command]
3. Run: [test command] — expect N passing
4. Push to GitHub and verify the CI pipeline goes green

### Assumptions made
- [Any assumption the user should verify before proceeding]
```

---

## Mandatory Files Reference

Every project, regardless of stack, needs these from day one:

| File | Why it cannot be skipped |
|------|--------------------------|
| `README.md` | Without it, no one knows how to run the project |
| `CLAUDE.md` | Claude makes wrong assumptions without project context |
| `.gitignore` | One accidental commit of `.env` is permanent in git history |
| `.env.example` | New engineers waste hours finding out which env vars exist |
| `LICENSE` | Code without a license is legally ambiguous even internally |
| `tests/` | Projects without tests from day one rarely add them later |
| `.github/workflows/ci.yml` | Without CI, broken code reaches main with no automated catch |

---

## Examples

### Example 1: TypeScript REST API

**User**: "New project — a REST API for managing team subscriptions. TypeScript, small team of 2, deploy to Railway."

**Phase 1 — Project Brief:**
```
Type:           REST API
Purpose:        Subscription management (plans, users, invoices)
Users:          Internal dashboard + mobile app (machine-to-machine)
Scale:          MVP, under 500 users initially
Stack:          TypeScript (team knows it well)
Infrastructure: Railway (Node.js containers, PostgreSQL add-on available)
Team:           2 engineers
Compliance:     None specified
```

**Phase 2 — Stack:**
```
Runtime:    Node.js 22 LTS
Language:   TypeScript 5.x (strict mode)
Framework:  Fastify (lower overhead than Express, better TS support out of the box)
ORM:        Prisma (type-safe queries, migration tooling, Railway PostgreSQL compatible)
Testing:    Vitest + Supertest
Linting:    ESLint flat config + Prettier
CI:         GitHub Actions
Container:  Docker + docker-compose (local dev only, Railway handles production)
```

**Phase 4 — Directory structure:**
```
billing-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── architecture.md
├── prisma/
│   └── schema.prisma
├── scripts/
│   └── seed.ts
├── src/
│   ├── config/
│   │   └── env.ts
│   ├── plugins/
│   │   └── db.ts
│   ├── routes/
│   │   ├── subscriptions.ts
│   │   └── health.ts
│   └── server.ts
├── tests/
│   ├── routes/
│   │   └── subscriptions.test.ts
│   └── setup.ts
├── .env.example
├── .gitignore
├── .nvmrc
├── .prettierrc
├── CLAUDE.md
├── LICENSE
├── README.md
├── docker-compose.yml
├── eslint.config.js
├── package.json
└── tsconfig.json
```

---

### Example 2: Python Data Pipeline on AWS Lambda

**User**: "Python pipeline that reads CSVs from S3, validates them, and writes results to PostgreSQL. Runs on AWS Lambda."

**Stack selected:**
```
Runtime:    Python 3.12
Packages:   uv (fast, lockfile-based)
Framework:  None — plain Python (Lambda cold start matters)
AWS SDK:    boto3
DB client:  psycopg3
Validation: Pydantic v2
Testing:    pytest + moto (mocks S3 without hitting real AWS)
Linting:    ruff
CI:         GitHub Actions
```

**Key architectural decision:** No Docker (Lambda runtime constraint). Local development uses moto to mock S3 — no LocalStack dependency, no Docker, no extra tooling. The Lambda handler is the entry point and must stay thin; all business logic lives in `src/pipeline/`. Tests never hit real AWS in CI.

**Structure:**
```
csv-pipeline/
├── .github/workflows/ci.yml
├── docs/architecture.md
├── scripts/invoke_local.py
├── src/
│   ├── pipeline/
│   │   ├── reader.py       # S3 CSV reading
│   │   ├── validator.py    # Pydantic models
│   │   └── writer.py       # PostgreSQL writes
│   └── handler.py          # Lambda entry point (thin)
├── tests/
│   ├── test_reader.py
│   ├── test_validator.py
│   └── conftest.py
├── .env.example
├── .gitignore
├── .python-version
├── CLAUDE.md
├── LICENSE
├── README.md
├── pyproject.toml
├── pytest.ini
└── ruff.toml
```

---

### Example 3: Full-Stack Monorepo

**User**: "SaaS analytics dashboard. React frontend, Node backend, same repo. Small startup, need to move fast."

**Architecture decision:** Monorepo with two deployable apps: `apps/web` (React + Vite, deploy to Vercel) and `apps/api` (Fastify, deploy to Railway). Shared TypeScript types in `packages/types` — imported by both apps, never duplicated. Turborepo orchestrates builds. CI runs lint and tests for the entire repo on every PR but only rebuilds what changed.

**Top-level structure:**
```
analytics-dashboard/
├── apps/
│   ├── api/                # Fastify REST API
│   └── web/                # React + Vite SPA
├── packages/
│   └── types/              # Shared TypeScript interfaces
├── .github/
│   └── workflows/
│       └── ci.yml
├── CLAUDE.md
├── README.md
├── package.json            # Workspace root
└── turbo.json
```

---

## Tips

- Never start with code. Discovery first, always. The worst greenfield projects fail because requirements were assumed rather than asked.
- `.env.example` is not optional. Every missing env var is a future production outage or a wasted hour for the next engineer.
- Write `CLAUDE.md` on day one and update it whenever the architecture changes. It pays dividends immediately.
- Pin versions everywhere — Node in `.nvmrc`, Python in `.python-version`, GitHub Actions by SHA or tag. Floating versions cause "works on my machine" failures.
- One passing test on day one creates a green baseline. A test added on day 100 is paying off technical debt.
- The architecture document in `docs/` is a gift to your future self. Write it while the decisions are still fresh and the reasoning is clear.
- Keep entry points thin (`server.ts`, `handler.py`, `main.go`). Business logic in entry points is untestable.

## Common Mistakes

- **Skipping `.gitignore` before the first commit**: One accidental commit of `node_modules` or `.env` is permanent in git history.
- **Empty or placeholder README**: "TODO: add description" means the next engineer starts from zero. Write it now.
- **No CI from day one**: The first PR that breaks tests with no CI is caught by nobody.
- **Business logic in the entry point**: Makes testing impossible without starting the whole server.
- **Committing `.env`**: Never. Use `.env.example` for documentation, `.env` for local secrets only.
- **Defaulting to the most popular framework**: Match the framework to the requirements and the team's experience, not to what is trending.
- **No `CLAUDE.md`**: Claude Code will make architectural assumptions that contradict your decisions. Write it explicitly.
