# Exoplanet Habitability Pipeline

A three-tier scoring pipeline for ranking potentially habitable exoplanets using data from the NASA Exoplanet Archive. Extends the standard Earth Similarity Index approach with Habitable Zone Distance normalization and SEPHI scoring, then introduces a Tidally Locked Habitability Index (TLHI) for planets around M-dwarf stars.

---

## Overview

Most habitability rankings stop at the Earth Similarity Index (ESI). This pipeline adds two more dimensions — where a planet sits *within* its habitable zone, and how likely it is to be statistically habitable — before combining them into a single final score using a geometric mean. Phase 2 then computes tidal locking probability and applies a modified index for planets that are likely tidally locked.

---

## Pipeline

```
NASA Exoplanet Archive
        │
        ▼
 Radius filter          →  Remove radius > 1.6 R⊕ (Fulton gap; likely sub-Neptunes)
        │
        ▼
 Tier 1 — ESI           →  Remove ESI < 0.75 (too unlike Earth in structure)
        │
        ▼
 Tier 2 — HZD           →  Remove HZD_norm < 0.71 (near zone edges)
        │
        ▼
 Tier 3 — SEPHI         →  Statistical Likelihood Exo-Planetary Habitability Index
        │
        ▼
 Final Score = (ESI × HZD_norm × SEPHI)^(1/3)
        │
        ▼
 Ranked candidates
```

### Phase 1 — Core scoring

| Step | Formula / Threshold |
|---|---|
| Radius filter | `pl_rade < 1.6 R⊕` |
| ESI | Standard ESI formulation; keep `ESI ≥ 0.75` |
| HZD normalization | `HZD_norm = (1 − \|HZD\|)^0.5`; keep `HZD_norm ≥ 0.71` |
| SEPHI | Statistical Likelihood Exo-Planetary Habitability Index (SEPHI, not SEPHI 2.0 — latter requires eccentricity and rotation period data unavailable for most candidates) |
| Final score | `(ESI × HZD_norm × SEPHI)^(1/3)` — geometric mean penalizes weak scores on any single dimension |

---

## Results

Top candidates from the Phase 1 pipeline (NASA Exoplanet Archive, Planetary System Composite Data):

| S No | Planet Name | ESI | HZD | SEPHI | Combined Score | Tidal Lock |

| --- | --- | --- | --- | --- | --- |

| 0 | GJ 1061 d | 0.873787 | 0.999570 | 0.927434 | 0.932182 | ✅ Locked |

| 1 | GJ 667 C f | 0.835860 | 0.968433 | 0.967638 | 0.921805 | ⚠️ Likely Locked |

| 2 | Kepler-442 b | 0.912707 | 0.826603 | 0.962354 | 0.898782 | ❌ Not Locked |

| 3 | Wolf 1069 b | 0.974170 | 0.895218 | 0.815817 | 0.892727 | ✅ Locked |

| 4 | TRAPPIST-1 e | 0.951359 | 0.903434 | 0.755585 | 0.865980 | ✅ Locked |

| 5 | Proxima Cen b | 0.889379 | 0.909200 | 0.801853 | 0.865527 | ✅ Locked |

| 6 | GJ 1002 b | 0.926202 | 0.864048 | 0.796679 | 0.860681 | ✅ Locked |

| 7 | TOI-715 b | 0.854830 | 0.807265 | 0.905702 | 0.854989 | ✅ Locked |

7 of the 8 top-ranked planets are around M-dwarf stars and are tidally locked or very likely so. Kepler-442 b (K-dwarf, 112-day orbit) is the lone exception — and the only one with Earth-like day-night cycles. This observation directly motivates the TLHI extension.

---

## Installation

```bash
git clone https://github.com/ShankarSrivathsa/exoplanet-habitability.git
cd exoplanet-habitability
pip install -r requirements.txt
```

Then open `notebook.ipynb` in Jupyter.

---

## Data

This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.

---

## Author

**A Shankar Srivathsa** — Final year, CSE (AI & ML), Geethanjali College of Engineering and Technology.
Working toward ML engineering with astrophysics domain expertise.
Open to collaboration on exoplanet characterization, astrobiology, and ML-for-astronomy.
