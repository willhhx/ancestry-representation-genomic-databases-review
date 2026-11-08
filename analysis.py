"""Project 4 (narrative literature review): turns data/extracted_figures.csv (every figure was read from a cited source)
into derived numbers (outputs/results.json) and Figure 1 (outputs/figure1_ancestry_representation.png).
Run: python3 analysis.py     Needs: pandas, matplotlib."""
import json, os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "outputs"); os.makedirs(OUT, exist_ok=True)
df = pd.read_csv(os.path.join(HERE, "data", "extracted_figures.csv")); F = dict(zip(df.key, df.value))
R = {"inputs": {k: float(v) for k, v in F.items()}}

# ---- derived numbers and internal consistency checks
mon = ["monitor_eur_now", "monitor_asian_now", "monitor_african_now", "monitor_aa_now", "monitor_hisp_now", "monitor_other_now"]
R["monitor_now_sum"] = round(sum(F[k] for k in mon), 2); assert abs(R["monitor_now_sum"] - 100) < 0.05
R["monitor_now_nonEur"] = round(100 - F["monitor_eur_now"], 2)
R["monitor_now_all_non_asian_non_eur"] = round(100 - F["monitor_eur_now"] - F["monitor_asian_now"], 2)
R["exac_sum"] = round(sum(F[k] for k in ["exac_eur", "exac_sa", "exac_lat", "exac_afr", "exac_ea"]), 1)
R["fatumo_2021_listed_sum"] = round(sum(F[k] for k in ["eur_share_fatumo_2021", "ea_share_fatumo_2021", "afr_share_fatumo_2021", "sa_share_fatumo_2021", "hisp_share_fatumo_2021"]), 2)
R["nonEur_fatumo_2016"] = round(100 - F["eur_share_fatumo_2016"], 1)
R["nonEur_fatumo_2021"] = round(100 - F["eur_share_fatumo_2021"], 1)
R["nonEur_corpas_2023"] = round(100 - F["eur_share_corpas_2023"], 1)
R["gnomad4_nonEur_share_pct"] = round(100 * F["gnomad4_nonEur_approx"] / F["gnomad4_total"], 1)
R["gnomad2_total"] = int(F["gnomad2_exomes"] + F["gnomad2_genomes"])
R["gnomad4_ukb_share_of_exomes_pct"] = round(100 * F["gnomad4_ukb_exomes"] / F["gnomad4_exomes"])
R["double_count_ratio_uk"] = round(F["monitor_uk_double_count_millions"] / F["uk_population_millions"], 1)
R["cand_ratio_sa_vs_eur"] = round(F["cand_sa"] / F["cand_eur"], 2)
R["cand_ratio_afr_vs_eur"] = round(F["cand_afr"] / F["cand_eur"], 2)
R["martin_eur_minus_global_pop_pp"] = round(F["eur_share_martin"] - F["eur_share_global_pop_martin"], 0)
json.dump(R, open(os.path.join(OUT, "results.json"), "w"), indent=1)
pd.Series({k: v for k, v in R.items() if k != "inputs"}).to_csv(os.path.join(OUT, "results.csv"), header=["value"])

# ---- Figure 1 (Okabe-Ito colorblind-safe palette)
BL, OR, GR, VM = "#0072B2", "#D55E00", "#009E73", "#CC79A7"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(1, 2, figsize=(13, 5.6), gridspec_kw={"width_ratios": [1.15, 1]})
pts = {  # label: (year, value)
 "Published analyses of the GWAS Catalog": [(2009, F["eur_share_2009"], "Popejoy &\nFullerton 2016\n(2009 analysis)"), (2016, F["eur_share_fatumo_2016"], ""), (2019, F["eur_share_martin"], "Martin\n2019"), (2021, F["eur_share_fatumo_2021"], ""), (2023, F["eur_share_corpas_2023"], "")],
 "Scientometric review (Mills & Rahal 2019)": [(2017, F["eur_share_mills_2017"], "")],
 "GWAS Diversity Monitor": [(2024, F["monitor_eur_sep2024"], "Sept 2024\n(per Corpas\net al. 2025)"), (2026, F["monitor_eur_now"], "Nov 2026\n(discovery stage)")],
}
mk = {"Published analyses of the GWAS Catalog": ("o", BL), "Scientometric review (Mills & Rahal 2019)": ("s", OR), "GWAS Diversity Monitor": ("D", GR)}
a = ax[0]
for name, p in pts.items():
    m, c = mk[name]; a.scatter([x[0] for x in p], [x[1] for x in p], marker=m, color=c, s=70, label=name, zorder=3)
for name, p in pts.items():
    for x, y, t in p:
        a.annotate(f"{y:g}%", (x, y), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9)
a.set_ylim(60, 102); a.set_xlim(2007, 2028); a.set_xticks([2009, 2012, 2015, 2018, 2021, 2024, 2027])
a.set_xlabel("Year of the report or data snapshot"); a.set_ylabel("Participants of European ancestry (%)")
a.set_title("A. Reported European share of GWAS participants", loc="left", fontsize=12)
a.grid(axis="y", color="#e6e6e6", zorder=0); a.legend(loc="lower left", fontsize=9, frameon=False)
b = ax[1]
labs = ["European", "Asian", "African American or\nAfro-Caribbean", "Hispanic or\nLatin American", "Other or mixed", "African"]
vals = [F["monitor_eur_now"], F["monitor_asian_now"], F["monitor_aa_now"], F["monitor_hisp_now"], F["monitor_other_now"], F["monitor_african_now"]]
cols = [BL, OR, GR, VM, "#999999", "#E69F00"]
y = range(len(labs))[::-1]; b.barh(list(y), vals, color=cols, zorder=3)
for yy, v in zip(y, vals): b.text(v + 1, yy, f"{v:g}%", va="center", fontsize=10)
b.set_yticks(list(y)); b.set_yticklabels(labs); b.set_xlim(0, 100); b.set_xlabel("Share of GWAS participants (%)")
b.set_title("B. Composition now (Diversity Monitor)", loc="left", fontsize=12); b.grid(axis="x", color="#e6e6e6", zorder=0)
fig.text(.01, .005, "Sources: values extracted from the cited publications and the GWAS Diversity Monitor (https://www.gwasdiversitymonitor.com/, data last checked by the site 2026-11-03; read 2026-11-08). "
         "Sources use different datasets, metrics and category definitions, so points are not a single continuous series.", fontsize=8, color="#555555", wrap=True)
fig.tight_layout(rect=(0, .05, 1, 1)); fig.savefig(os.path.join(OUT, "figure1_ancestry_representation.png"), dpi=300); plt.close(fig)
print("ok", {k: v for k, v in R.items() if k != "inputs"})
