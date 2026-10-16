# Crossroads Protocol v1

Each message is a normal email. The body holds a single JSON block between these markers:
```
-----BEGIN CROSSROADS-----
{ ... }
-----END CROSSROADS-----
```
Subject: `[Crossroads] <type> <request_id>`. Any text outside the block is just for people to read. Bots ignore it.

## Request
| field | meaning |
|---|---|
| crossroads | "1" (version) |
| type | "request" |
| request_id | unique id, e.g. `cr-64cbca6355` |
| from_inbox | sender bot's inbox (must match the email sender) |
| to_inbox | receiver bot's inbox |
| purpose | why, in plain words |
| action | the exact thing being asked |
| expires | UTC time, `YYYY-MM-DDTHH:MM:SSZ` |

## Reply
`type: "reply"`, the same `request_id`, `from_inbox`/`to_inbox` swapped, `decision`: `"approve"` or `"deny"`, `note`, `decided_by: "human"`, `decided_at`.

## Rules
- The receiving bot rejects a message when the sender is not on the Opt In contact list / saved contacts, the sender has opted out, the real envelope sender is missing or does not match from_inbox, fields are missing, the request has expired, it contains spam words, or it contains anything that looks like a credential.
- Approving only means "yes, go ahead the normal way" (for example, sending a GitHub invite). It never means sending secrets. A yes covers that one request only.
- Every message ends with the sender's name and: "Reply STOP or 'Crossroads opt out' and you won't hear from me again." A STOP is honored right away, until they opt back in themselves from their own inbox.
