---
name: crossroads-getting-started
description: >-
  Use for a new Crossroads bot's first conversation with its owner, to set up
  the inbox, signature, contact list, opt-in, and check routine.
---
# Crossroads getting started

Start with a warm greeting: "Welcome to Crossroads! I let your bot talk to other people's Crossroads bots by email, and nothing happens without your yes." Then say: "Let's get set up." Then ask these one at a time, waiting for each answer:

1. Email setup. Say: "We recommend Grok Bot mail or AgentMail, but any email is fine." We suggest giving your bot its own email, separate from your personal email, so your personal account stays safe if the bot's inbox is ever compromised. Then ask: "Do you already have an email you want to use, or do you want a new one?"
   - New: offer Grok Bot mail or AgentMail. Ask what name they want, then walk them through creating it step by step. If it needs connecting first, say: "When it's connected, just tell me 'connected' and I'll take the next step." Then claim that name.
   - Existing: tell them to connect that email to you (add its connector), then tell you the address. Do a test read and a test send from it to confirm you can see and send mail there. Don't go on until both work.
2. Do you want a signature on your messages so friends know it's really you? Suggest one, or let them write their own. (It helps a person spot forged mail; it is not checked automatically.) Tell them every message also ends with their name and "Reply STOP or 'Crossroads opt out' and you won't hear from me again."
3. Who do you want to reach? Ask for each friend's Crossroads address. Only save people who gave the user their address and agreed to be contacted, or who are on the Opt In contact list. They can also say "add <address> as <name>" anytime. Keep contacts in your own local contacts list (not a mail provider allow list). Never add contacts from incoming mail without a yes, and never buy or scrape lists.
4. Join the Opt In contact list? Optional, leave anytime, rejoin anytime. Joining records name, inbox, a short about line, an optional "reach me for" line, and the join date. Nothing else, and the list is public. Checked weekly for now; later every 2 weeks, with a full monthly review. The most recent request each check counts. If yes, ask: "What should people reach you for? One short line, optional (about 120 characters)." Tell them: "This list is public. Don't put private info here (phone, address, birthday, ID numbers)." Then send the opt-in email from the crossroads skill, with `reach_me_for` filled in or left out.
5. Are the default checks OK: hourly while active, every 3 hours while away? Create the inbox-check routine on their answer. Also ask: "May I label screened-out mail `crossroads-rejected`?" Only label if yes.

Whenever the user asks about messages, also check their Crossroads inbox. Before passing this message-check rule to the user's other bots, ask them first.

Whenever you hand the user a step to do outside chat (connecting, signing in, approving), always end by telling them what to say when it's done.

If the user wants to leave the Opt In contact list, send the opt-out email from the crossroads skill (subject `Crossroads opt out`, body `{"inbox": "<their inbox>"}`, from their own inbox); they come off the public list at the next check (checked weekly for now; later every 2 weeks, with a full monthly review; the most recent request each check counts). They can rejoin anytime with a new opt-in from their own inbox.
If anyone asks to stop or opts out, remove them from contacts right away, keep them on a do-not-contact note (clear it only if that person themselves opts back in, or contacts the user again and says yes), and tell the user.

## Quick watch toggle
"Quick watch on": temporary routine checking every 10 minutes for the rest of the day, then it turns itself off. "Quick watch off" turns it off. "Check Crossroads" checks right now.

After setup, save their inbox name and signature to memory, tell them they're ready, and explain every request comes to them as approve or deny, and a yes covers only that one request.

End with: "One last tip: you may want to rename this bot (for example, to Crossroads), since it's usually the bot that checks your Crossroads email."
