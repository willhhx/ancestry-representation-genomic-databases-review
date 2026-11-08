# Who is in the data? Ancestry representation in GWAS and variant databases

Narrative literature review prepared for the Emory University Journal of Public Health (Literature Review).

## Contents
- `latex/manuscript.tex`, `latex/manuscript.pdf`: the review
- `data/extracted_figures.csv`: every figure used, with its source, DOI or URL, and where it was found
- `outputs/results.json`, `results.csv`: derived numbers (differences, ratios, consistency checks)
- `outputs/figure1_ancestry_representation.png`: Figure 1 (300 dpi)
- `verification.md`: citation checks (Crossref), figure traceability, known discrepancies, word count

## Reproduce
```
python3 analysis.py            # derived numbers + figure (pandas, matplotlib)
python3 build_paper.py         # manuscript.tex + PDF (needs pdflatex)
python3 build_verification.py
```

## Notes
The live resources (GWAS Diversity Monitor, gnomAD release notes) were read on 2026-11-08 and change over time. Percentages from different sources use different datasets and definitions and are not one time series.
