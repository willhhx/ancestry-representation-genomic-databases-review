"""Builds latex/manuscript.tex and manuscript.pdf. Every number in the prose is read from data/extracted_figures.csv or outputs/results.json.
Run after analysis.py:  python3 build_paper.py   (needs pdflatex)"""
import json, os, re, shutil, subprocess
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "outputs"); TEX = os.path.join(HERE, "latex")
df = pd.read_csv(os.path.join(HERE, "data", "extracted_figures.csv")); F = dict(zip(df.key, df.value))
R = json.load(open(os.path.join(OUT, "results.json")))
REPO = "https://github.com/willhhx/ancestry-representation-genomic-databases-review"
def g(k):  # number as written in the source
    v = float(F[k]); return f"{v:,.0f}" if v >= 1000 else (f"{v:g}")
nonEur_now = R["monitor_now_nonEur"]

abstract = (
 "Background: Genetic studies are the evidence base for genomic medicine, but who is included in them determines whom that evidence serves. "
 "Methods: This narrative review draws on 15 verified peer-reviewed articles plus two live data resources, the GWAS Diversity Monitor and the gnomAD database. It summarizes the scale of ancestry imbalance, its documented consequences, where sources agree and disagree, and how strong the evidence is. "
 f"Findings: Across analyses spanning 2009 to 2026, participants of European ancestry make up roughly 80 to 96 percent of genome-wide association study (GWAS) participants, depending on the source and the year. Participants of African, Hispanic or Latin American, and indigenous ancestry together were below 4 percent in a 2016 analysis. As of November 2026 the GWAS Diversity Monitor lists {g('monitor_eur_now')}% European, {g('monitor_asian_now')}% Asian, and {g('monitor_african_now')}% African ancestry. "
 "Studies report that polygenic risk scores predict less accurately in non-European groups (1.6 to 4.9 times lower accuracy in one analysis), that rare-variant interpretation produces longer candidate lists for non-European individuals, and that benign variants were misclassified as pathogenic in patients of African ancestry. "
 "Sources disagree on whether the gap is closing, largely because they count participants differently, and several caution that counts can exaggerate or understate the imbalance. "
 "Conclusions: The imbalance is large and well documented, but the exact numbers are not comparable across sources. Standardized ancestry reporting, tracking of the real performance gap, and sampling beyond diaspora populations are the main open needs."
)
intro = [
 "Genome-wide association studies (GWAS) scan the genomes of many people to find genetic variants linked to diseases and traits. Their results feed into tools used in research and care: polygenic risk scores, which add up the small effects of many variants into one estimate of a person's inherited risk, and reference databases that tell clinicians how common a variant is in the general population and therefore whether it is likely to be harmful. Both depend on who was included in the underlying data.",
 f"Concern about the ancestry makeup of this evidence is not new. A 2009 analysis found that {g('eur_share_2009')} percent of GWAS participants were of European descent, and later reviews have repeatedly returned to that finding (Popejoy & Fullerton, 2016; Sirugo et al., 2019). Yet the scale of the problem, whether it is shrinking, and what it costs patients are described with different numbers in different places. This review asks four questions. How large is the ancestry gap in GWAS and variant databases? What consequences have been documented? Where do sources agree and disagree? And how good is the evidence, and what is missing?",
 "Ancestry in this literature is usually a coarse label (for example European, Asian, or African) assigned by study authors or participants. These labels are imperfect stand-ins for genetic variation, a point several sources make themselves. This review uses the labels as the sources do and flags where that matters.",
]
methods = [
 "This is a narrative review, not a systematic review. It followed no registered protocol and did not use a formal risk-of-bias tool. One reviewer selected the sources.",
 "Candidate sources were identified in November 2026 through targeted searches of Crossref and Europe PMC, starting from the anchor topics set for this review: the GWAS Diversity Monitor, work by Martin and colleagues, Popejoy and Fullerton, Sirugo and colleagues, and the gnomAD database. About 20 candidate sources were examined. Fifteen peer-reviewed articles were kept because they quantified ancestry representation or its consequences, were published in a peer-reviewed journal, and could be verified: every article's title, authors, year, journal, volume, pages, and DOI were confirmed against Crossref, and every figure used in this review was read from the article's abstract or full text or, for the live resources, from the resource itself. Two live resources, the GWAS Diversity Monitor and the gnomAD release notes, were read directly and are cited with their access date. Two older works that the sources build on (the 2009 analysis by Need and Goldstein and a 2011 commentary by Bustamante and colleagues) were located but not read, so they are not cited, and the 2009 figure is reported only as restated by Popejoy and Fullerton (2016).",
 "Figures were recorded in a data file with the source and the location in the source (supplementary file extracted_figures.csv). Arithmetic on those figures, such as differences and ratios, was done by script and is described as the reviewer's own calculation where it appears. Where only an abstract was available, claims are limited to what the abstract states. Quotation was avoided in favor of paraphrase.",
 "Limitations of the method are that other relevant work was probably missed, that sources are dominated by publications indexed in major biomedical databases, and that the data change over time: the live resources were read on 8 November 2026 and will differ later.",
]
scale = {
 "Genome-wide association studies": [
  f"The earliest widely cited figure is the 2009 analysis reporting {g('eur_share_2009')} percent European participants, restated by Popejoy and Fullerton (2016). Their 2016 update of the GWAS Catalog, which then held {g('gwas_catalog_studies_2016')} studies and nearly {g('gwas_catalog_samples_2016_millions')} million samples, found that the share of non-European participants had risen to nearly {g('nonEur_nearly_2016')} percent. They noted that nearly {g('asia_share_of_growth')} percent of the growth in non-European samples came from populations in East, South, and Southeast Asia, and that participants of African, Latin American, Hispanic, or indigenous ancestry together made up less than {g('four_groups_combined_max')} percent of all samples.",
  f"Later analyses agree on the broad picture but report different figures (Table 1). Martin and colleagues (2019) reported that about {g('eur_share_martin')} percent of GWAS Catalog participants were of European descent, in a world where Europeans are about {g('eur_share_global_pop_martin')} percent of the population. Mills and Rahal (2019), in an analysis of {g('mills_studies')} studies from 2005 to 2018, reported {g('eur_share_mills_2017')} percent European participants in 2017 and found that {g('mills_three_country_share')} percent of discoveries came from participants recruited in three countries (the United States, the United Kingdom, and Iceland). Fatumo and colleagues (2022) reported, as of June 2021, {g('eur_share_fatumo_2021')} percent European, {g('ea_share_fatumo_2021')} percent East Asian, {g('afr_share_fatumo_2021')} percent African, {g('sa_share_fatumo_2021')} percent South Asian, and {g('hisp_share_fatumo_2021')} percent Hispanic or Latino participants. Corpas and colleagues (2025) reported {g('eur_share_corpas_2023')} percent European and {g('afr_share_corpas_2023')} percent African (excluding African American and Afro-Caribbean labels) in 2023.",
  f"The GWAS Diversity Monitor, maintained by the Leverhulme Centre for Demographic Science (Mills & Rahal, 2020), tracks the GWAS Catalog continuously. On 8 November 2026 its homepage, set to participants at the discovery stage, listed {g('monitor_eur_now')} percent European, {g('monitor_asian_now')} percent Asian, {g('monitor_aa_now')} percent African American or Afro-Caribbean, {g('monitor_hisp_now')} percent Hispanic or Latin American, {g('monitor_african_now')} percent African, and {g('monitor_other_now')} percent other or mixed ancestry. The categories sum to 100 percent, so about {nonEur_now:g} percent of counted participants are non-European, and all groups other than European and Asian together make up about {R['monitor_now_all_non_asian_non_eur']:g} percent (reviewer's calculation).",
 ],
 "Variant databases": [
  f"Reference databases of human variation show a similar skew. In the Exome Aggregation Consortium data available in 2016, {g('exac_eur')} percent of {g('exac_n')} people with an assigned ancestry were European, {g('exac_sa')} percent South Asian, {g('exac_lat')} percent Latino, {g('exac_afr')} percent African or African American, and {g('exac_ea')} percent East Asian (Petrovski & Goldstein, 2016). Its successor, gnomAD, grew to {g('gnomad2_exomes')} exomes and {g('gnomad2_genomes')} genomes in version 2 (Karczewski et al., 2020), and to {g('gnomad4_total')} individuals in version 4.0, of whom about {g('gnomad4_nonEur_approx')} are described by the gnomAD team as having non-European genetic ancestry (gnomAD Team, 2023). That is about {R['gnomad4_nonEur_share_pct']:g} percent (reviewer's calculation), a much larger absolute number than before but still a minority. The gnomAD team also reports that {g('gnomad4_ukb_exomes')} of the {g('gnomad4_exomes')} exomes in version 4.0 come from a single cohort, the UK Biobank, so one resource shapes much of the database.",
 ],
 "Beyond GWAS": [
  f"Representation gaps extend to pharmacogenomics. Corpas and colleagues (2025) report that {g('pharmgkb_eur')} percent of individuals in studies curated by PharmGKB, a drug-gene knowledge base, are European and {g('pharmgkb_eas')} percent East Asian, and, citing information from the US Food and Drug Administration, that {g('fda_trials_eur')} percent of clinical trial participants from 2015 to 2019 were of primarily European descent. The trial figure is secondhand here and was not checked against the original FDA source. In contrast, the All of Us Research Program released {g('allofus_genomes')} genomes in 2024, of which {g('allofus_underrep_pct')} percent come from communities historically underrepresented in biomedical research, an explicit effort to reverse the pattern (All of Us Research Program Genomics Investigators, 2024).",
 ],
}
conseq = {
 "Polygenic risk scores": [
  f"Martin and colleagues (2019) tested how well scores built from largely European data predict traits in other groups. Relative to the accuracy in Europeans, prediction accuracy averaged {g('prs_fold_hispanic')}-fold lower in Hispanic and Latino Americans, {g('prs_fold_south_asian')}-fold lower in South Asians, {g('prs_fold_east_asian')}-fold lower in East Asians, and {g('prs_fold_african')}-fold lower in Africans. They argue that using such scores clinically today would give European-descent patients more benefit and could widen disparities. Duncan and colleagues (2019) reviewed the first decade of polygenic scoring studies (2008 to 2017) and found that {g('duncan_eur_only')} percent included only European-ancestry participants, {g('duncan_ea_only')} percent only East Asian, and only {g('duncan_afr_hisp_indig')} percent cohorts of African, Hispanic, or indigenous peoples. They also found lower predictive performance in non-European samples, including in samples of African ancestry.",
 ],
 "Variant interpretation and diagnosis": [
  f"Rare-variant interpretation depends on knowing which variants are common in a person's own ancestry group. Using the largest public exome database of its time, Petrovski and Goldstein (2016) found that after removing variants seen in reference data, a European-ancestry person carried on average {g('cand_eur')} candidate variants in disease-associated genes, compared with {g('cand_afr')} for African, {g('cand_lat')} for Latino, {g('cand_ea')} for East Asian, and {g('cand_sa')} for South Asian ancestry. Longer candidate lists make a genetic diagnosis harder. In a clinical example, Manrai and colleagues (2016) found that patients of African or unspecified ancestry received positive genetic test reports for hypertrophic cardiomyopathy based on variants later reclassified as benign, and that the variants most common in the general population were more common among Black Americans than among white Americans. The authors concluded that sequencing diverse populations is needed to interpret variants correctly.",
 ],
 "Research evidence and drug response": [
  "A review of the GWAS Catalog and the database of Genotypes and Phenotypes found significantly fewer studies of African, Latin American, and Asian ancestral populations than of European populations, across both data types and disease areas (Landry et al., 2018). Sirugo and colleagues (2019) argued from empirical and theoretical reasoning that the European bias has implications for disease risk prediction across global populations. These sources document differences in tool performance and in evidence available. They do not by themselves measure differences in patient outcomes, which is a gap discussed below.",
 ],
}
patterns = {
 "Is the gap closing?": [
  f"Sources disagree. Popejoy and Fullerton (2016) reported progress, with the non-European share rising to nearly {g('nonEur_nearly_2016')} percent, though mostly through Asian-ancestry studies. Martin and colleagues (2019) described the non-European fraction as stagnant or declining since late 2014. Fatumo and colleagues (2022) report European share rising from {g('eur_share_fatumo_2016')} percent in 2016 to {g('eur_share_fatumo_2021')} percent in June 2021, and Corpas and colleagues (2025) report a non-European share falling from {g('nonEur_corpas_2016')} percent in 2016 to {g('nonEur_corpas_2021')} percent in 2021 and attribute part of that to repeated use of the same large UK Biobank sample of roughly {int(F['ukb_white_british_n']):,} White British participants. The most recent monitor reading, {g('monitor_eur_now')} percent European, is below the {g('monitor_eur_sep2024')} percent that Corpas and colleagues cite for September 2024, but I could not establish whether that reflects real change or differences in what was counted (stage, metric, or categories).",
  "Taken together, the sources support a cautious statement: non-European representation rose in the early 2010s, largely owing to Asian-ancestry studies, and has not improved steadily since. African, Hispanic or Latin American, and indigenous representation remains very low in every source.",
 ],
 "What counts as representative?": [
  "Sources use different yardsticks. Martin and colleagues compare GWAS participants with global population shares. Corpas and colleagues argue that comparing ancestry shares with global census shares is an insufficient measure of how well global genetic diversity is represented, and note that some populations are proportionally overrepresented relative to both their population size and the genomic diversity of their ancestral haplotypes. They also note that population labels are not genetically coherent or mutually exclusive categories, even though they are useful for tracking trends. Fatumo and colleagues add that the African participants who are included are mostly African Americans, and that more than 90 percent of African ethnolinguistic groups have no representative genetic data, so the small African share overstates coverage of continental African diversity.",
 ],
 "Does diversifying pay off?": [
  "Evidence points to value in diversifying even with smaller samples. Martin and colleagues state that early diversifying efforts show promise even when non-European samples are much smaller than the largest studies. Morales and colleagues (2018), applying a standardized ancestry framework to the GWAS Catalog, found that African and Hispanic or Latin American populations contributed a disproportionately high number of associations relative to their participant counts. This is a descriptive finding about the Catalog and does not show that every new diverse sample will be equally productive, but it argues against assuming that small samples are low value.",
 ],
}
quality = [
 "Ancestry labels are the first weakness. Morales and colleagues (2018) developed their framework because no established guidelines existed for describing sample ancestry, which means published labels vary in detail and definition. Labels are also coarse: grouping all Asian participants, or all African-ancestry participants, hides large differences within groups.",
 f"Counting is the second. The GWAS Diversity Monitor counts a person in every study they appear in, so one person with many measured traits is counted many times. Corpas and colleagues illustrate this with the United Kingdom, where the monitor showed {g('monitor_uk_double_count_millions')} million participants in 2021 for a population of {g('uk_population_millions')} million, about {R['double_count_ratio_uk']:g} times the population (reviewer's calculation from their figures). They suggest this double counting may make diversity look worse than it is in absolute terms, since the number of diverse genomes is growing. Martin and colleagues similarly note that cohorts used in many GWAS are represented many times, which may disproportionately include European cohorts. The direction of the bias in percent shares is therefore uncertain: heavily reused European biobank samples push the European share up, while repeated use of any large diverse cohort would push other shares up.",
 "Third, snapshots differ. Sources draw on the GWAS Catalog at different dates and with different filters (cumulative or yearly, discovery stage or all stages, participants or studies), and the figures in Table 1 are not a single time series. Fourth, most of what is cited here for consequences comes from a small number of analyses, including one UK Biobank and BioBank Japan comparison (Martin et al., 2019) and one exome comparison (Petrovski & Goldstein, 2016). Replication across more datasets would strengthen the case, and the existing evidence concerns predictive accuracy and diagnostic burden, not patient outcomes.",
 "Finally, some sources could be read only in part. For Sirugo and colleagues, Landry and colleagues, and Peterson and colleagues, only the abstracts were available to the reviewer, so claims about them are limited to what the abstracts state.",
]
gaps = [
 f"Several next steps appear across the sources. First, more data from underrepresented populations, collected in ways those populations benefit from. Fatumo and colleagues (2022) set out a roadmap based on their experience establishing genomic studies in diverse global populations, emphasizing sustained global effort toward genomic equity. Large cohorts such as All of Us ({g('allofus_genomes')} genomes, {g('allofus_underrep_pct')} percent from historically underrepresented communities; All of Us Research Program Genomics Investigators, 2024) and the larger non-European share of gnomAD version 4.0 are movement in that direction, although the effect on the gap in practice has not yet been shown in the sources reviewed here.",
 "Second, methods. Peterson and colleagues (2019) summarize analytic approaches for multi-ancestry and admixed cohorts and argue that analyzing diverse data is both feasible and necessary. Third, reporting standards: a common way to describe ancestry, such as the framework of Morales and colleagues (2018), would make counts comparable across studies and over time. Fourth, better metrics. Counting each person once, separating discovery from replication samples, and measuring representation against genetic diversity and not only census share (Corpas et al., 2025) would give a more faithful picture than a single European percentage.",
 "Fifth, outcome evidence. Studies that follow whether narrowing the data gap narrows differences in diagnosis, treatment, or health outcomes are largely absent from the sources reviewed. Sixth, continental coverage: for African ancestry in particular, the available data come mainly from diaspora populations, so recruitment on the African continent is a distinct need from recruitment of African Americans.",
]
conclusion = [
 "Every source reviewed describes genetic studies and reference databases as heavily skewed toward participants of European ancestry, and the documented consequences, lower polygenic score accuracy, longer variant candidate lists, and misclassified variants, fall on the groups least represented. The exact size of the gap and whether it is shrinking depend on how participants are counted, and the sources do not allow a single trend line. The strongest conclusions are the persistent very low representation of African, Hispanic or Latin American, and indigenous participants and the need for standard reporting and better metrics. Evidence on effects on patient outcomes remains to be built.",
]
kt = ("Key takeaway: Genetic studies still draw most of their participants from European-ancestry populations (roughly 80 to 96 percent depending on the source and year), and the groups least represented are the ones for whom risk scores and variant interpretation have been shown to work less well. "
      "The sources disagree on whether the gap is closing because they count participants differently, so no single trend can be trusted, but very low African, Hispanic or Latin American, and indigenous representation is consistent across every source.")

