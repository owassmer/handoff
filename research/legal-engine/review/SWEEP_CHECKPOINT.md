# Sweep checkpoint: building, owner and agent preconditions (paused)

Stopped 2026-09-29 16:26 at Owen's request, to save machine compute. No process from the sweep is running.
Resume only when Owen says so.

## State on disk (verified by Ferro after the stop)

- build/sweep_building_owner.py adds 29 atoms and is idempotent (rerunning it changes nothing). Backups taken before
  its first run: build/backups/{NY,NYC,US}_pre_sweep.json.
- stage_a_check.py passes: NY.json 221 atoms, NYC.json 192, US.json 178, VA.json 277, cross-file 0 errors. The worker's
  mutation test failed as it should.
- 55 SWEEP_ source files saved under sources/.
- Case walks already reference the new atoms (NY C-walks and NYC C-walks).
- The worker's full transcript is copied to build/sweep_transcript_2026-09-29.log.
- review/NYC_MARKET_RATE.md is unchanged; check_review.py reports the 29 new atoms as not cited (expected until Ferro
  integrates the walk text).
- Ferro has not yet verified any of the 29 atoms.

## The 29 atoms added

NY:RPL-232, NY:ADJ-RPL-232-monthly-letting, NY:ADJ-RPL-232-indefinite-term, NY:ADJ-RPL-232-after-october,
NY:ADJ-RPL-232-agreement-sets-end, NY:ADJ-MDL-rent-bar-not-1-2-family, NY:ADJ-vacate-order-rent,
NY:COMMONLAW-constructive-eviction, NY:RPL-235-a, NY:RPAPL-776-778-administrator, NY:CPLR-6401-foreclosure-receiver,
NY:COMMONLAW-owner-death-agency, NY:RPL-440(1)-rent-collection, NY:RPL-442-d-442-e-unlicensed, NY:RPL-442-f-exemptions,
NY:ADJ-broker-owner-and-staff, NY:HANDOFF-broker-config-collects-rent, NY:HANDOFF-broker-config-settlement-only,
NY:HANDOFF-broker-config-under-broker, NY:HANDOFF-broker-config-collection-agency, NYC:HMC-27-2087-cellar-basement,
NYC:HMC-27-2056.8-lead-turnover, NYC:HMC-27-2017.5-turnover, NYC:HMC-27-2045-detector-charge,
NYC:HMC-27-2128-owner-debt, NYC:HMC-27-2135(c)-receiver-rents, NYC:HMC-27-2147-rent-levy,
US:24CFR982.404(d)(3)-(4), US:11USC541-704-owner-chapter7.

## Not finished

1. Sources fetched but not yet compiled into any atom: RPL 232 decisions (Dodge v Richmond 1st Dept 1958; Futersak v
   Perl Sup Ct 2010 and 2d Dept 2011; Geiger v Braun 1876; Souhami v Brownstone 2d Dept 1919); RPAPL 769 and 770
   (article 7-A proceedings); MDL 34 and 309; RPL 442; NYC Admin. Code 27-2130, 27-2139, 27-2140. Decide each: compile
   it, or record why it changes no decision.
2. The RPL 232 atoms were written before those decisions were read. Recheck them against the decisions.
3. The worker was running case-law searches on receivers, vacate orders and RPL 232 when it stopped.
4. review/SWEEP_BUILDING_OWNER.md is not written: the family enumeration (in or out, why), each atom's controlling
   authority and adjudication, the RPL 232 resolution, over-scope items, and proposed walk text by step.

## To resume

1. Re-dispatch the sweep with its original brief (session 20260928_154206_d435d5, batch deleg_81209247) plus: "Resume
   from review/SWEEP_CHECKPOINT.md. Do not redo the 29 atoms; extend build/sweep_building_owner.py. Start with the
   'Not finished' list, then write the report."
2. Ferro then verifies the atoms against their sources, folds the walk text into review/NYC_MARKET_RATE.md, runs both
   checks, and dispatches the third independent review limited to the round-2 changes and this family.
3. Then Owen's acceptance of Review 1, then the two approved Jev experiments.
