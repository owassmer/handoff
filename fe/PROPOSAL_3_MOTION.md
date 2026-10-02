# Handoff: motion and live behavior (proposal)

Status: proposal only. Nothing below is built.

## Problem
The screens are right when they are still, but a case changes while you watch it and the page doesn't show that.
- The page polls every 7 seconds and swaps in the new data at once. New timeline entries, job stages, payments and
  emails appear with no signal that anything changed. Your co-founder's "black box" and "jumpy" notes come from this.
- Nothing says whether Handoff is working now, waiting on a vendor, or waiting on you.
- Chat: your message is saved, but nothing says a reply is coming or when.
- Accepting a plan swaps the page from the decision card to the work list in one frame.

## Principles
1. Motion only shows a real change in saved data. No fake progress, spinners with no work behind them, or counting
   animations on money.
2. Calm B2B motion: 120 to 200 ms, ease-out, no bounce and no celebration. Stripe and Linear are the reference.
3. Layout holds still. New things arrive in place; nothing already on screen jumps or reorders under the pointer.
4. Everything respects `prefers-reduced-motion` (changes are still highlighted, without movement).
5. Every addition replaces something: the blind 7-second swap is the first thing removed.

## What changes, and the product each pattern comes from
1. Live status line (GitHub Actions and Vercel deployment pages)
   - The Now line gets a live state: a small pulsing dot while a step is due ("Handoff is working"), a countdown when the
     next step has a known time ("Next check in 40 s", from `nextWakeAt`), a steady amber dot when waiting on a vendor
     with the vendor named, and the accent colour when it's waiting on you.
   - Limit: a turn's edits save only when it ends, so the app can't see a turn running. "Working" means "a step is
     due". I'd say that in the design notes, not in the product.
2. Arrivals (Linear issue updates, GitHub timeline, Front new message)
   - A new timeline entry, email or document slides in at the top (8 px, 160 ms) and its row carries a soft highlight
     that fades over 1.5 s.
   - A job's stage pill cross-fades to the new stage, and the rail fills the new step's dot (Stripe payment timeline).
   - A changed money figure gets the same brief highlight. It never counts up.
3. Change toasts (Linear and Vercel)
   - When something lands on a tab you're not looking at: one toast in the corner, e.g. "Westside booked the visit
     for Monday, October 5", with View. At most one visible; others fold into "3 more updates". Tab counts tick up
     (Front's unread counts).
4. Chat (Intercom, Slack)
   - Your message appears at once with "Sending", then "Sent".
   - A typing indicator shows while Handoff's reply is due. When the reply lands it replaces the indicator in place.
   - If no reply comes within 2 minutes the indicator becomes "Handoff will answer after its next step".
5. Decision to work (Stripe checkout, Linear state change)
   - Accept shows progress on the button, then the decision card collapses (200 ms) into the one-line accepted plan,
     and each order appears in Work as its record lands. No full-page swap.
6. Polling that follows the work (Vercel logs)
   - 2-second reads while a step is due or a reply is expected, 15 seconds while waiting on vendors, paused when the
     tab is hidden. This replaces the fixed 7 seconds.
7. Small interactions (Linear, Stripe)
   - Tab underline slides between tabs (150 ms); calendar event panel and document preview open with a short
     fade-and-rise; hover and focus states on every row and chip; skeleton rows while a tab first loads.

## Removed or replaced
- Removed: the fixed 7-second poll and whole-snapshot swap; the static status pill in the Now line.
- Replaced: the chat's silent wait with a typing indicator and plain "answer after next step" line; the decision card's
  hard swap with a collapse into the accepted plan.

## How it's built
- CSS transitions and keyframes, plus one small hook that compares ids and values between the last and current read
  and marks what's new or changed. No animation library.
- The adaptive poll is a change to the existing read resource's interval.
- Tests: arrivals are marked once and cleared; reduced motion disables movement; poll interval follows the state.

## How I'd check it (motion, not just stills)
- Use Case controls on a fresh test case while recording the page with Playwright video, extract frames with ffmpeg
  every 100 ms around each change, and review the frame strips with vision_analyze against the reference products:
  does each change read as one clear event, does anything jump, is anything missed.
- Same pass at 390 px.
