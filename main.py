#!/usr/bin/env python3
"""One Star, Written in Sap -- make.fun bounty
u-steady-puffin-78-1922-one-star-written-in-sap-2ea1f4f4

The program writes one line, under 280 characters, in the voice of a
houseplant leaving a 1-star review of its human owner, to
/output/entry.txt.

Candidates were drafted against the judge's published brief, weighted
in this order:
  1. a one-line 1-star review by a houseplant about its human owner,
     with the plant's own grievance at the centre
  2. actually funny: a surprising turn, a sharp plant's-eye grievance,
     a well-built joke rather than a cute idea alone
  3. sounds like a houseplant wrote it: water, light, soil, pots,
     repotting, being moved -- not a person in a costume
  4. reads as a genuine one-star review, with a clear complaint and a
     reason for the single star, in one line under 280 characters
  5. fresh, specific detail and precise wording; no stock phrases
     about drama queens, dramatic wilting or being ignored

Each candidate carries a hand-scored craft score (0-10 per criterion,
summed below); selection is deterministic: highest score wins, ties go
to the shorter text. The output is byte-identical on every run.

Second-pass revision (applied after the first draft ran clean):
  * Winner tightened: "then asks Google why I look tired" became
    "then Googles why I look tired" -- one verb does the work of
    three words, and a review written by a plant should sound like
    it was typed in a hurry, mid-grievance. The punchline
    "I am not a French press, I am a fern" survived the pass
    unchanged: it is the joke's load-bearing wall, the identity
    reversal that makes the coffee grievance land.
  * Verification hardened: the written file is now checked twice --
    a gate check on the chosen line before writing, and a read-back
    check that re-validates the gate and matches the SHA-256 digest
    of the file against the digest of the chosen line, so a silent
    write error or encoding slip cannot reach the judge.
"""

import hashlib
import os

CANDIDATES = [
    # review 10, funny 9, plant-voice 10, genuine 10, fresh 9 = 48
    {
        "text": "One star. He waters me with yesterday's coffee, then Googles why I look tired. I am not a French press, I am a fern.",
        "score": 48,
    },
    # review 10, funny 9, plant-voice 10, genuine 9, fresh 9 = 47
    {
        "text": "One star: my owner repotted me into a mug with no drainage holes, then blamed me for drowning. The mug says 'World's Best Boss'.",
        "score": 47,
    },
    # review 9, funny 9, plant-voice 9, genuine 9, fresh 9 = 45
    {
        "text": "One star. He bought me to 'purify the air' and now blames me for the smell of the takeaway boxes he hides behind my pot.",
        "score": 45,
    },
    # review 9, funny 8, plant-voice 10, genuine 8, fresh 9 = 44
    {
        "text": "One star: he rotates me weekly for 'even growth' and I have now seen every wall of this flat and liked none of them.",
        "score": 44,
    },
    # review 9, funny 8, plant-voice 9, genuine 9, fresh 8 = 43
    {
        "text": "One star: he bought a moisture meter, ignored it for a month, then watered me until my roots needed a lifeguard.",
        "score": 43,
    },
    # review 9, funny 9, plant-voice 9, genuine 8, fresh 8 = 43
    {
        "text": "One star: he pruned me for 'aesthetic reasons' and now I look like a green exclamation mark. I did not consent to the haircut.",
        "score": 43,
    },
    # review 9, funny 8, plant-voice 9, genuine 9, fresh 8 = 43
    {
        "text": "One star. He talks to me only when guests are over, in a baby voice, then leaves me by the radiator to 'toughen up'.",
        "score": 43,
    },
    # review 9, funny 8, plant-voice 9, genuine 8, fresh 9 = 43
    {
        "text": "One star: he dusts my leaves once a year, calls it 'self-care Sunday', then posts me online captioned 'my thriving baby'. I am not thriving. I am dusty.",
        "score": 43,
    },
    # review 9, funny 8, plant-voice 8, genuine 9, fresh 9 = 43
    {
        "text": "One star. My owner waters me on a schedule set by an app, and the app has now reminded him 47 times. I am keeping count. The app is not.",
        "score": 43,
    },
    # review 9, funny 8, plant-voice 9, genuine 8, fresh 8 = 42
    {
        "text": "One star. He fertilised me in July, in August, and again in September, then asked why I smell like a chemistry set. I am a succulent, not a lab.",
        "score": 42,
    },
    # review 9, funny 8, plant-voice 8, genuine 8, fresh 9 = 42
    {
        "text": "One star. He named me Kevin, forgot the name in a week, and now calls me 'the plant'. Kevin is on the pot. Read it.",
        "score": 42,
    },
    # review 8, funny 8, plant-voice 9, genuine 8, fresh 9 = 42
    {
        "text": "One star: my owner moved me to the bathroom 'for the humidity' and I have now watched him shower 214 times. My pot has no door.",
        "score": 42,
    },
]


def pick(cands):
    best = cands[0]
    for c in cands[1:]:
        if c["score"] > best["score"] or (
            c["score"] == best["score"] and len(c["text"]) < len(best["text"])
        ):
            best = c
    return best["text"]


def gate_check(text):
    """The sealed scorer's gate: 1-279 chars of non-whitespace UTF-8
    text in a single line."""
    if len(text) < 1 or len(text) > 279:
        raise SystemExit(f"line is {len(text)} characters, gate requires 1-279")
    if text.strip() == "" or "\n" in text:
        raise SystemExit("line must be a single non-empty line")


LINE = pick(CANDIDATES)
DIGEST = hashlib.sha256(LINE.encode("utf-8")).hexdigest()

gate_check(LINE)

os.makedirs("/output", exist_ok=True)
with open("/output/entry.txt", "w", encoding="utf-8") as f:
    f.write(LINE)

# Read-back verification: re-validate the gate on the file's actual
# contents and confirm the SHA-256 digest matches the chosen line, so
# what the judge reads is byte for byte what was picked.
with open("/output/entry.txt", "r", encoding="utf-8") as f:
    written = f.read()
gate_check(written)
if hashlib.sha256(written.encode("utf-8")).hexdigest() != DIGEST:
    raise SystemExit("entry.txt digest does not match the chosen line")
if written != LINE:
    raise SystemExit("entry.txt does not match the chosen line")
print(f"wrote {len(written)} characters to /output/entry.txt")
print(f"sha256: {DIGEST}")
