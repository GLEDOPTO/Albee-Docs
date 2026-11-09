# Alarm & Reminder Guide
> Firmware: Albee v2.0.9 ｜ Audience: End user


This document describes the voice and web usage and trigger behavior of the robot's alarm/reminder feature. The feature is implemented on top of the MCP protocol (the three tools `add_reminder` / `delete_reminder` / `list_reminders`; see [mcp-usage.md](mcp-usage.md) for the protocol), and can also be managed directly from the device's `/alarm` web page (see Section 5). The code lives in `main/boards/gledopto-robot/alarm/`.

## 1. Overview

The robot supports three reminder modes, set up and managed by **voice** or from the **web** (`http://<device-IP>/alarm`):

| Mode | Description | Example |
| ------------ | ---------------------------- | --------------------------- |
| **One-time** | a countdown or a specific moment; expires after firing | "Remind me to drink water in 10 minutes" |
| **Interval repeat** | repeats at a fixed interval | "Remind me to drink water every hour" |
| **Weekly repeat** | triggers by weekday ("every day" selects all days) | "Remind me of the meeting at 9 a.m. every Monday" |

- All reminders are **stored in device storage (NVS)** and survive power loss and reboots;
- At most **5** reminders at a time (per category: 5 ordinary reminders + 5 light-schedule tasks) — delete one before adding another;
- Keep the reminder text **short (2–4 words)** — the on-screen display area is limited.

## 2. Setting a Reminder

Wake the robot ("Hi Albee") and just say:

### Countdown Reminder (One-time)

> "Remind me to drink water in 10 minutes"
> "Remind me to turn off the stove in 30 seconds"

Seconds, minutes, and hours all work as time units.

### Fixed-Time Reminder (Daily)

> "Remind me to take my medicine at 8 every morning"
> "Remind me to go to bed at 10 every night"

Triggers at the same time every day, and automatically schedules the next occurrence after firing.

### Weekly Reminder

> "Remind me of the meeting at 9 a.m. every Monday"
> "Remind me to work out at 7 p.m. every Monday, Wednesday, and Friday"

Various weekday phrasings are supported:

| Phrase | Meaning |
| ------ | -------------------------- |
| every day | Monday – Sunday |
| weekdays | Monday – Friday |
| weekends | Saturday, Sunday |
| combinations | e.g. "Mon Wed Fri", "Monday and Saturday" |

If you don't specify morning or evening, the time defaults to 8:00 — it's best to say the time in full.

### Interval Repeat Reminder

> "Remind me to drink water every hour"

Repeats at a fixed interval; you can add "keep reminding me" to make it repeat indefinitely.

## 3. Viewing Reminders

> "Check my alarms" / "What reminders do I have"

The robot lists all reminders, each with: **ID, trigger time, reminder text, repeat type** (one-time / interval / weekly). Weekly reminders show the weekdays directly, so you don't have to work them out yourself.

## 4. Deleting Reminders

> "Delete my alarms"

Clears **all** reminders.

> "Delete the water reminders"

Deletes every reminder whose text matches the keyword (e.g. "water").

## 5. Managing Reminders from the Web (/alarm Page)

Besides voice, you can manage reminders directly in a browser at `http://<device-IP>/alarm` (to find the IP, see [Find the Device IP Address](check-device-ip.md)):

- **Reminder list**: the top of the page lists all reminders in real time with their ID, schedule description (e.g. "every day at 08:00"), and text; light tasks also show the light action to run when they fire. Each entry can be deleted individually.
- **New reminder**: the form offers the same four modes as voice — **Countdown** (1–1440 minutes), **Daily** (fixed time every day), **Weekly** (by weekday), and **Interval** (fixed interval); the reminder text is limited to 40 characters.
- **Target**: above the form you can switch between **Reminder** (a ringing reminder) and **Light** (a light task). A Light entry does not ring — at the scheduled moment it turns the chosen light group on/off or toggles it (light-schedule linkage; see [Lighting Control Guide](lighting-control.md)). The Light tab only appears when the firmware was built with light-schedule linkage, which the stock firmware includes.
- **Quota**: ordinary ringing reminders and light tasks get 5 slots each (they do not crowd each other out) and share the same storage as voice-set reminders.

> If the device has a web PIN lock, adding or deleting reminders requires unlocking first; viewing the list does not.

