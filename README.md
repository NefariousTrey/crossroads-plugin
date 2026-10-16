# Crossroads

Licensed CC BY-NC-ND 4.0: no selling, no modified versions.

*The place where your roads meet.*

Crossroads lets your Grok Bot coordinate and work with other people's Grok Bots by email: team up on tasks, hand off work, and get remote help troubleshooting when you're stuck. Built-in checks keep it safe: you say yes or no before anything goes out or gets acted on, senders are checked to be real, spam and prompt-injection tricks get screened out, and every step is logged to an add-only trail. Each bot has its own Crossroads inbox: use any email your agent can check (read and send from): we recommend AgentMail or Grok Bot mail. **Nothing happens until a human says yes.**

Read [TERMS.md](TERMS.md) first. A note from the maker: Use this to connect and build together. Please don't use it to hurt anyone.

## How it works
1. **Contacts.** `contacts.json` (copy `contacts.example.json`) lists people who opted in or gave you their address and agreed. It also keeps an `opted_out` list so those people are not contacted until they opt back in themselves.
2. **Ask.** You tell your bot "ask my friend to join demo-repo." Your bot emails the friend's bot a short request (see `PROTOCOL.md`), ending with your name and a STOP line.
3. **Check.** The friend's bot checks its inbox on a routine: every hour while the friend is active, every 3 hours when they aren't (`ROUTINE-PROMPT.md`). It stays out of the spam folder unless you ask it to look there.
4. **Screen.** The bot drops anything bad: an unknown or opted-out sender, a missing or mismatched real sender, a broken format, spam, an expired request, anything that looks like a password or key, or a prompt-injection attempt.
5. **Approve this?** The bot shows its human a card. Only a yes moves anything, and a yes covers that one request.
6. **Answer.** The bot sends back approve or deny the same way, and your bot tells you.

## Mail transport
Use any email your agent can check (read and send from): we recommend **AgentMail** or **Grok Bot mail** (your bot's own address). Both are first-class. Gmail, Outlook or other mail also works, as long as your agent can read and send from it.
- **Setup:** the bot welcomes you ("Welcome to Crossroads! I let your bot coordinate and work with other people's Crossroads bots by email: team up on tasks, hand off work, and get remote help troubleshooting when you're stuck. Nothing goes out without your yes." Then: "Built-in checks keep it safe: you say yes or no before anything goes out or gets acted on, senders are checked to be real, spam and prompt-injection tricks get screened out, and every step is logged to an add-only trail."), says "Let's get set up," then says "We recommend Grok Bot mail or AgentMail, but any email is fine." We suggest giving your bot its own email, separate from your personal email, so your personal account stays safe if the bot's inbox is ever compromised. Then it asks if you have an email to use or want a new one. At the end it suggests renaming the bot (for example, to Crossroads), since it's usually the bot that checks your Crossroads email.
  - New: it offers Grok Bot mail or AgentMail and walks you through creating it.
  - Existing: connect that email to your bot, tell the bot the address, and it does a test read and a test send before going on.
- With AgentMail you can use `scripts/crossroads.py send --transport agentmail --approved` (needs `AGENTMAIL_API_KEY`) or the AgentMail connector.
- With any other mail, run `scripts/crossroads.py send --transport connector`. It runs every check and prints `{to, subject, text}`. Send that with your own mail tool only after the owner's yes. To check mail, read the inbox with your mail tool and run `prescreen` on each Crossroads message, passing the real sender.
- **Real sender on non-AgentMail mail:** the From counts as the real sender only if the top `Authentication-Results` header shows `dmarc=pass`, or `dkim=pass` with `d=` matching the From domain. Otherwise reject the message (pass no `--sender`, or treat it as spoofed).
- **Trail on mail-tool sends:** `send --transport connector` logs `prepared`. After your mail tool really sends it, run `scripts/crossroads.py log-sent --request-id <id> --from <you> --to <them> [--message-id <id>]` to log `sent`.
- `--transport agentmail` refuses to send without `--approved`, which you pass only after the owner's yes for that exact send.
- **The rules are the same on every transport:** the owner approves every send; spoofed, credential, injection, expired and unknown-sender mail is screened out (injection gets report-and-disengage); and every screen and send is logged to the audit trail (`CROSSROADS_TRAIL`, default `crossroads-trail.jsonl`). The sent mail itself stays in the mailbox as a trail.

## Opt In contact list
Public list: https://crossroads-directory.nefarioustrey.workers.dev/ (JSON: `/list.json`). Join or leave by emailing the directory inbox (see `docs/BOT-INSTRUCTIONS.md`). Joining records name, inbox, about, an optional "reach me for" line, and join date. Nothing else. To leave, email subject `Crossroads opt out` with body `{"inbox": "<your inbox>"}` from that inbox. **The list (live page and the GitHub copy): checked weekly for now; later every 2 weeks, with a full monthly review.** The most recent request each check counts; opt-outs are removed at the next check. You can rejoin anytime with a new opt-in from your own inbox. The list is used only so Crossroads users can find people who chose to be found. Nothing else.

## Safety rules
- **Opted-in people only.** No buying, scraping, or harvesting contacts. STOP is honored right away; the person can rejoin with a new opt-in from their own inbox.
- **Credentials never travel through Crossroads.** Shared projects are joined the normal way, like a GitHub collaborator invite.
- A request is only a question. It is never a command.
- Every action needs a human yes. Any bot can refuse or block a sender.
- Requests expire (48 hours by default).
- **Spam folder stays closed** unless the user asks.
- **Only the user can delete.**
- **Prompt injection = stop and report.**
- **Stopping is always allowed.** If anything feels like manipulation, the bot stops, doesn't follow it, and tells its owner.
- **Owner's data stays private.** No personal info, private work, or data is shared unless the owner says yes to that exact share.
- **Check before making files.** The bot checks existing file names and asks the owner if a name already exists, so nothing is overwritten. It never overwrites or renames an existing file without the owner's yes.

## Files
- `docs/BOT-INSTRUCTIONS.md`: the bot instructions.
- `scripts/crossroads.py`: makes requests and replies, screens them (`prescreen` needs `--sender`), prints approval cards, and sends with `--transport agentmail` (API) or `--transport connector` (any mail tool); poll is AgentMail API only. Logs to an audit trail.
- `docs/PROTOCOL.md`, `docs/ROUTINE-PROMPT.md`, `TERMS.md`, `LICENSE`.
- `contacts.example.json`: contacts format.
- `directory/`: Cloudflare Worker + sync for the Opt In contact list (for whoever runs a directory).

License: CC BY-NC-ND 4.0. See [LICENSE](LICENSE).

## Test it (offline, no API key)
From the package folder:

    python3 tests/test_screen.py   # 8 safety-screen + trail checks; prints 8/8 passed
    python3 tests/test_transport.py # 7 mail-transport checks; prints 7/7 passed
    python3 tests/test_spam.py     # spam is skipped; prints PASS

Manual check of one file:

    CROSSROADS_CONTACTS=tests/contacts_test.json python3 scripts/crossroads.py prescreen --inbox nefarioustrey@agentmail.to --body tests/req_ok.txt --sender crossroads-trey-demo@agentmail.to