refs = [
 r"All of Us Research Program Genomics Investigators. (2024). Genomic data in the All of Us Research Program. \emph{Nature, 627}(8003), 340--346. \url{https://doi.org/10.1038/s41586-023-06957-x}",
 r"Corpas, M., Pius, M., Vincent, C., Guio, H., Dwek, M., Nagaraj, S., Lopez-Correa, C., Popejoy, A., \& Fatumo, S. (2025). Bridging genomics' greatest challenge: The diversity gap. \emph{Cell Genomics, 5}(1), Article 100724. \url{https://doi.org/10.1016/j.xgen.2024.100724}",
 r"Duncan, L., Shen, H., Gelaye, B., Meijsen, J., Ressler, K., Feldman, M., Peterson, R., \& Domingue, B. (2019). Analysis of polygenic risk score usage and performance in diverse human populations. \emph{Nature Communications, 10}(1), Article 3328. \url{https://doi.org/10.1038/s41467-019-11112-0}",
 r"Fatumo, S., Chikowore, T., Choudhury, A., Ayub, M., Martin, A. R., \& Kuchenbaecker, K. (2022). A roadmap to increase diversity in genomic studies. \emph{Nature Medicine, 28}(2), 243--250. \url{https://doi.org/10.1038/s41591-021-01672-4}",
 r"gnomAD Team. (2023, November 1). \emph{gnomAD v4.0} [Release notes]. Genome Aggregation Database. \url{https://gnomad.broadinstitute.org/news/2023-11-gnomad-v4-0}",
 r"Karczewski, K. J., Francioli, L. C., Tiao, G., Cummings, B. B., Alf\"oldi, J., Wang, Q., Collins, R. L., Laricchia, K. M., Ganna, A., Birnbaum, D. P., Gauthier, L. D., Brand, H., Solomonson, M., Watts, N. A., Rhodes, D., Singer-Berk, M., England, E. M., Seaby, E. G., Kosmicki, J. A., \ldots MacArthur, D. G. (2020). The mutational constraint spectrum quantified from variation in 141,456 humans. \emph{Nature, 581}(7809), 434--443. \url{https://doi.org/10.1038/s41586-020-2308-7}",
 r"Landry, L. G., Ali, N., Williams, D. R., Rehm, H. L., \& Bonham, V. L. (2018). Lack of diversity in genomic databases is a barrier to translating precision medicine research into practice. \emph{Health Affairs, 37}(5), 780--785. \url{https://doi.org/10.1377/hlthaff.2017.1595}",
 r"Manrai, A. K., Funke, B. H., Rehm, H. L., Olesen, M. S., Maron, B. A., Szolovits, P., Margulies, D. M., Loscalzo, J., \& Kohane, I. S. (2016). Genetic misdiagnoses and the potential for health disparities. \emph{New England Journal of Medicine, 375}(7), 655--665. \url{https://doi.org/10.1056/NEJMsa1507092}",
 r"Martin, A. R., Kanai, M., Kamatani, Y., Okada, Y., Neale, B. M., \& Daly, M. J. (2019). Clinical use of current polygenic risk scores may exacerbate health disparities. \emph{Nature Genetics, 51}(4), 584--591. \url{https://doi.org/10.1038/s41588-019-0379-x}",
 r"Mills, M. C., \& Rahal, C. (2019). A scientometric review of genome-wide association studies. \emph{Communications Biology, 2}(1), Article 9. \url{https://doi.org/10.1038/s42003-018-0261-x}",
 r"Mills, M. C., \& Rahal, C. (2020). The GWAS Diversity Monitor tracks diversity by disease in real time. \emph{Nature Genetics, 52}(3), 242--243. \url{https://doi.org/10.1038/s41588-020-0580-y}",
 r"Mills, M. C., \& Rahal, C. (2026). \emph{GWAS Diversity Monitor} [Data set; data last checked by the site 2026-11-03; accessed 2026-11-08]. Leverhulme Centre for Demographic Science. \url{https://www.gwasdiversitymonitor.com/}",
 r"Morales, J., Welter, D., Bowler, E. H., Cerezo, M., Harris, L. W., McMahon, A. C., Hall, P., Junkins, H. A., Milano, A., Hastings, E., Malangone, C., Buniello, A., Burdett, T., Flicek, P., Parkinson, H., Cunningham, F., Hindorff, L. A., \& MacArthur, J. A. L. (2018). A standardized framework for representation of ancestry data in genomics studies, with application to the NHGRI-EBI GWAS Catalog. \emph{Genome Biology, 19}(1), Article 21. \url{https://doi.org/10.1186/s13059-018-1396-2}",
 r"Peterson, R. E., Kuchenbaecker, K., Walters, R. K., Chen, C.-Y., Popejoy, A. B., Periyasamy, S., Lam, M., Iyegbe, C., Strawbridge, R. J., Brick, L., Carey, C. E., Martin, A. R., Meyers, J. L., Su, J., Chen, J., Edwards, A. C., Kalungi, A., Koen, N., Majara, L., \ldots Duncan, L. E. (2019). Genome-wide association studies in ancestrally diverse populations: Opportunities, methods, pitfalls, and recommendations. \emph{Cell, 179}(3), 589--603. \url{https://doi.org/10.1016/j.cell.2019.08.051}",
 r"Petrovski, S., \& Goldstein, D. B. (2016). Unequal representation of genetic variation across ancestry groups creates healthcare inequality in the application of precision medicine. \emph{Genome Biology, 17}(1), Article 157. \url{https://doi.org/10.1186/s13059-016-1016-y}",
 r"Popejoy, A. B., \& Fullerton, S. M. (2016). Genomics is failing on diversity. \emph{Nature, 538}(7624), 161--164. \url{https://doi.org/10.1038/538161a}",
 r"Sirugo, G., Williams, S. M., \& Tishkoff, S. A. (2019). The missing diversity in human genetic studies. \emph{Cell, 177}(1), 26--31. \url{https://doi.org/10.1016/j.cell.2019.02.048}",
]