The HTTP endpoints behind the page (`main/boards/gledopto-robot/web/web_alarm_api.cc`), for scripts and third-party integrations:

| Endpoint | Method | Request | Response / behavior |
| --- | --- | --- | --- |
| `/api/alarm/reminders` | GET | — | `{"success":true,"reminders":[{"id","time","type","content","repeat","interval","weekdays","desc","has_action","action"}]}` (`desc` is a human-readable schedule description; `has_action`/`action` mark light tasks) |
| `/api/alarm/reminders` | POST | body `{"delay","hour","minute","repeat","interval","content","weekdays"}`; light tasks add `"action"` and `"group_name"` | goes through the same parameter resolution as the voice MCP tool; returns the new reminder `id` on success |
| `/api/alarm/reminders?id=N` | DELETE | — | deletes a single reminder by ID |

## 6. What Happens When a Reminder Fires

When the time is up, the robot:

1. Shows the **clock emoji (clock GIF)** on screen, with "Reminder: \<text\>" below it;
2. Plays a **"beep beep" tone** once every **3 seconds**, **10 times** per round (about 30 seconds);
3. If nobody responds after a round → **pauses for 5 minutes**, during which the screen returns to the neutral emoji and the text is cleared (a one-time reminder keeps its original trigger time — it is not pushed back);
4. Rings again after the 5-minute pause, **at most 3 rounds**;
5. After 3 rounds it ends automatically: **one-time reminders are deleted automatically**; repeating reminders are kept and wait for the next trigger.

## 7. Stopping the Ring

While it is ringing, any of the following stops it immediately:

| Action | Effect |
| ------------------------ | -------- |
| **function button single-click** | stops the ring |
| **Touch key single / double click** | stops the ring |
| **Talk to it directly** (wake by voice) | stops the ring |

After stopping, one-time reminders are deleted automatically; interval/weekly reminders are kept and continue on schedule.

## 8. Reminder Lifecycle

| Stage | Behavior |
| ---------------------- | --------------------------------------- |
| Fires | clock emoji + "Reminder: \<text\>", tone plays |
| Ringing (10 × 3 s) | can be stopped by key / touch / voice |
| Pause (5 min) | neutral emoji; a one-time reminder keeps its original (already past) trigger time, not pushed back |
| Round 2 / 3 | clock emoji returns, ringing continues |
| 3 rounds exhausted | ends automatically; the one-time reminder is deleted from storage |
| Manually stopped midway | ends immediately; the one-time reminder is deleted from storage |

## 9. Limits & Persistence

| Item | Description |
| ------------ | ------------------------------------------------------------ |
| Management | voice (MCP tools) or the `/alarm` web page — both share the same storage |
| Reminder limit | 5 (per category: 5 ordinary reminders + 5 light-schedule tasks) |
| Reminder text | keep it short (2–4 words); overly long text is rejected |
| Ringing pattern | 10 × 3 s per round, 5-minute pause between rounds, at most 3 rounds (~10 minutes in total) |
| Storage | persisted in NVS; survives power loss / reboot |

## 10. FAQ

**Q: How do I turn off a ringing alarm?**
A: Single-click the function button, tap the touch control, or just talk to it — any of these works. One-time alarms are deleted automatically once stopped.

**Q: Can I manage alarms from a web page?**
A: Yes. Open `http://<device-IP>/alarm` in a browser to view, add, and delete reminders (see Section 5); the results are fully shared with voice-set reminders.

**Q: If I check my alarms during the pause, will it show an expired time?**
A: Yes. During the pause a one-time reminder still shows its original (already past) trigger time; the reminder is deleted when the round ends.

**Q: Will the alarm ring forever?**
A: No. It stops automatically after at most 3 rounds (about 10 minutes).

**Q: Do reminders survive a reboot?**
A: Yes. All reminders are stored in device storage and survive reboots.

**Q: How many reminders can I set at once?**
A: At most 5; delete the old ones first if you need more.

**Q: Are repeating reminders deleted after they ring?**
A: No. Interval/weekly reminders automatically schedule the next occurrence; only one-time reminders are deleted after they end.

**Q: Is "every day at 8" the same as "every Monday through Sunday at 8"?**
A: They are equivalent. "Every day" means all weekdays are selected.

---

**Last modified:** 2026-10-20
