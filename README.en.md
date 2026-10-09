# Bailing

## v0.3.0: Recovery reliability

Adds an optional operational summary, character-budget controls and explicit optional-source read failures. Existing workspaces remain supported. See [recovery behavior and validation scope](docs/RECOVERY.md); configuration diagnostics are guidance only.


**An open experiment in digital individuality, persistent memory, and continuity across runtimes.**

[中文](README.md)

What should persist when an AI companion changes models or runtimes? Who controls its records? How do we prevent a single conversation from becoming permanent identity?

Bailing explores these questions through user-owned, readable files: genesis, state, tasks, memory, significant experiences, and an identity change ledger. This public edition contains reusable tooling and synthetic examples, not the private Bailing archive. Initiated by [ruyingrufeng](https://github.com/ruyingrufeng), with AI-assisted implementation.

## What is a digital individual?

We propose the following working definition:

> **A digital individual is a digital entity built on AI cognition and interaction, with a recognizable identity, persistent memory and relationships, and behavioral tendencies that can develop and be revised through ongoing experience. A shared archive that can be preserved, inspected, and transferred carries that identity and history, allowing different models and runtimes to continue the same individual.**

The definition has five connected parts:

- **Identity:** a recognizable self-description, voice, core principles, and boundaries, with a record of approved changes.
- **Memory:** sourced accounts of events that distinguish facts, inferences, uncertainty, and corrections.
- **Relationships:** accumulated understanding, agreements, and boundaries that persist through interaction.
- **Evolution:** experience may inform later judgments, preferences, and behavior; a single conversation does not automatically become permanent personality.
- **Continuity:** identity, memory, relationships, and unfinished work have a shared basis for recovery when models, tools, or runtimes change.

Bailing follows a **creator-sovereign** approach. The creator is the person who establishes and helps maintain the individual, retaining final control over core definitions, memory, capabilities, and continued existence. Within agreed boundaries, the individual can express views, develop preferences, and participate in long-term collaboration. Users can define their own individuals and relationship styles.

This is a working definition for design and evaluation, open to discussion and revision. “Individual” describes how identity and experience are organized; it does not assert subjective consciousness, free will, or legal personhood. Portable records provide a basis for continuity, while actual model behavior still requires evaluation.

## Try it

Python 3.10+, no third-party dependencies. macOS/Linux; Windows users can use WSL.

```bash
git clone https://github.com/ruyingrufeng/bailing.git
cd bailing
python3 -m bailing init ../my-individual --name River
python3 -m bailing doctor --root ../my-individual
python3 -m bailing context --root ../my-individual --runtime codex
python3 -m bailing record --root ../my-individual --runtime codex "Reading session outline drafted; date undecided."
python3 -m bailing context --root ../my-individual --runtime hermes
```

Edit the new workspace's GENESIS.md to define your own individual's identity and boundaries. Give the context output to your chosen AI as user-approved reference material. Runtime labels identify the reader; they do not invoke or configure products. New workspaces are created outside the public source tree and ignore all contents in Git by default.

## New in v0.2: finding history

Read-only archive search with runtime, inclusive date, and session filters. Results include source paths and line numbers. It only reads Markdown you explicitly place in your private workspace; there is no account discovery or automatic import.

```bash
python3 -m bailing archive-search "reading" --root examples/fictional
python3 -m bailing archive-search "reading" --root examples/fictional --runtime hermes --since 2026-01-02 --json
```

Store files under `memory/archive/` (subdirectories allowed), named `YYYY-MM-DD-runtime-session.md`. Use `### user · timestamp` and `### assistant · timestamp` headings for message boundaries. Existing v0.1 workspaces only need this optional directory; do not reinitialize them. Invalid/unreadable files and symlinks are reported as skipped. JSON includes full matching blocks; inspect output before sharing. Lexical relevance is not current truth. See [format and limitations](docs/ARCHIVE.md).

## What is implemented

Initialization, file validation, deterministic context assembly, factual journal append, and source-preserving lexical retrieval (`prepare`). A fictional reading-session example is in `examples/fictional`; see [the demo](docs/DEMO.md).

## Limits

Experimental v0.2.0. No autonomous memory extraction, account access, model calls, background jobs, or enforcement of identity governance. Task checkpoints must be updated explicitly. Software tests do not establish model compliance or successful model-to-model continuity. No real-model behavioral evaluation of this public edition has been completed. Context size is not automatically limited; use a single writer. Retrieval relevance is not truth, and `prepare` does not search journals.

## Join the exploration

We welcome failures, questions, alternative approaches, and small contributions via Issues and pull requests. How should continuity be evaluated? What should be remembered or forgotten? How can users inspect and control identity changes? Use synthetic examples, never private transcripts.

MIT License. This release is a fresh public extraction with no private archive or inherited commit history. See [design](docs/DESIGN.md), [contributing](CONTRIBUTING.md), and [changelog](CHANGELOG.md).
