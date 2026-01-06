import streamlit as st
from utils.io import load_data
from utils.visualizations import age_barchart, gender_donutchart, apoe_genotype, cognitive_status, adnc_distribution, apoe4_by_adnc, dementia_by_adnc

def app(df):
    st.title("SEA-AD donor cohort overview")

    st.info("""
        This mini-project focuses on a subset of key variables in the SEA-AD dataset that are directly relevant to exploring the relationship between Alzheimer’s disease pathology and clinical cognitive status. 
        Given the short timeframe, we prioritize variables that are widely used, consistently available, and easy to interpret, while leaving out variables that are sparse, redundant, or beyond the scope of this exploratory analysis.

    """)
    st.header("Who are the donors ?")

    # Explore basic informations about the donor, gender and age 
    st.markdown("""The SEA-AD donor cohort is predominantly female (60.7%). 
            Donors span a wide age range from 65 to 102 years at death, reflecting advanced aging and enabling the study of late-life neurodegenerative processes across a broad elderly population.""")


    # create a container 
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gender distribution")
        gender_donutchart(df)

    with col2:
        st.subheader("Age at death distribution")
        age_barchart(df)
    
    st.markdown("""With the age and sex distribution of the SEA-AD donors established, 
                the next step is to examine how genetic variation, particularly APOE alleles, 
                contributes to individual risk for Alzheimer’s disease.""")

    # ================= APOE Genotype part ====================================
    st.header("Genetic risk factors")
    # Explore precise informations related to Alzheimer disease such as APOE
    st.info(""" 
        **APOE genotype** refers the identification of the types of APOE gene in the DNA. 
            
        There are three common allelic forms: ε2, ε3, and ε4. Each individual inherits two copies of APOE, resulting in genotypes such as 3/3, 3/4, or 4/4. 
        
        Having two copies of **APOE ε4** is associated with a higher risk of Alzheimer’s than having one copy. While inheriting APOE ε4 increases a person’s risk of Alzheimer’s, some people with an APOE ε4 allele never develop the disease.

        """)
    
    st.markdown("""
        - **APOE ε2** is considered a protective allele against Alzheimer’s disease. When Alzheimer’s does occur in individuals carrying ε2, symptom onset typically happens later in life compared to ε4 carriers. This allele is relatively rare, present in approximately 5–10% of the population.
        - **APOE ε3** is the most prevalent allele in the general population and is generally regarded as having a neutral effect on Alzheimer’s disease .
        - **APOE ε4** is associated with an increased risk of developing Alzheimer’s disease and, in some populations, with an earlier age at disease onset. Approximately 15–25% of individuals carry at least one ε4 allele, while 2–5% carry two copies.
        
        
    """)


    apoe_genotype(df)

    st.markdown("""
    While APOE genotype is a well-established genetic risk factor for Alzheimer’s disease,
    it does not directly describe an individual’s clinical presentation.

    To better understand how genetic risk translates into real-world outcomes,
    we next examine the **cognitive status** of donors, which captures the clinical
    expression of cognitive impairment and dementia.
    """)
    # ================= Cognitive status part ====================================
    st.header("Clinical dementia status")
    # Explore precise informations related to Alzheimer disease such as cognitive status
    st.info("""
        **Cognitive status** reflects the clinical manifestation of cognitive decline in donors.
        It summarizes whether individuals were cognitively normal, mildly impaired, or affected
        by dementia at the time of assessment.

        Unlike genetic risk factors, cognitive status captures the *observable clinical outcome*
        of neurodegeneration and provides a direct link between biological processes and
        functional impairment.
    """)
    cognitive_status(df)

    st.markdown("""
        Cognitive status closely mirrors neuropathological severity in the SEA-AD cohort.
        
        **Dementia is rare or absent in donors with no or low AD pathology, but becomes
        increasingly prevalent in intermediate and high ADNC groups.** These observations highlight cognitive impairment as a clinical manifestation
        of underlying Alzheimer’s disease pathology.
    """) 

    # ================= Dementia vs ADNC ====================================
    dementia_by_adnc(df)

    st.caption("""
    The prevalence of dementia increases sharply with Alzheimer’s disease
    neuropathological severity. Nearly three-quarters of donors with high
    ADNC had dementia before death, compared to approximately one-third
    of donors with intermediate or low AD pathology, and none among donors
    with no AD pathology.
    """)
    
    st.markdown("""While cognitive status captures the observable effects of neurodegeneration, 
                examining the brain itself reveals the pathological changes—amyloid plaques and tau tangles—that 
                underlie these clinical outcomes.""")
    # ================= Alzheimer's Disease Neuropathologic Change part ====================================
    st.header("Neuropathological burden")
    # Explore precise informations related to Alzheimer disease such as ADNC
    st.info("""
            Alzheimer's Disease Neuropathologic Change, refers to the specific brain lesions—amyloid plaques and tau tangles—that are hallmarks of Alzheimer's
            
            The distribution of Alzheimer’s Disease Neuropathologic Change (ADNC) shows that most donors fall into the intermediate and high pathology categories, with fewer donors classified as low or no AD pathology.
            
            """)
    adnc_distribution(df)

    st.markdown("""
    While Alzheimer’s Disease Neuropathologic Change (ADNC) captures the severity of
    brain pathology at the tissue level, disease progression is influenced by both
    neuropathological processes and underlying genetic risk factors.

    To explore how genetic susceptibility relates to neuropathological burden,
    we next examine the distribution of the APOE ε4 allele across ADNC stages.
    """) 
    
    # ================= APOE vs ANDC ====================================
    # Explore precise informations related to Alzheimer disease such as APOE vs ADNC
    st.info("""Donors with an APOE4 allele included nearly half (20 of 42) of high ADNC cases, a quarter (five of 21) of intermediate cases and no low ADNC or no AD cases.""")
    apoe4_by_adnc(df)

    st.markdown("""
    These results show a clear association between APOE ε4 carrier status and
    Alzheimer’s disease neuropathological severity.

    The proportion of APOE ε4 carriers increases progressively across ADNC stages,
    with ε4 being almost exclusively observed in donors with intermediate to high
    neuropathological burden. This pattern is consistent with the established role
    of APOE ε4 as a major genetic risk factor for Alzheimer’s disease.
    """)

    st.success(
        """
        **Take-home message**

        The SEA-AD cohort spans the full spectrum of Alzheimer’s disease neuropathology.
        Genetic risk (APOE4), neuropathological burden (ADNC), and clinical status
        (dementia) are coherently structured across donors, providing a strong foundation
        for investigating how brain pathology relates to cognitive decline.
        """
    )