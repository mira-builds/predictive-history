# Commentaries

**Essay commentary canvases** for the Predictive History public corpus.

Repo path: **`commentaries/`** at the repository root (sibling to [`essays/`](../essays/README.md), [`interviews/`](../interviews/README.md), [`lectures/`](../lectures/README.md)).

## Scope (this pass)

- **Essays only:** `commentaries/essay-YYYY-MM-DD-{slug}-commentary.md` pairs with flat [`essays/essay-YYYY-MM-DD-{slug}.md`](../essays/README.md).
- **Lectures / interviews** keep commentary beside chapter folders under [`lectures/`](../lectures/README.md) and [`interviews/`](../interviews/README.md).

## Path template

| File | Role |
| --- | --- |
| `commentaries/{source_id}-commentary.md` | Open commentary canvas |
| [`essays/{source_id}.md`](../essays/) | Verbatim essay body |
| [`data/cards/{source_id}.md`](../data/cards/) | Public orientation card |

Registry: [`data/cards.jsonl`](../data/cards.jsonl) · essays slice [`predictive-history-essay-index.md`](../essays/predictive-history-essay-index.md) · full hub [`docs/predictive-history-index.md`](../docs/predictive-history-index.md).
