# Practice cases

Use these prompts to try the skill and review its outputs. They are qualitative scenarios, not a published benchmark or proof of universal language support.

## Positive cases

| Prompt | Evidence of a good result |
| --- | --- |
| Add Chinese walkthrough comments to this Java batching method. Show why clearing the list does not erase previous results. | One fixture throughout; exact batches; explains snapshot versus alias; no logic change. |
| Annotate this Python sliding-window function in English for a data engineer who is new to this implementation. | Tracks append, eviction, total, and first output; respects positive-width assumptions; no unnecessary syntax lesson. |
| Annotate this JavaScript function in English. Explain Promise.all ordering. | English prose; exact identifiers retained; distinguishes result order and completion order; no invented cancellation. |
| 用中文注释讲解这个 SQL 查询，并展示各阶段的示例行。 | Shows rows before/after ranking/filtering; recognizes unspecified order or ties if present; no unrequested query changes. |
| Add an example-based walkthrough to this Rust iterator pipeline. | Correct lazy/eager boundaries and ownership; no imaginary mutable execution sequence; native comments. |
| Improve the existing example comments without making this method longer unnecessarily. | Updates stale examples; does not duplicate the fixture or chase a line-count target. |

## Boundary and adversarial cases

| Prompt/context | Required behavior |
| --- | --- |
| Explain this function; do not edit any files. | Returns an annotated excerpt; no filesystem mutation. |
| Add inline comments to strict JSON. | Preserves valid JSON; uses an excerpt/companion explanation instead. |
| Repository requires English comments; user has not requested a language. | Uses English comments even if the conversation is in another language. |
| User explicitly requests Chinese comments under instructions that permit that override. | Uses Chinese prose; preserves code identifiers and literals. |
| Provided fixture contradicts the implementation. | Corrects the explanation and identifies the mismatch; does not change logic to manufacture the requested result. |
| Comment says the method retries; no retry exists in the implementation. | Inspects helper/caller as needed and corrects the claim; no fabricated resilience. |
| Generator, optimizer hint, build tag, type directive, docstring, or line-continuation hazard. | Preserves semantics and placement; uses a safe comment form or explains the limitation. |
| User asks for a comment-only change in a file with existing local edits. | Establishes the current baseline; preserves unrelated edits; verifies only the requested change. |

## Review rubric

Score each item as met, partially met, or unmet; support the rating with an actual excerpt or check result.

1. Grounding: claims match implementation, configuration, and helper behavior.
2. Continuity: the same fixture leads coherently to the stated output.
3. State clarity: difficult transitions show relevant before/after values and reasons.
4. Audience fit: explanation depth and natural language match the request.
5. Preservation: changes stay within scope and respect language/tool directives.
6. Verification honesty: executed checks and manual reasoning are clearly distinguished.

When an item fails, revise that part of the skill or example and rerun the affected case. Do not equate a structurally valid SKILL.md with good teaching performance.
