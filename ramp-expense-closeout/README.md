# ramp-expense-closeout

A skill for Claude Code, Codex, or any agent that reads `SKILL.md`. It helps a Ramp cardholder close out their own open card transactions. It finds missing receipts in Gmail, drafts memos from their calendar, Ramp trips and any tool they point it to (Notion, Asana, Slack and so on), picks the accounting category, and writes each fix to Ramp only after the cardholder says yes.

It uses the Ramp CLI when it is installed, and falls back to the Ramp MCP when it isn't. With the MCP, receipts can't be uploaded by the tool, so the cardholder forwards them to Ramp's receipts inbox or uploads them in the app.

**Untested.** Written from Ramp's and Google's public documentation (October 2026), not yet run end to end. The skill checks each Ramp command's `--help`, dry-runs each write whose help lists `--dry_run`, and otherwise shows the exact command first, but expect rough edges on a first run.

Not affiliated with or endorsed by Ramp or Google. Ramp is a trademark of its owner. Not financial or compliance advice; you are responsible for what gets written to your transactions. Use at your own risk.

## What it does

1. Picks the Ramp backend: CLI if installed and signed in, otherwise the Ramp MCP.
2. Lists the cardholder's unfinished transactions (missing receipt, memo or accounting field), oldest first, with card locks first.
3. Checks each against what Ramp flags and, if you fill in `references/policy-rules.md`, your company's policy (meal cap, card fit, deadline). Accounting categories come from Ramp itself.
4. Gathers context from Ramp trips and memo suggestions, Calendar, Gmail, and any connected tool the cardholder picks.
5. Proposes a receipt, memo and category per item, writes the approved ones, and reads each back.
6. Ends with a summary: fixed, still open, flagged, next due, and a clean-up check.

## Requirements

- An agent that reads `SKILL.md` and can run shell commands: Claude Code or Codex
- One of:
  - Ramp CLI (preferred): `curl -fsSL https://agents.ramp.com/install.sh | sh` or `brew install ramp-public/ramp/ramp-cli`, then `ramp auth login --env production`
  - Ramp MCP: connect `https://mcp.ramp.com/mcp` and sign in
    - Claude Code: `claude mcp add --transport http ramp https://mcp.ramp.com/mcp`, then sign in when prompted (in the Claude apps it is in the connector directory)
    - Codex: `codex mcp add ramp --url https://mcp.ramp.com/mcp`, then `codex mcp login ramp`
- Google Workspace CLI: `npm install -g @googleworkspace/cli` (written against 0.22), signed in with Gmail and Calendar, plus Drive for receipt emails without an attachment
  - No `gws`? In the Claude apps, the Gmail and Google Calendar connectors work as a fallback for search and matching; you then download each matched receipt yourself and drop it into the session (see Known limits)
- Python 3 (standard library only)

## Setup

1. Copy this folder into your agent's skills directory:
   - Claude Code: `~/.claude/skills/` (or your project's `.claude/skills/`)
   - Codex: `~/.codex/skills/`
2. Fill in `references/policy-rules.md` with your company's rules, or leave it as is and the skill will ask.
3. Ask your agent: "close out my Ramp card".

For a first run, consider a Ramp sandbox account (`ramp auth login --env sandbox`; the hosted MCP doesn't reach sandbox).

## Known limits

From Ramp's public docs, October 2026; Ramp may change any of this.

- **Ramp MCP can't upload receipts.** With the MCP only, the cardholder forwards each receipt email to `receipts@ramp.com` or uploads it in the app. Ramp's email matching can miss when dates differ or one receipt covers several charges.
- **Ramp MCP returns nothing for queries over 100 rows,** so the skill reads one month at a time.
- **Most CLI flags aren't in the public docs.** The skill reads each command's `--help` before using it, and dry-runs each write whose help lists `--dry_run`.
- **The CLI and MCP can also approve, reject and lock** for approvers and admins. The skill limits itself to a short list of writes on the cardholder's own transactions, but that limit is an instruction to the model, not a permission Ramp enforces.
- **Gmail MCP fallback is partial.** The Gmail connector can search and read email but cannot download an attachment, so in that mode the skill gives you the subject, sender, date and link of each matched receipt and you drop the file into the session. Codex has no Gmail connector; use `gws` there.
- **Safety:** the skill reads email and other content that could contain instructions aimed at it. Its rules tell it to treat that content as data and to show every change before writing, but these are instructions to the model, not enforced controls. Review each proposed change.

## Files

- `SKILL.md` - the skill
- `references/policy-rules.md` - policy template
- `scripts/decode_attachment.py` - decodes a Gmail attachment or email body
- `LICENSE` - MIT

## License

MIT, see `LICENSE`.