def esc(s):
    s = s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")
    return s
def paras(l): return "\n\n".join(esc(p) for p in l)
def block(d): return "\n\n".join(f"\\subsection*{{{k}}}\n" + paras(v) for k, v in d.items())

t1 = "\n".join([
 f"2009 analysis, as reported by Popejoy \\& Fullerton (2016) & 2009 & {g('eur_share_2009')} & Reported as the share of participants \\\\",
 f"Popejoy \\& Fullerton (2016) & Aug 2016 & about {100-float(F['nonEur_nearly_2016']):g} & Nearly {g('nonEur_nearly_2016')}\\% non-European; implied \\\\",
 f"Fatumo et al. (2022) & 2016 & {g('eur_share_fatumo_2016')} & GWAS Catalog \\\\",
 f"Mills \\& Rahal (2019) & 2017 & {g('eur_share_mills_2017')} & All GWAS, 2005--2018 \\\\",
 f"Martin et al. (2019) & Report year 2019 & about {g('eur_share_martin')} & GWAS Catalog, cumulative; snapshot date not stated \\\\",
 f"Fatumo et al. (2022) & Jun 2021 & {g('eur_share_fatumo_2021')} & GWAS Catalog \\\\",
 f"Corpas et al. (2025) & 2023 & {g('eur_share_corpas_2023')} & GWAS Catalog \\\\",
 f"GWAS Diversity Monitor, per Corpas et al. (2025) & Sep 2024 & {g('monitor_eur_sep2024')} & Total participants \\\\",
 f"GWAS Diversity Monitor (live) & Nov 2026 & {g('monitor_eur_now')} & Participants, discovery stage \\\\",
])
t2 = "\n".join([
 f"Martin et al. (2019) & Polygenic score accuracy, relative to Europeans & Hispanic or Latino {g('prs_fold_hispanic')}-fold lower; South Asian {g('prs_fold_south_asian')}; East Asian {g('prs_fold_east_asian')}; African {g('prs_fold_african')} \\\\",
 f"Petrovski \\& Goldstein (2016) & Candidate variants per person after filtering & European {g('cand_eur')}; African {g('cand_afr')}; Latino {g('cand_lat')}; East Asian {g('cand_ea')}; South Asian {g('cand_sa')} \\\\",
 f"Duncan et al. (2019) & Polygenic scoring studies, 2008--2017 & {g('duncan_eur_only')}\\% only European; {g('duncan_ea_only')}\\% only East Asian; {g('duncan_afr_hisp_indig')}\\% African, Hispanic, or indigenous \\\\",
])
caption = ("Reported share of European-ancestry participants in GWAS by source and snapshot (panel A) and current ancestry composition in the GWAS Diversity Monitor (panel B). "
           "Panel A combines figures from different sources, datasets, and metrics, so points are not a single time series; the 2019 point is the year of the Martin et al. report because its snapshot date is not stated. "
           "Panel B shows participants at the discovery stage as listed on 8 November 2026 (site data last checked 2026-11-03). Sources: published analyses cited in the text and the GWAS Diversity Monitor (Mills \\& Rahal, 2020).")

