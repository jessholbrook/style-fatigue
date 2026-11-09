# Measuring style fatigue where it actually happens

**Research design memo** · Status: adopted — recruitment for the controlled study is paused

Run the noticeability item continuously in Sprig. Save the controlled study for the question only it can answer.

## Recommendation

1. **Field one non-comparative item continuously in Sprig** — always-on, not a campaign timed to a launch. The continuity is the whole method, not an implementation detail.
2. **Use an optional open-text follow-up** to learn which style dimensions people name unprompted. That input is what we're missing, and a good controlled study needs it in order to exist.
3. **Keep the controlled study and run it third**, on the two or three dimensions the open text surfaces, as single-dimension variants rather than bundles.

## Why re-sequence

The built study randomizes people into two *bundles* of style changes — formality, formatting, punctuation and several others moving together. Run perfectly, it tells us people detected bundle A at some rate. It can't tell us which dimension drove the detection, because nothing in the design varies one dimension at a time.

It also can't see harm. "Harmful habituation" is a claim about consequences — people quietly stopping using the product for something they used to rely on it for. That shows up in retention and task abandonment over months. It doesn't show up in a satisfaction item after a five-turn conversation about an assigned topic.

Both problems point the same way: we're being rigorous about a question we haven't yet earned the right to ask. Designing single-dimension variants requires knowing which dimensions register with people at all. That's a discovery problem, and in-product open text solves it cheaply, at a scale no panel will match.

## The instrument

Two questions. The first runs on every impression and produces the time series; the second is optional and produces the taxonomy.

| | Wording | Format |
|---|---|---|
| Item 1 (always on) | How much did the way Claude wrote stand out to you today? | 7-point, *Not at all* → *Very much* |
| Item 2 (optional) | If anything stood out, what was it? An example helps. | Open text |

**Why not "how AI-like did the answers feel?"** Two reasons, both fatal to a time series. It conflates style with quality: a wrong or hedged answer reads as "more AI-like," so the item absorbs every unrelated regression we ship. And its referent drifts: what counts as AI-sounding changes as the whole market changes, so a rising line would measure the discourse about AI rather than our writing. The wording above is non-comparative, so it doesn't prime people to hunt for changes, and it asks about the text rather than about the machine.

> Item 1 already exists. It's `notice_change` in [`experiment/survey_instruments/post_conversation.json`](../experiment/survey_instruments/post_conversation.json), written for the controlled study. Using identical wording in both venues means the in-product series and the eventual lab study share an instrument.

## Fielding rules

This is the part that's easy to get wrong, and getting it wrong can't be fixed after the fact.

- **Continuous, not campaign.** Sprig studies usually run as bursts around a launch. A burst is worthless here — without the pre-period there's nothing to compare the post-period to.
- **Random sample of eligible sessions.** Never trigger on thumbs-down, regeneration or error states. Those are the most tempting triggers, and each one guarantees the sample comes from people who are already unhappy.
- **Frequency cap of roughly one impression per person per 30 days.** Stops a small pool of repeat responders from carrying the series, and stops people habituating to the survey itself.
- **Freeze wording and targeting for the life of the series.** Any mid-flight edit to either one severs before from after. A new question ships as a second study.
- **Log the release calendar next to the responses.** Model and prompt changes are the intervention points; without dated releases the series can't be read.

## Continuous fielding *is* the control arm

The strongest objection to going in-product is that there's no control group: everyone gets the same model, so when 30% say the writing stood out, there's no denominator. The always-on design answers that. The weeks when nothing shipped *are* the ambient baseline — what people say when, by construction, nothing changed.

```
 Item 1 mean
   │                    ┆●  detection
   │                    ┆ ╲
   │                    ┆  ╲___   decay back to baseline = habituation
   │ ░░░░░░░░░░░░░░░░░░░┆░░░░░▔▔▔‾‾‾─────░░░░░  ambient baseline band
   │ ‾─_─‾─_─‾─_─‾─_─‾─_┆
   └────────────────────┼──────────────────────── weeks
                  style change ships
```

One continuously fielded question yields three quantities: the ambient rate, the size of the detection spike, and the shape of the decay back to baseline. That decay is the habituation curve — what the longitudinal study was built to produce — measured against real usage instead of assigned topics.

This is weaker than randomization in one specific way: ambient events can move the baseline. A competitor launch or a viral thread about AI writing tics will lift the line without anything of ours changing. Randomization would absorb that; a time series can't. The mitigation is mundane: watch for level shifts that don't line up with our releases, and note external events as they happen.

## How much traffic this needs

Assuming a standard deviation near 1.6 on the 7-point item, comparing the post-release window against a baseline built from many prior weeks:

| Shift to detect | Effect size | Responses needed | Impressions at 10% response |
|---|---|---|---|
| +0.20 points | d = 0.13 | ~1,020 | ~10,200 |
| **+0.30 points** | **d = 0.19** | **~450** | **~4,500** |
| +0.50 points | d = 0.31 | ~165 | ~1,650 |

The middle row is the target. At weekly resolution that's roughly 4,500 impressions a week. If we can't clear it, move to biweekly or monthly buckets rather than raising the sampling rate — oversampling burns the frequency cap and degrades the panel.

## The harm question needs a join, not a survey

Item 1 tells us people noticed. It can't tell us whether noticing mattered. For that, responses need to join to behavior: retention over the following weeks, session length, task abandonment, whether someone stops using the product for a category they used to.

In practice, Sprig responses need to land in the warehouse alongside product analytics, keyed to a stable user ID, with a 30–90 day forward window. Confirm this early. Without that join the benefit-versus-harm question stays unanswered however good the survey is, and we should know that before fielding.

## What stays in the controlled study

One thing genuinely requires randomization: the false-positive rate under a *known* change — the share of people who report a difference when we can prove nothing changed for them. The in-product baseline approximates this but can't separate it from ambient drift. That's what the control arm's pseudo-shift marker was built for, and it's still worth running once we know which dimensions to point it at.

The repository is finished, tested and deployable. It becomes the Phase 3 instrument. No further work on the forced-shift fallback or the demo until Phase 2 says which dimensions to encode.

## Sequence

1. **Field the always-on item** (weeks 1–2 to set up, then indefinite). Both questions live in Sprig under the fielding rules above. The first weeks produce nothing to analyze, and that's the point — the pre-period is the deliverable.
2. **Code the open text into a dimension taxonomy** (from about week 6, ongoing). Sprig's theming gets most of the way; hand-code a sample against the seven candidate dimensions already in the study — formulaicness, repetition, punctuation, formality, formatting, slang, trend-chasing — and let unexpected themes extend the list. Output: a ranked list of what people actually name.
3. **Run the controlled study on the top dimensions** (after Phase 2 reports). Rebuild the style profiles as single-dimension variants, one per arm, in the existing app. Re-open enrollment by setting `enrollment_open` to `true` in [`experiment/config.json`](../experiment/config.json).

## What would change this plan

- **The warehouse join isn't available.** The in-product arm then only answers detection, not harm, and the case for it weakens considerably.
- **Traffic is below ~4,500 impressions a week even with monthly buckets.** The series is then too noisy to read, and the controlled study is the better instrument despite its narrower question.
- **Style ships as continuous drift, not dated releases.** An interrupted time series needs interruptions. Without discrete change points, the approach collapses back to the lab.

---

*Sprig specifics are written as requirements, not configuration. Confirm sampling, frequency capping, open-text theming and warehouse export against our actual plan before committing to the timeline.*
