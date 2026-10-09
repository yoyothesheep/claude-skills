# Scenario Matrix Template

Use this template to present the exhaustive scenario mapping for any feature.

---

## Feature: [Feature Name]
**Scope:** [Brief description of the workflow or system boundary]
**Primary Actors:** [User roles, external systems]

---

## 1. Scenario Summary Matrix

| ID | Dimension | Scenario Title | Input / State Condition | Expected Behavior | Failure Mode / Risk | Test Target |
|:---|:---|:---|:---|:---|:---|:---|
| **S01** | Actor/Auth | Unauthenticated ingress | User accesses flow while logged out | Redirect to login with return_to parameter | Silent 403 or blank state | E2E |
| **S02** | Flow Path | Happy path (single item) | Standard nominal payload submitted | Immediate success with feedback | Stuck loading spinner | E2E |
| **S03** | Flow Path | Cancellation mid-stream | User dismisses flow midway | State cleanly discarded without residue | Orphaned draft records | Unit |
| **S04** | Data Volume | Cold start (Zero state) | Collection has 0 items | Welcoming empty state with clear CTA | Broken layout / null deref | E2E |
| **S05** | Data Volume | Extreme scale (Bulk) | 20+ items submitted simultaneously | Chunked processing with progress meter | Gateway 504 timeout | Integration |
| **S06** | Input Boundary | Degraded / dirty input | Low-res or partially obstructed input | Graceful parse with low-confidence flag | Hard crash or crash loop | Unit |
| **S07** | Generic AI | Schema compliance failure | LLM returns malformed JSON response | Parser repairs or retries once cleanly | Uncaught syntax error | Unit |
| **S08** | Generic AI | Repetition / Overlap | Sequential inputs with redundant overlap | Deduplication filter purges duplicates | Repeated instructions | Eval/Unit |
| **S09** | Domain AI | [From Project Config] | [Specific domain condition] | [Domain expected outcome] | [Domain risk] | Eval/Unit |
| **S10** | Human Override| 1-tap manual correction | User overrides AI classification | Immediate state update, persists on save | Reverts to AI guess | E2E |
| **S11** | Network | Flaky connection | Network drops mid-submission | Client caches and prompts retry button | Duplicate creation | Integration |
| **S12** | Platform | Mobile viewport & touch | Single-shot mobile file input | Sequential staging tray flow | Form closes prematurely | E2E |

---

## 2. In-Depth Scenario Specifications

### [S_ID]: [Scenario Title]
* **Pre-conditions:** [System and user state before trigger]
* **Trigger:** [Exact user action or external event]
* **System Execution:** [What the frontend, backend, and AI pipeline execute]
* **Post-conditions:** [Expected database, UI, and external state]
* **Human Recovery Path:** [How the user recovers if something goes wrong]
* **Verification Plan:** [Automated test mapping: unit, integration, or eval fixture]
