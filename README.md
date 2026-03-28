---
title: SupportDesk OpenEnv
emoji: "🤖"
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# SupportDesk OpenEnv

SupportDesk OpenEnv is a real-world customer support operations environment built for OpenEnv-style agent training and evaluation. Instead of a toy game, the agent must inspect support tickets, consult policy knowledge, assign urgency, route ownership, write a customer reply, and resolve the case correctly.

## Why this environment

This environment models work that real support teams do every day:

- Billing dispute handling
- Security incident escalation
- Logistics recovery for VIP customers

The environment is deterministic and reproducible, but still requires multi-step reasoning across ticket facts, contract notes, recent events, and policy snippets.

## Tasks

- `billing_duplicate_charge` (`easy`): identify a duplicate annual charge, route to billing, approve the refund, and communicate the settlement window.
- `security_compromised_account` (`medium`): triage a likely account takeover, escalate to Security Ops, and communicate containment steps.
- `logistics_missing_order_vip` (`hard`): resolve a missing event-critical shipment, dispatch a replacement, and apply a shipping credit.

## Action Space

The agent interacts through typed actions:

- `open_ticket`
- `search_policy`
- `set_priority`
- `route_ticket`
- `send_reply`
- `resolve_ticket`

You can inspect the machine-readable schema at `GET /action_schema`.

## Observation Space

Each observation contains:

- Task instruction
- Available ticket IDs
- The active ticket once opened
- Latest search results from the policy base
- Recent action log
- Partial score so far
- Remaining step budget

## Reward Design

The reward function emits partial progress instead of a sparse pass/fail signal:

- `0.05` for opening the correct ticket
- `0.10` for consulting required policy knowledge
- `0.15` for correct priority
- `0.20` for correct team routing
- `0.20` for reply coverage of required policy details
- `0.30` for the correct final resolution

Total score is capped at `1.0`, and `/grader` returns a deterministic component breakdown.

## Endpoints

- `POST /reset`
- `POST /step`
- `GET /state/{episode_id}`
- `GET /tasks`
- `POST /grader`
- `POST /baseline`
- `GET /health`
- `GET /action_schema`

## Local setup

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
uvicorn main:app --reload --host 0.0.0.0 --port 7860
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
uvicorn main:app --reload --host 0.0.0.0 --port 7860
```

## Baseline

Run the deterministic baseline agent:

```bash
python baseline.py
```

It executes the built-in heuristic policy against all 3 tasks and prints reproducible scores.

## Hugging Face Spaces deployment

This repository includes a Dockerfile that launches the environment with Uvicorn on port `7860`, which is suitable for Spaces container deployment.
