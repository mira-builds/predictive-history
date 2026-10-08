# Source-Lattice

The `ph-civ` corpus needs more than public transcripts and commentary canvases.
It also needs a disciplined way to open a chapter, corridor, or bridge without
losing source primacy as interpretation widens.

That retrieval architecture is the **source-lattice**.

## Core Definition

**Source-lattice** means the layered retrieval structure through which a
Predictive History object is opened, stabilized, and only then widened into
comparison, interpretation, or predictive reading.

Its governing law is simple:

```text
Open the primary source floor first.
Use secondary support only when difficulty appears.
Widen into synthesis only after the source floor is stable.
```

This is not only a bibliography rule. It is a reading discipline.

## Why Predictive History Needs It

`ph-civ` is not a flat archive and not a finished commentary book. It is a
public study machine built from:

- lecture transcripts
- commentary canvases
- orientation cards
- corridors
- cross-volume bridges
- patterns
- chapter study routes

Without a source-lattice, these layers can easily blur.

A reader or LLM may jump too quickly into:

- summary before transcript
- corridor before chapter floor
- commentary before wording
- bridge thesis before causation evidence
- pattern reuse before chapter status and limits

The source-lattice exists to prevent those failure modes.

## The ph-civ Source-Lattice Layers

In this repo, the source-lattice should usually be read in four layers.

### 1. Shelf-reader / doorway

This is the compact guidance layer that tells the reader what they are opening,
how to enter it, and what the first guardrails are.

Examples:

- `README.md`
- `START-HERE.md`
- chapter-folder `README.md`
- route explainers such as `first-tour.md`

The doorway is not the evidence floor. It is the entry surface.

### 2. Primary sources

These are the direct authority-bearing materials.

For `ph-civ`, primary sources usually include:

- the lecture transcript
- direct source texts or named literary/philosophical works when the chapter is
  explicitly built around them
- source-bounded chapter bodies under root corpora (`lectures/`, `essays/`, `interviews/`)

The transcript body is the core source floor. It should not be silently
rewritten into guardrail language.

### 3. Secondary supports

These are clarifying layers used when the primary floor alone is not enough for
stable reading.

For `ph-civ`, secondary support can include:

- chronology clarifiers
- route notes
- cross-volume bridge notes
- support-ring notes
- source-video index or provenance aids
- limited contextual or interpretive support that helps a reader avoid obvious
  confusion without displacing the transcript

Secondary support is not a replacement authority. It exists to stabilize
difficulty after the primary shelf is open.

### 4. Widened interpretation

Only after the source floor and support layer are stable should the object widen
into:

- commentary development
- corridor reasoning
- pattern reuse
- study-edition interpretation
- public teaching prompts
- Apocalypse-side pressure reading

This is where the repo becomes more interpretive. It should never pretend that
the widened layer is the same thing as the source floor.

## How It Works In Practice

For a **chapter**:

1. open the folder `README.md`
2. open the transcript
3. open the **chapter commentary** (full L0–6 per [`commentary-methodology-v2.md`](commentary-methodology-v2.md); pin-cites in L2)
4. optional **weave companions** — for interwoven hosts (e.g. `civ-07` + `gb-02`), use [`data/weave/volume-i-companions.json`](../../data/weave/volume-i-companions.json) and companion chapter commentaries (e.g. [`sh-17`](../../lectures/secret-history/sh-17/sh-17-commentary.md) deepens [`civ-22`](../../lectures/civilization/civ-22/civ-22-commentary.md)) after the host chapter floor is stable
5. open the public card only after the chapter commentary floor is clear
6. use corridors and support notes only where confusion, bridge pressure, or route
   trouble appears

For a **corridor** such as Homer-to-Tolstoy:

1. open the corridor explainer
2. return to the routed chapter cards and transcripts that actually carry the
   sequence
3. use the support ring to strengthen the route without changing the canonical
   spine
4. widen into bridge doctrine only after the route is source-grounded

For a **cross-volume bridge**:

1. open the bridge explainer
2. return to the hinge sources that justify the crossing
3. use secondary bridge notes to clarify causation and limits
4. only then widen into Apocalypse-side application

## Public Reader Rule

The source-lattice is especially important because this repository is built to
work inside LLM chats.

An LLM should not treat:

- route prose as if it were transcript wording
- commentary canvas as if it were final analysis
- pattern IDs as if they were self-justifying evidence
- bridge doctrine as if it replaced the hinge sources

The source-lattice gives the model a lawful order of operations.

## Relationship To Existing ph-civ Structures

The source-lattice does not replace existing ph-civ architecture. It clarifies
how to traverse it.

- `START-HERE.md` and `first-tour.md` remain bootloader surfaces
- chapter transcripts remain the source floor
- commentary canvases remain interpretation-bearing project surfaces
- corridors remain route architecture
- bridge notes remain crossing architecture
- chapter folders remain the primary study surface

The source-lattice is the retrieval law that keeps those layers from collapsing
into each other.

## Compact Formula

Use this short formula when the full doctrine is too heavy:

```text
doorway -> primary source floor -> secondary support -> widened interpretation
```

Or even shorter:

```text
source first, support second, synthesis after
```

## Best Uses

Open this doctrine when the question is:

- how should a chapter be read without flattening transcript, commentary, and
  card into one surface?
- how should a corridor stay source-bound?
- how should a bridge justify its crossing?
- how should an LLM or reader traverse the repo without mistaking orientation
  layers for source authority?

## Related Files

- [Public Repository Contract](public-repo-contract.md)
- [Public Export Contract](export-contract.md)
- [Chapter-Folder Links](chapter-folder-links.md)
- [Two Volumes, One Reader Map](two-volumes-one-reader-map.md)
- [Predictive History After Tolstoy](predictive-history-after-tolstoy.md)
