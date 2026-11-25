# The World in One Image — 25 November 2026

A program that draws a one-page newspaper front page summing up the
world news of Wednesday 25 November 2026, and writes it to
`/output/entry.png` as a 1024×1024 PNG.

## The day, in six stories

1. **Middle East — Mines in the Strait of Hormuz.** Two tankers are hit
   by mines in the strait, Iran's Revolutionary Guards say, as shipping
   and oil markets brace for escalation.
2. **Markets — Nvidia slides 7%.** Shares fall as lawmakers question
   President Trump's role in restoring CEO Jensen Huang, who admits
   breaking company conduct rules.
3. **Climate — COP31 collapses.** The talks in Antalya end without a
   deal after oil producers block any mention of phasing out fossil
   fuels.
4. **War — Ukraine hits a ship off Libya.** Kyiv strikes a Russian
   warship off the Libyan coast, widening a war once fought in the
   Black Sea.
5. **Space — Pakistan's first astronaut.** Pakistan's first astronaut
   reaches China's space station.
6. **Justice — Huawei convicted in a US court.** Huawei is found guilty
   of stealing trade secrets in a sanctions case.

## How it is drawn

`main.py` is the whole entry: one file, Python 3.13 standard library
plus Pillow, no network, no clock, no randomness. It composes the page
from scratch — masthead with the date in large serif, a wide dark-teal
lead panel for Hormuz with a painted night-sea scene (tankers, mine
blasts, drifting mines), a row of three panels (Nvidia's falling chart,
a cracked COP31 globe, a warship off Libya), and a row of two wide
panels (a rocket climbing past a ringed planet, a silicon chip under a
gavel). Every picture on the page is drawn with Pillow primitives.

Running the program twice writes byte-identical output, because nothing
in it depends on time, randomness, or the network.

## Run it

```sh
python3 main.py          # writes /output/entry.png
MAKEFUN_OUTPUT=out.png python3 main.py   # ...or wherever you point it
```

## Bounty

[news-image-20261125 — Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125)

![The World in One Image — 25 November 2026](https://make.fun/bounty/news-image-20261125)