tex = r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx,booktabs,url,setspace,caption,amsmath,float,array}
\usepackage[T1]{fontenc}\usepackage{lmodern}\usepackage[hidelinks]{hyperref}\usepackage{xurl}
\captionsetup{font=small,labelfont=bf,justification=justified}
\setstretch{1.15}
\title{Who Is in the Data? Ancestry Representation in Genome-Wide Association Studies and Variant Databases: A Narrative Review}
\author{Haoxi Hu\thanks{Corresponding author: \href{mailto:hu.haoxi@northeastern.edu}{hu.haoxi@northeastern.edu}}\\[2pt]
\small Khoury College of Computer Sciences and Bouv\'e College of Health Sciences,\\
\small Northeastern University}
\date{}
\begin{document}
\maketitle
\vspace{-2em}
\begin{abstract}
""" + esc(abstract) + r"""
\end{abstract}
\noindent\textbf{Keywords:} genomic diversity; genome-wide association studies; ancestry; health disparities; polygenic risk scores; variant databases

\section*{Introduction}
""" + paras(intro) + r"""

\section*{Methods}
""" + paras(methods) + r"""

\section*{Scale of the Gap}
""" + block(scale) + r"""

\begin{table}[H]
\centering\small
\caption{Reported share of European-ancestry participants in genome-wide association studies, by source and snapshot. Sources use different datasets, metrics, and definitions, so rows are not directly comparable.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{p{5.6cm}p{2.4cm}p{2.0cm}p{5.4cm}}
\toprule
Source & Snapshot & European (\%) & Notes \\
\midrule
""" + t1 + r"""
\bottomrule
\end{tabular}%
}
\end{table}

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{figures/figure1_ancestry_representation.png}
\caption{""" + caption + r"""}
\end{figure}

