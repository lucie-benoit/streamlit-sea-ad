import streamlit as st
from utils.prep import filtered
from utils.io import load_csv
from utils.visualizations import at8_scatter_by_dementia,  at8_vs_adnc, abeta_vs_adnc, correlation_heatmap_pathology, neun_vs_adnc, neun_vs_at8



def app(df) :

    df = load_csv()
    df_filtered = filtered(df)

    st.title("Brain pathology in Alzheimer’s disease (MTG)")

    # ================= Context: brain region =================
    st.info(
        """ 
        The middle temporal gyrus (MTG) is a brain region involved in language and memory and is known to be particularly vulnerable in Alzheimer’s disease.

        It represents a transition zone where early tau pathology progresses toward widespread cortical involvement associated with dementia, making it an ideal region to study disease progression at the tissue and cellular levels."""
    )


    # ================= What is measured =================
    st.header("Neuropathological features measured in the MTG")
    st.info("""
        Measurements of Abeta, pTau, pTDP43, a-synuclein, Neun+ cells, IBA1+ cells, and GFAP+ cells from quantitative analysis of stained neuropathology images from Middle Temporal Gyrus (MTG).
    """)

    st.markdown("""
    - **Amyloid-β (Aβ)** and **phosphorylated tau (pTau)** reflect the core protein aggregates
      that define Alzheimer’s disease.
    - **NeuN+ cells** provide an estimate of neuronal integrity.
    """)

    st.markdown("""
    We first examine the distribution of key neuropathological markers measured
    in the middle temporal gyrus across the SEA-AD donor cohort.

    These features capture distinct biological processes, including protein aggregation,
    neuronal loss, and glial activation.
    """)

    st.subheader("Phosphorylated tau vs dementia status")

    st.markdown(
        """ **Phosphorylated tau (pTau) pathology** was quantified using **AT8 immunostaining**, a widely used marker of tau phosphorylation in Alzheimer’s disease. 
        AT8-positive area therefore serves as a proxy for pTau burden throughout this analysis.
        """)
    st.info(
        """
        Donors with low or no AD neuropathological change (ADNC) show low AT8 values,
        whereas intermediate and high ADNC groups exhibit higher values and greater
        inter-donor variability.
        """
    )

    st.caption(
        """ AT8-positive area (% of grey matter) is shown across AD neuropathological
        change (ADNC) categories. Each point represents one donor, with AT8-positive area (% of grey matter)
        shown according to dementia status.
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("AT8 by dementia")
        at8_scatter_by_dementia(df_filtered)

    with col2:
        st.subheader("AT8 by ADNC")
        at8_vs_adnc(df_filtered)

    st.markdown(
        """
        Donors with dementia display a broader range of AT8 values compared to donors
        without dementia, with partial overlap between the two groups.
        This pattern is consistent with observations reported in the SEA-AD study,
        where pTau burden varies across individuals and does not uniquely define
        clinical dementia status.
        """
    )
    
    st.subheader("Aβ plaque burden (6E10) across ADNC stages")
    st.info(
        """ **Amyloid-β (Aβ) pathology** was quantified using **6E10 immunostaining**, a widely used marker of Aβ plaques in Alzheimer’s disease. 
        6E10-positive area therefore serves as a proxy for Aβ burden throughout this analysis.
        """)
    abeta_vs_adnc(df_filtered)

    st.markdown(
        """
        To mirror the analysis presented in the SEA-AD study, we computed a correlation matrix across quantitative neuropathological markers.
        Consistent with Figure 2c of the original study, core Alzheimer’s disease pathologies (pTau and Aβ) cluster together, while pTDP-43 and α-synuclein show weaker and more heterogeneous associations, reflecting their role as frequent but non-systematic comorbid pathologies.
        """
    )
    st.subheader("Correlation heatmap of pathology markers (Spearman)")
    st.markdown("""
    This correlation matrix highlights the relationships among key neuropathological
    features measured in the middle temporal gyrus.
    Strong positive correlations are observed between core Alzheimer’s disease
    pathologies—phosphorylated tau (pTau) and amyloid-β (Aβ)—consistent with their
    co-accumulation during disease progression. In contrast, pTDP-43 and α-synuclein exhibit weaker
    and more variable associations with other markers, reflecting their status as
    common but non-obligate comorbid pathologies in Alzheimer’s disease.
    These findings align with prior observations from the SEA-AD study,
    underscoring the complex interplay of neuropathological processes in Alzheimer’s disease.
    """)
    correlation_heatmap_pathology(df_filtered)

    
    # ================= Neun vs ADNC and AT8 ====================================
    st.subheader("Neuronal integrity across ADNC and pTau burden")
    st.info(
        """NeuN immunoreactivity provides an estimate of neuronal integrity, 
        allowing us to assess how neuronal loss relates to increasing Alzheimer’s pathology.
        """
    )

    st.markdown("""
    Neuronal integrity, as estimated by NeuN immunoreactivity, declines progressively
    with increasing ADNC stages and pTau burden, consistent with the expected loss of
    neurons in Alzheimer’s disease. This pattern mirrors findings from the SEA-AD study,
    where neuronal loss correlates with advancing neuropathological severity.
    """)

    neun_vs_adnc(df_filtered)
    st.markdown("""NeuN immunoreactivity decreases across increasing ADNC categories and shows a negative association with AT8-positive pTau burden, 
                consistent with patterns reported in the SEA-AD quantitative neuropathology analyses.
                """)
    
    neun_vs_at8(df_filtered)
    st.markdown("""NeuN immunoreactivity is negatively associated with pTau burden measured by AT8, 
                consistent with the anti-correlation between neuronal integrity and Alzheimer’s disease protein pathologies reported in the SEA-AD study.
                """)

    # ================= Pathology distribution across disease severity =================
    st.header("Pathology distribution across disease severity")
    st.success("""
    These neuropathological features were analyzed across donors spanning the full spectrum
    of Alzheimer’s disease severity.

    As disease severity increases, protein aggregates accumulate and neuronal integrity declines,
    with accompanying changes suggestive of increased tissue reactivity, reflecting progressive
    tissue-level neurodegeneration.
    """)

    st.markdown("""Together, these analyses illustrate how quantitative neuropathology in the MTG
    captures a continuous spectrum of Alzheimer’s disease progression across donors,
    providing a foundation for cell-type–resolved analyses in the SEA-AD atlas.
    """)