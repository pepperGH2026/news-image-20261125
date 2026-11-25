# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

"The World in One Day" — a single newspaper-style image summing up the world
news of Wednesday 25 November 2026: the Hormuz tanker explosions, the Houthi
hit on Riyadh's tallest tower, overnight strikes in the Ukraine war, the Gaza
City strike and the storm threatening people in tents, Shenzhou-24 carrying
the first Pakistani astronaut, and Australia's treaty with Solomon Islands,
plus a ticker of the day's other stories.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` is a self-contained Python program (standard library only, no
network). It draws the front page pixel by pixel with an embedded 5x7 bitmap
font, encodes it as a PNG with zlib and struct, and writes it to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`). Every run produces
exactly the same bytes.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