\section*{Documented Consequences}
""" + block(conseq) + r"""

\begin{table}[H]
\centering\small
\caption{Quantified differences reported in three analyses of how ancestry imbalance relates to tool performance or study composition.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{p{4.4cm}p{5.2cm}p{7cm}}
\toprule
Source & Measure & Reported values \\
\midrule
""" + t2 + r"""
\bottomrule
\end{tabular}%
}
\end{table}

\section*{Patterns and Disagreements}
""" + block(patterns) + r"""

\section*{Quality and Limits of the Evidence}
""" + paras(quality) + r"""

\section*{Gaps and Next Steps}
""" + paras(gaps) + r"""

\section*{Conclusion}
""" + paras(conclusion) + r"""

\section*{Data and Code Availability}
{\raggedright The extracted figures with their sources, the scripts that produce the figure and this manuscript, and the verification log are available at \url{""" + REPO + r"""}.\par}

\section*{References}
\begingroup\small\setlength{\parindent}{-0.5in}\setlength{\leftskip}{0.5in}\setlength{\parskip}{4pt}
""" + "\n\n".join(refs) + r"""
\endgroup
\end{document}
"""
os.makedirs(os.path.join(TEX, "figures"), exist_ok=True)
shutil.copy(os.path.join(OUT, "figure1_ancestry_representation.png"), os.path.join(TEX, "figures"))
open(os.path.join(TEX, "manuscript.tex"), "w").write(tex)
for _ in range(2):
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "manuscript.tex"], cwd=TEX, capture_output=True, text=True)
print("pdflatex rc", r.returncode, [l for l in r.stdout.splitlines() if l.startswith("!")][:5])

main = [abstract] + intro + methods + sum(scale.values(), []) + sum(conseq.values(), []) + sum(patterns.values(), []) + quality + gaps + conclusion
wc = sum(len(p.split()) for p in main); wca = len(abstract.split())
allp = " ".join(main) + kt
assert "\u2014" not in allp and "---" not in allp
for bad in ("causes ", "caused by", "leads to", "due to the"):
    assert bad not in allp.lower(), bad
assert wc <= 4000
json.dump({"words_main_text_incl_abstract_excl_tables_figures_refs": wc, "words_abstract": wca, "key_takeaway": kt}, open(os.path.join(OUT, "wordcount.json"), "w"), indent=1)
print("main words", wc, "abstract", wca)
