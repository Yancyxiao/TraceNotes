# Design notes and attribution

Reviewed on 2026-10-20. This is a comparison of the linked source files, not an exhaustive survey or a claim of originality for educational code comments.

## Positioning

TraceNotes helps a reader reconstruct an implementation by following one fixture through decisive operations. Its unit of explanation is the meaningful state transition or value transformation. A comment should answer a specific learning question at the relevant code location.

Programming language, natural language, general technical experience, and familiarity with the current subsystem are separate dimensions. None implies the others.

## What we learned

| Source | Adopted idea | Adaptation in TraceNotes |
| --- | --- | --- |
| [add-educational-comments](https://github.com/github/awesome-copilot/blob/main/skills/add-educational-comments/SKILL.md) | Distinguish general knowledge and language/platform familiarity. | Consider those dimensions separately; infer them instead of requiring a questionnaire. |
| Same source | Configure depth and connect related explanations. | Accept plain-language preferences and stable example/step labels when useful; do not embed fragile source line numbers. |
| Same source | Preserve encoding, indentation, newlines, and build correctness. | Keep these constraints, including semantically active comments and directives. |
| [code-explainer](https://github.com/mohitagw15856/pm-claude-skills/blob/main/skills/code-explainer/SKILL.md) | Begin with a stand-alone one-sentence purpose. | Put the purpose near the relevant code or before an explanation-only excerpt. |
| Same source | Explain steps and non-obvious behavior rather than restating syntax. | Attach concrete states to meaningful operations; explain relevant side effects, boundaries, dependencies, and failure propagation. |
| Same source | Surface concrete problems found while reading. | Report the trigger, evidence, consequence, and suggested correction separately; do not silently fix behavior in an annotation-only task. |

## Deliberate differences

- No line-count growth target. More comments are useful only when they improve understanding.
- No ASCII-only prose restriction. Preserve encoding while supporting the reader's natural language.
- No unconditional English output. Repository rules and explicit requests govern the comment language under the applicable instruction hierarchy.
- No forced certainty for a fragment. Explain visible behavior and identify missing context rather than inventing helper outputs.
- No automatic refactor or full audit. Concrete findings are reported within the actual evidence and task scope.
- No required tool integration. Serena or another symbol tool may help, but ordinary source navigation is sufficient.

## Workflow contract

The main fixture remains consistent across the walkthrough. Inputs, assumptions, units, aliases, and expected outputs must agree. Edge cases are separate examples. For concurrent code, distinguish guaranteed ordering from an illustrative schedule. For declarative code, trace value/row transformations without inventing physical execution order.

Annotation-only changes preserve executable behavior and unrelated local edits. Verification checks both the explanation and the patch. Executed checks and manual traces must not be described interchangeably.

## Packaging references

The README organization draws on the visible patterns in [anthropics/skills](https://github.com/anthropics/skills), [obra/superpowers](https://github.com/obra/superpowers), and [vercel-labs/skills](https://github.com/vercel-labs/skills): clear purpose, installation, usage, examples, package contents, contribution instructions, and licensing. Their project-specific workflows are not requirements of TraceNotes.

The [skills CLI source-format and option reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) supports the documented repository/local installation commands. CLI integration is optional and owned by that project.

## Authorship and validation limits

The instructions, wording, runnable examples, and scripts in this repository are independently written. Linked projects provide conceptual inspiration; their implementation files are not vendored here. Acknowledgment does not imply affiliation or endorsement.

Repository validation and example execution do not constitute a model-behavior benchmark. The practice cases are future evaluation material. Remote CI status should be read from the actual GitHub run, not inferred from the presence of a workflow file.
