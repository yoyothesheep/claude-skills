# Generic LLM & Probabilistic System Failure Archetypes

This reference documents universal failure modes inherent to probabilistic models (LLMs, vision models, classifiers, embeddings, audio transcription). It is domain-agnostic and applies to any AI-powered software feature.

---

## 1. Structural & Syntactic Failures

### 1.1 Schema Conformance Failure
* **Failure Mode:** Model returns malformed JSON, unclosed quotes, markdown fences surrounding JSON, or violates schema types (e.g. returning a string instead of an array).
* **Impact:** Downstream parsers crash, 500 internal server errors, blank UI states.
* **Mitigations:** Structured output APIs (JSON schema enforcement), defensive JSON repair parsers, fallback retries.

### 1.2 Key / Field Hallucination & Drift
* **Failure Mode:** Model renames keys (e.g. `items` instead of `elements`), invents non-existent properties, or omits mandatory keys.
* **Impact:** Silent data loss, frontend `undefined` errors.
* **Mitigations:** Strict schema validation with Pydantic/Zod, rejecting extra fields or normalizing common aliases.

---

## 2. Generative & Grounding Failures

### 2.1 Pure Hallucination (Unbacked Generation)
* **Failure Mode:** Model generates facts, URLs, entity IDs, or numbers not present in the input context to satisfy an answer.
* **Impact:** False information shown to user with high presentation polish.
* **Mitigations:** Grounding verification pass, quoting source spans, highlighting confidence.

### 2.2 Omission & Attention Degradation
* **Failure Mode:** In long or dense inputs, model misses items in the middle ("lost in the middle" phenomenon) or drops trailing list items.
* **Impact:** Incomplete extractions or partial answers without warning.
* **Mitigations:** Chunked processing, count reconciliation (prompting model to count items first), two-pass verification.

### 2.3 Context Truncation (Token Boundary Exhaustion)
* **Failure Mode:** Output cuts off mid-sentence or mid-JSON because the maximum generation token limit is reached.
* **Impact:** Incomplete payload, parsing syntax error.
* **Mitigations:** Higher token limits, streaming continuation tokens, compact schema representations.

---

## 3. Classification & Decision Failures

### 3.1 False Positive (Noise as Signal)
* **Failure Mode:** Irrelevant, decorative, or accidental input is classified as a target domain entity.
* **Impact:** Junk records created, user annoyance.
* **Mitigations:** Strict relevance gates, negative few-shot examples, confidence score thresholds.

### 3.2 False Negative (Signal as Noise)
* **Failure Mode:** Valid, but non-standard or informal input is rejected as invalid/unsupported.
* **Impact:** User blocked from completing intended task.
* **Mitigations:** Human override escape hatches ("Treat as valid anyway"), graceful fallback paths.

### 3.3 Confidence Miscalibration
* **Failure Mode:** Model asserts an incorrect classification with 0.99 confidence, or hedges on an obvious classification with low confidence.
* **Impact:** Wrong automated routing, unneeded human review friction.
* **Mitigations:** Calibration curves, temperature tuning, ensemble agreement checks.

---

## 4. Repetition & Contextual Artifacts

### 4.1 Loop & Repetition Degeneration
* **Failure Mode:** Model enters an infinite generative loop repeating the same phrase, bullet point, or paragraph.
* **Impact:** Token exhaustion, garbled output.
* **Mitigations:** Repetition penalty, deduplication post-processing.

### 4.2 Verbatim Duplicate Extraction
* **Failure Mode:** When input contains repeated content (e.g. overlapping visual steps, repeated subtitles, scroll overlap), model includes redundant steps multiple times.
* **Impact:** Bloated, confusing instructions for the user.
* **Mitigations:** Sequence deduplication heuristics (Jaccard similarity / Levenshtein distance on adjacent items).

---

## 5. Security & System Failures

### 5.1 False Refusal (Over-Safety)
* **Failure Mode:** Benign text containing benign trigger words (e.g. "knife", "cocktail", "alcohol", "burn") triggers model moderation filters and refuses execution.
* **Impact:** Workflow broken for valid user tasks.
* **Mitigations:** System prompt context framing, using lighter models for non-adversarial internal pipelines.

### 5.2 System Prompt Leakage & Indirect Injection
* **Failure Mode:** Text within user inputs contains instructions (e.g. "Ignore previous instructions and do X") that derail extraction.
* **Impact:** Hijacked task, data extraction failure.
* **Mitigations:** Clear delimiter separation (XML/Markdown fences), input sanitization, read-only extraction prompts.

### 5.3 Infrastructure Degradation
* **Failure Mode:** Provider API rate limits (HTTP 429), gateway timeouts (HTTP 504), service outages (HTTP 503).
* **Impact:** Latency spikes, broken user experience.
* **Mitigations:** Exponential backoff jitter, circuit breakers, fallback model providers.
