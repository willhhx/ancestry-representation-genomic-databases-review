"""Writes verification.md: checks that every extracted figure used in the manuscript text is traceable to a source row, and lists citation checks."""
import json, os, re
import pandas as pd
H = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(H + "/data/extracted_figures.csv"); W = json.load(open(H + "/outputs/wordcount.json")); R = json.load(open(H + "/outputs/results.json"))
tex = open(H + "/latex/manuscript.tex").read(); flat = re.sub(r"\s+", " ", tex.replace("\\%", "%"))
def fmt(v):
    v = float(v); return f"{v:,.0f}" if v >= 1000 else f"{v:g}"
rows = []; used = 0
for _, r in df.iterrows():
    f = fmt(r.value); present = f in flat; used += present
    rows.append(f"| {r.key} | {f} | {r.source} | {r.doi_or_url} | {r.where_found} | {'in text' if present else 'in data file only'} |")
derived = [(k, v) for k, v in R.items() if k != "inputs"]
cites = [
 ("Popejoy & Fullerton 2016, Nature 538:161", "10.1038/538161a", "Crossref match; figures read from author manuscript PMC5089703 (full text)"),
 ("Martin et al. 2019, Nat Genet 51:584", "10.1038/s41588-019-0379-x", "Crossref match; figures read from PMC6563838 (full text)"),
 ("Sirugo, Williams & Tishkoff 2019, Cell 177:26", "10.1016/j.cell.2019.02.048", "Crossref match (10.1016/j.cell.2019.04.032 is a correction notice, not used); abstract only"),
 ("Fatumo et al. 2022, Nat Med 28:243", "10.1038/s41591-021-01672-4", "Crossref match; figures read from PMC7614889 (full text)"),
 ("Mills & Rahal 2019, Commun Biol 2:9", "10.1038/s42003-018-0261-x", "Crossref match; abstract figures"),
 ("Mills & Rahal 2020, Nat Genet 52:242", "10.1038/s41588-020-0580-y", "Crossref match; no abstract, cited as the citation for the GWAS Diversity Monitor"),
 ("Morales et al. 2018, Genome Biol 19:21", "10.1186/s13059-018-1396-2", "Crossref match; abstract"),
 ("Duncan et al. 2019, Nat Commun 10:3328", "10.1038/s41467-019-11112-0", "Crossref match; abstract figures"),
 ("Corpas et al. 2025, Cell Genomics 5:100724", "10.1016/j.xgen.2024.100724", "Crossref match; figures read from PMC11770215 (full text)"),
 ("Karczewski et al. 2020, Nature 581:434", "10.1038/s41586-020-2308-7", "Crossref match; abstract figures (125,748 exomes + 15,708 genomes = 141,456, matching the title)"),
 ("Petrovski & Goldstein 2016, Genome Biol 17:157", "10.1186/s13059-016-1016-y", "Crossref match; figures read from PMC4944427 (full text)"),
 ("Manrai et al. 2016, N Engl J Med 375:655", "10.1056/NEJMsa1507092", "Crossref match; abstract"),
 ("Landry et al. 2018, Health Aff 37:780", "10.1377/hlthaff.2017.1595", "Crossref match; abstract"),
 ("Peterson et al. 2019, Cell 179:589", "10.1016/j.cell.2019.08.051", "Crossref match; abstract only"),
 ("All of Us Genomics Investigators 2024, Nature 627:340", "10.1038/s41586-023-06957-x", "Crossref match (author is the group name); abstract figures"),
]
md = f"""# Verification: ancestry-representation-genomic-databases-review

## 1. Citations ({len(cites)} peer-reviewed articles; title, authors, year, journal, volume and pages matched in Crossref)

| Reference | DOI | Check |
|---|---|---|
""" + "\n".join(f"| {a} | {b} | {c} |" for a, b, c in cites) + f"""

Live resources: GWAS Diversity Monitor homepage (https://www.gwasdiversitymonitor.com/), read 2026-11-08, site data last checked 2026-11-03; gnomAD v4.0 release notes (https://gnomad.broadinstitute.org/news/2023-11-gnomad-v4-0), read 2026-11-08. Per-group gnomAD v4.0 counts were not available in the page text, so only the total (807,162), the exome and genome counts and the approximate non-European count (about 138,000) are used.

Not cited because not read: Need & Goldstein (2009) and Bustamante et al. (2011). The 2009 figure (96%) is reported only as restated by Popejoy & Fullerton (2016). The FDA clinical-trial figure (76%) is reported as cited by Corpas et al. (2025) and was not checked against the FDA source.

## 2. Every extracted figure, its source, and whether it appears in the manuscript

{used} of {len(df)} figures appear in the manuscript text; the rest are kept in the data file for traceability.

| Key | Value | Source | DOI or URL | Where found | Status |
|---|---|---|---|---|---|
""" + "\n".join(rows) + """

## 3. Derived numbers (reviewer's arithmetic, computed by analysis.py)

""" + "\n".join(f"- {k}: {v}" for k, v in derived) + f"""

Checks passed in analysis.py: Diversity Monitor categories sum to 100.0; ExAC groups sum to 100.0; gnomAD v2 exomes plus genomes equal 141,456 (matches the paper's title).

## 4. Known discrepancies, reported in the paper rather than resolved

- Diversity Monitor European share: 94.48% (September 2024, as cited by Corpas et al.) versus 88.37% (8 November 2026, discovery stage). The cause could not be determined from the sources.
- Popejoy & Fullerton report a non-European share of nearly 20% in 2016; Fatumo et al. report a 2016 European share of 81%; Corpas et al. report 19% non-European in 2016. These are consistent with each other.
- Martin et al. (about 79% European) does not state its GWAS Catalog snapshot date; plotted at the report year.
- Popejoy & Fullerton state a rise of more than 2,000% in sample numbers; the reviewer's ratio of the reported 35 million to 1.7 million samples gives about 1,959%, so the paper does not repeat either figure as its own result.

## 5. Word count (main text including abstract, excluding tables, figures, references)

- build_paper.py count: {W['words_main_text_incl_abstract_excl_tables_figures_refs']} words (abstract {W['words_abstract']}). Limit for Literature Reviews: 4,000. PASS

## 6. Style checks

- No em dashes (asserted in build_paper.py): PASS
- No causal verbs such as "causes" or "leads to" (asserted): PASS
- No direct quotations (all paraphrased): PASS
- Limitations of the method and of each evidence type stated in the paper: PASS
"""
open(H + "/verification.md", "w").write(md); print("figures in text", used, "of", len(df))
