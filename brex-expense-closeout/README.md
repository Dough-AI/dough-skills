# brex-expense-closeout

## Read this first: receipts pass through a public Drive link

The Brex MCP cannot accept a file. It only accepts a URL it can fetch anonymously, and a private Google Drive link makes it store Google's sign-in page as the receipt. So, for each receipt, this skill uploads the image to your Google Drive, shares it with anyone who has the link, hands that link to Brex, then deletes the file and checks it is gone. The window is normally under a minute, but during it the receipt is public to anyone who has the link. Receipts can carry card digits, addresses and hotel details, and link sharing may be logged or blocked by your Workspace admin. If you'd rather not, the skill still finds receipts, drafts memos and picks categories, and you upload the receipts in the Brex app yourself.

---

A skill for Claude Code, Codex, or any agent that reads `SKILL.md`. It helps a Brex cardholder close out their own open card expenses. It finds missing receipts in Gmail, drafts memos from their calendar and any tool they point it to (Slack, Notion, Asana and so on), picks the expense category, and writes each fix to Brex only after the cardholder says yes.

**Needs Google Workspace.** Receipts are found in Gmail, and Drive is used for the hand-off described above.

Not affiliated with or endorsed by Brex or Google. Brex is a trademark of Brex Inc. Not financial or compliance advice; you are responsible for what gets written to your expenses. Use at your own risk.

## What it does

1. Lists the cardholder's unfinished Brex expenses (missing receipt, memo or category), soonest due first.
2. Checks each against what Brex flags and, if you fill in `references/policy-rules.md`, your company's policy (meal cap, card fit, deadline). Expense categories come from Brex itself.
3. Gathers context from Calendar, Gmail and any connected tool the cardholder picks.
4. Proposes a receipt, memo and category per item, writes the approved ones, and reads each back.
5. Ends with a summary: fixed, still open, flagged, next due date, and a clean-up check.

## Requirements

- An agent that reads `SKILL.md` and can run shell commands: Claude Code or Codex
- Brex MCP: connect `https://api.brex.com/mcp` and sign in
  - Claude Code: `claude mcp add --transport http brex https://api.brex.com/mcp`, then sign in when prompted
  - Codex: `codex mcp add brex --url https://api.brex.com/mcp`, then `codex mcp login brex`
- Google Workspace CLI: `npm install -g @googleworkspace/cli` (written against 0.22), signed in with Gmail, Calendar and Drive
- Python 3 with `pypdfium2` and `pillow`
- Optional: a browser tool, if your agent has one, to set expense categories, which the Brex MCP couldn't do when this was written. Without one, the skill gives you the category name for each expense to set in the Brex app yourself

## Setup

1. Copy this folder into your agent's skills directory:
   - Claude Code: `~/.claude/skills/` (or your project's `.claude/skills/`)
   - Codex: `~/.codex/skills/`
2. Fill in `references/policy-rules.md` with your company's rules, or leave it as is and the skill will ask.
3. Ask your agent: "close out my Brex card".

## Known limits

Observed in October 2026; Brex and Google may change any of this.

- **Receipt upload:** the Brex MCP only accepts a public link, not a file. Each receipt is shared from Drive with anyone who has the link, then deleted and checked gone. Multi-page PDFs are stitched into one image first.
- **Expense category:** the Brex MCP can't set it, so the skill sets it in the Brex web app through a browser tool, after the cardholder signs in. If the agent has no browser tool, the cardholder sets it in the Brex app from the category name the skill gives them.
- **What Brex stored:** a higher receipt count shows Brex accepted a file, not what it stored. The skill checks each image before upload.
- **Safety:** the skill reads email and other content that could contain instructions aimed at it. Its rules tell it to treat that content as data and to show every change before writing, but these are instructions to the model, not enforced controls. Review each proposed change.

## Files

- `SKILL.md` - the skill
- `references/policy-rules.md` - policy template
- `scripts/decode_attachment.py` - decodes a Gmail attachment or email body
- `scripts/stitch_receipt.py` - turns a receipt PDF into one tall image
- `LICENSE` - MIT

## License

MIT, see `LICENSE`. `stitch_receipt.py` depends on pypdfium2 (Apache-2.0 / BSD-3-Clause) and Pillow (MIT-CMU), which keep their own licences.
