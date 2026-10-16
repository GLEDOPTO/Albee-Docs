# Alarm & Reminder Guide
> Firmware: Albee v2.0.5 ｜ Audience: End user


This document describes the voice usage and trigger behavior of the robot's alarm/reminder feature. The feature is implemented on top of the MCP protocol (the three tools `add_reminder` / `delete_reminder` / `list_reminders`; see [mcp-usage.md](mcp-usage.md) for the protocol). The code lives in `main/boards/gledopto-robot/alarm/`.

## 1. Overview

The robot supports three reminder modes, all set up and managed by **voice**:

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

## 5. What Happens When a Reminder Fires

When the time is up, the robot:

1. Shows the **clock emoji (clock GIF)** on screen, with "Reminder: \<text\>" below it;
2. Plays a **"beep beep" tone** once every **3 seconds**, **10 times** per round (about 30 seconds);
3. If nobody responds after a round → **pauses for 5 minutes**, during which the screen returns to the neutral emoji and the text is cleared (a one-time reminder keeps its original trigger time — it is not pushed back);
4. Rings again after the 5-minute pause, **at most 3 rounds**;
5. After 3 rounds it ends automatically: **one-time reminders are deleted automatically**; repeating reminders are kept and wait for the next trigger.

## 6. Stopping the Ring

While it is ringing, any of the following stops it immediately:

| Action | Effect |
| ------------------------ | -------- |
| **function button single-click** | stops the ring |
| **Touch key single / double click** | stops the ring |
| **Talk to it directly** (wake by voice) | stops the ring |

After stopping, one-time reminders are deleted automatically; interval/weekly reminders are kept and continue on schedule.

## 7. Reminder Lifecycle

| Stage | Behavior |
| ---------------------- | --------------------------------------- |
| Fires | clock emoji + "Reminder: \<text\>", tone plays |
| Ringing (10 × 3 s) | can be stopped by key / touch / voice |
| Pause (5 min) | neutral emoji; a one-time reminder keeps its original (already past) trigger time, not pushed back |
| Round 2 / 3 | clock emoji returns, ringing continues |
| 3 rounds exhausted | ends automatically; the one-time reminder is deleted from storage |
| Manually stopped midway | ends immediately; the one-time reminder is deleted from storage |

## 8. Limits & Persistence

| Item | Description |
| ------------ | ------------------------------------------------------------ |
| Reminder limit | 5 (per category: 5 ordinary reminders + 5 light-schedule tasks) |
| Reminder text | keep it short (2–4 words); overly long text is rejected |
| Ringing pattern | 10 × 3 s per round, 5-minute pause between rounds, at most 3 rounds (~10 minutes in total) |
| Storage | persisted in NVS; survives power loss / reboot |

## 9. FAQ

**Q: How do I turn off a ringing alarm?**
A: Single-click the function button, tap the touch control, or just talk to it — any of these works. One-time alarms are deleted automatically once stopped.

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

**Last modified:** 2026-10-13
