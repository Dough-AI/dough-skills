# Dough Skills

Open-source skills from [Dough](https://usedough.com) for finance work, written for Claude Code, Codex, or any agent that reads `SKILL.md`. Each skill is a self-contained folder and runs against your own logins. None of them need a Dough account.

| Skill | What it does | Needs |
|---|---|---|
| [brex-expense-closeout](brex-expense-closeout/) | Closes out a Brex cardholder's open expenses: finds receipts in Gmail, drafts memos from calendar and connected tools, picks the category, writes each fix after a yes. | Brex MCP, Google Workspace CLI, Python 3 |
| [ramp-expense-closeout](ramp-expense-closeout/) | The same for a Ramp cardholder. Uses the Ramp CLI, or the Ramp MCP when the CLI isn't installed. | Ramp CLI or Ramp MCP, Google Workspace CLI, Python 3 |

Each folder's README has the full requirements, setup and known limits. Read the Brex one before using it: receipts pass through a briefly public Google Drive link.

## Install

Copy the folder for the skill you want into your agent's skills directory, or ask your agent to do it from this repo's URL.

| Agent | Directory |
|---|---|
| Claude Code | `~/.claude/skills/` (or your project's `.claude/skills/`) |
| Codex | `~/.codex/skills/` |

Or download a single skill as a zip from the [Releases](../../releases) page.

Then fill in that skill's `references/policy-rules.md` with your company's expense policy, or leave it and the skill will ask.

## Repository layout

- One folder per skill at the root, named after the skill. Nothing reaches outside its folder, so copying one folder is a complete install.
- Shared helpers are duplicated into each folder on purpose. CI checks the copies stay identical.
- Every release attaches one zip per skill.

## Contributing

Issues and pull requests are welcome. Keep a skill self-contained, keep its `SKILL.md` frontmatter `description` under 500 characters, and run `python3 .github/scripts/check.py` before opening a PR.

## License

MIT, see [LICENSE](LICENSE). Third-party tools and libraries keep their own licences.
