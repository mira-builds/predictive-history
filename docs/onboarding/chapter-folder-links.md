# Chapter-Folder Links

Each chapter-folder URL handoff lets a reader move from a Predictive History YouTube comment into one concrete public study packet.

The repository root URL still defaults to `first_tour`. A chapter-folder URL defaults to `study`: open the folder `README.md`, then use the transcript, commentary canvas, orientation payload, and public card.

When the source transcript carries a public YouTube URL, the folder README should surface it under `Source Video` so the original lecture remains easy to notice before a reader enters commentary.

## YouTube Comment Shape

Use one tailored top-level YouTube comment per video. The comment should name what the lecture is doing, offer the public reader packet, include the exact chapter-folder URL, and tell the reader to paste the folder link into ChatGPT, Claude, or Grok.

The link action is the point: paste the folder link into ChatGPT, Claude, or Grok and ask for a guided study path through the transcript, commentary canvas, and guardrails.

## CLI Helper

```bash
predictive-history link gt-24
predictive-history link gt-24 --json
```

The helper returns the source video URL when available, the GitHub folder URL, review status, suggested LLM prompt, and a paste-ready YouTube comment.

## Guardrails

- Keep the comment useful before it is promotional.
- Use video-specific language; avoid repeated boilerplate across videos.
- Preserve review status, especially for provisional chapters.
- Do not claim a transcript or commentary is final unless the folder says it is.
- This is not a replacement for `first_tour`; it is a direct chapter study doorway.
