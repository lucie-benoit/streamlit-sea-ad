"""
Visualization utilities for the SEA-AD Streamlit app.

This module contains small, reusable plotting functions used across sections:
- Cohort overview: age, sex, APOE, ADNC, dementia
- MTG pathology: AT8 / Aβ distributions and relationships
- Descriptive correlation heatmap across pathology markers

Conventions
-----------
- Functions take a pandas.DataFrame as input and render directly to Streamlit.
- Each function performs lightweight validation checks to avoid hard crashes
  in Streamlit Cloud (missing columns, empty dataframes, etc.).
- We prefer `st.altair_chart(..., use_container_width=True)` for responsive sizing
  (Streamlit does NOT accept `width="stretch"` for Altair charts).
"""
import altair as alt
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def gender_donutchart(df):
    """
    Display a donut chart showing the sex distribution of SEA-AD donors.

    This visualization provides a high-level overview of the cohort composition
    and highlights the sex imbalance commonly observed in Alzheimer’s disease studies.

    Parameters
    ----------
    df : pandas.DataFrame
        Donor-level metadata containing at least the 'Sex' column.
    """
    # --- Safety checks ---
    if df is None:
        st.error("df is None in gender_donutchart")
        return

    if "Sex" not in df.columns:
        st.error("Column 'Sex' not found in dataframe")
        st.write("Available columns:", df.columns.tolist())
        return

    # --- Aggregate donor counts by sex ---
    gender_counts = df["Sex"].value_counts().reset_index()
    gender_counts.columns = ["Sex", "count"]

    # --- Plotly donut chart ---
    fig = px.pie(
        gender_counts,
        names="Sex",
        values="count",
        hole=0.4,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", y=-0.1),
        margin=dict(l=10, r=10, t=10, b=10),
    )

    st.plotly_chart(fig, width='stretch')


def age_barchart(df):
    """
    Show the distribution of age at death (binned histogram).

    Parameters
    ----------
    df : pandas.DataFrame
        Donor-level metadata containing 'Age at Death'.

    Returns
    -------
    None
        Renders an Altair binned bar chart in Streamlit.
    """

    # --- Safety checks ---
    if "Age at Death" not in df.columns:
        st.error("Column 'Age at Death' not found")
        return
    
    # Convert to numeric; invalid strings become NaN and are removed
    age_df = df.copy()
    age_df["Age at Death"] = pd.to_numeric(age_df["Age at Death"], errors="coerce")
    age_df = age_df.dropna(subset=["Age at Death"])

    chart = (
        alt.Chart(age_df)
        .mark_bar()
        .encode(
            x=alt.X(
                "Age at Death:Q",
                bin=alt.Bin(step=5),
                title="Age at death (years)"
            ),
            y=alt.Y("count()", title="Number of donors"),
            tooltip=["Age at Death:Q","count()"]
        )
        .properties(height=300)
    )

    st.altair_chart(chart, use_container_width=True)

def apoe_genotype(df):
    """
    Display the distribution of APOE genotypes in the cohort.

    Parameters
    ----------
    df : pandas.DataFrame
        Donor-level metadata containing 'APOE Genotype'.

    Returns
    -------
    None
        Renders a horizontal bar chart in Streamlit.
    """

    # Horizontal bars: easier to read genotype labels than a vertical axis
    chart = alt.Chart(df).mark_bar().encode(
        y=alt.Y(
            "APOE Genotype:N",
            title="APOE genotype",
            sort="-x"
        ),
        x=alt.X(
            "count()",
            title="Number of donors"
        ),
        tooltip=[
            "APOE Genotype:N",
            alt.Tooltip("count()", title="Number of donors")
        ],
        color=alt.Color(
            "APOE Genotype:N",
            legend=None,
            scale=alt.Scale(scheme="tableau10")
        )
    ).properties(
        height=300
    )

    st.altair_chart(chart, use_container_width=True)



def cognitive_status(df):
    """
    Display simple cohort-level cognitive status as two metrics (% Dementia / % No dementia).

    Why metrics instead of a bar chart?
    ----------------------------------
    For a quick dashboard overview, two big numbers are more readable than another plot.

    Parameters
    ----------
    df : pandas.DataFrame
        Donor-level metadata containing 'Cognitive Status'.

    Returns
    -------
    None
        Renders Streamlit metrics.
    """
     
    total = len(df)
    counts = df["Cognitive Status"].value_counts()

    # Keep the logic explicit for students: compute percentages manually
    dementia_pct = counts.get("Dementia", 0) / total * 100
    no_dementia_pct = counts.get("No dementia", 0) / total * 100

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Dementia",
            value=f"{dementia_pct:.1f} %",
        )

    with col2:
        st.metric(
            label="No dementia",
            value=f"{no_dementia_pct:.1f} %",
        )


def adnc_distribution(df):
    """
    Plot the distribution of AD neuropathological change (ADNC) categories.

    Parameters
    ----------
    df : pandas.DataFrame
        Donor-level metadata containing 'Overall AD neuropathological Change'.

    Returns
    -------
    None
        Renders an Altair bar chart.
    """

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(
            "Overall AD neuropathological Change:N",
            title="AD neuropathological change",
            sort=["Not AD", "Low", "Intermediate", "High"]
        ),
        y=alt.Y("count()", title="Number of donors"),
        color=alt.Color(
            "Overall AD neuropathological Change:N",
            scale=alt.Scale(scheme="greens"),
            legend=None
        ),
        tooltip=[
            "Overall AD neuropathological Change:N",
            alt.Tooltip("count()", title="Number of donors")
        ]
    ).properties(height=300)

    st.altair_chart(chart, use_container_width=True)

def apoe4_by_adnc(df):
    """
    Plot the proportion of APOE4 carriers across ADNC stages.

    Notes
    -----
    This converts APOE genotype strings into a boolean indicator 'APOE4+' and then
    displays the mean (i.e., the proportion of True) per ADNC category.

    Parameters
    ----------
    df : pandas.DataFrame
        Donor-level metadata containing 'APOE Genotype' and ADNC column.

    Returns
    -------
    None
        Renders an Altair bar chart.
    """
    df = df.copy()
    df["APOE4+"] = df["APOE Genotype"].str.contains("4")

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(
            "Overall AD neuropathological Change:N",
            sort=["Not AD", "Low", "Intermediate", "High"],
            title="AD neuropathological change"
        ),
        y=alt.Y(
            "mean(APOE4+):Q",
            axis=alt.Axis(format="%"),
            title="Proportion APOE4+"
        ),
        tooltip=[
            "Overall AD neuropathological Change:N",
            alt.Tooltip("mean(APOE4+):Q", format=".2%")
        ],
        color=alt.Color(
            "Overall AD neuropathological Change:N",
            legend=None,
            scale=alt.Scale(scheme="reds")
        )
    ).properties(height=300)

    st.altair_chart(chart, use_container_width=True)

def dementia_by_adnc(df):
    """
    Plot the proportion of donors with dementia across ADNC stages.

    Notes
    -----
    This derives a simple boolean flag `Dementia+` from the 'Cognitive Status' string.

    Parameters
    ----------
    df : pandas.DataFrame
        Donor-level metadata containing 'Cognitive Status' and ADNC column.

    Returns
    -------
    None
        Renders an Altair bar chart.
    """
    df = df.copy()

    # Binary indicator for dementia
    # Important: This is a simple string rule. If your dataset has more nuanced labels,
    # you may want a controlled mapping instead.
    df["Dementia+"] = df["Cognitive Status"].fillna("").str.contains("Dementia")

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(
            "Overall AD neuropathological Change:N",
            sort=["Not AD", "Low", "Intermediate", "High"],
            title="AD neuropathological change"
        ),
        y=alt.Y(
            "mean(Dementia+):Q",
            axis=alt.Axis(format="%"),
            title="Proportion of donors with dementia"
        ),
        tooltip=[
            "Overall AD neuropathological Change:N",
            alt.Tooltip("mean(Dementia+):Q", format=".2%")
        ],
        color=alt.Color(
            "Overall AD neuropathological Change:N",
            legend=None,
            scale=alt.Scale(scheme="blues")
        )
    ).properties(height=300)

    st.altair_chart(chart, use_container_width=True)

# =============================================================================
# MTG pathology plots
# =============================================================================

def at8_by_dementia_barplot(df):
    """
    Bar chart of mean AT8-positive area by dementia status.

    Parameters
    ----------
    df : pandas.DataFrame
        Pathology dataframe containing:
        - 'percent AT8 positive area_Grey matter'
        - 'Dementia_status' (categorical: 'No dementia' / 'Dementia')

    Returns
    -------
    None
        Renders an Altair bar chart.
    """
    required_cols = [
        "percent AT8 positive area_Grey matter",
        "Dementia_status"
    ]

    if not all(col in df.columns for col in required_cols):
        st.error("Required columns not found.")
        st.write("Available columns:", df.columns.tolist())
        return

    chart = (
        alt.Chart(df)
        .mark_bar(size=60)
        .encode(
            x=alt.X(
                "Dementia_status:N",
                sort=["No dementia", "Dementia"],
                title="Dementia status"
            ),
            y=alt.Y(
                "mean(percent AT8 positive area_Grey matter):Q",
                title="Mean AT8-positive area (% grey matter)"
            ),
            tooltip=[
                "Dementia_status:N",
                alt.Tooltip(
                    "mean(percent AT8 positive area_Grey matter):Q",
                    title="Mean AT8 (%)",
                    format=".2f"
                )
            ],
            color=alt.Color(
                "Dementia_status:N",
                scale=alt.Scale(domain=["No dementia", "Dementia"],
                                range=["#4C72B0", "#DD8452"]),
                legend=None
            )
        )
        .properties(height=350)
    )

    st.altair_chart(chart, use_container_width=True)

# Consistent height across pathology plots for a clean layout
HEIGHT = 350
 
def at8_scatter_by_dementia(df):

    """
    Scatter plot of AT8-positive area across dementia status (with horizontal jitter).

    Why jitter?
    -----------
    Many points share the same x-category ("Dementia"/"No dementia"), so jitter helps
    visualize donor density and overlap.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain:
        - 'Dementia' (boolean)
        - 'percent AT8 positive area_Grey matter'
        - 'Donor ID'

    Returns
    -------
    None
        Renders an Altair scatter chart.
    """

    value_col = "percent AT8 positive area_Grey matter"

    # --- Safety checks ---
    required = {"Dementia", value_col}
    if not required.issubset(df.columns):
        st.error("Missing required columns")
        st.write(df.columns.tolist())
        return

    plot_df = df.copy()
    # Make labels explicit for non-technical audiences
    plot_df["Dementia_status"] = plot_df["Dementia"].map(
        {True: "Dementia", False: "No dementia"}
    )

    # Jitter is computed in Vega (Altair) to avoid modifying your dataframe
    jitter = alt.Chart(plot_df).transform_calculate(
        jitter="(random() - 0.5) * 0.3"
    )

    chart = jitter.mark_circle(size=80, opacity=0.7).encode(
        x=alt.X(
            "Dementia_status:N",
            title="Dementia status",
            sort=["No dementia", "Dementia"]
        ),
        xOffset="jitter:Q",
        y=alt.Y(
            f"{value_col}:Q",
            title="AT8-positive area (% grey matter)"
        ),
        color=alt.Color(
            "Dementia_status:N",
            scale=alt.Scale(
                domain=["No dementia", "Dementia"],
                range=["#4C72B0", "#DD8452"]
            ),
            legend=alt.Legend(title="Status")
        ),
        tooltip=[
            "Donor ID:N",
            "Dementia_status:N",
            alt.Tooltip(f"{value_col}:Q", format=".2f")
        ]
    ).properties(
        height=HEIGHT
    )

    st.altair_chart(chart, use_container_width=True)


def at8_vs_adnc(df):
    """
    Plot AT8-positive area across ADNC stages with:
    - donor-level points (scatter)
    - median marker per ADNC category (tick)

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain:
        - 'Overall AD neuropathological Change'
        - 'percent AT8 positive area_Grey matter'
        - 'Donor ID'

    Returns
    -------
    None
        Renders a layered Altair chart.
    """
    adnc_order = ["Not AD", "Low", "Intermediate", "High"]

    base = alt.Chart(df).encode(
        x=alt.X(
            "Overall AD neuropathological Change:N",
            sort=adnc_order,
            title="AD neuropathological change (ADNC)"
        ),
        y=alt.Y(
            "percent AT8 positive area_Grey matter:Q",
            title="pTau burden (% AT8+ area)"
        )
    )

    # Each point is a donor
    points = base.mark_circle(
        size=60,
        opacity=0.6
    ).encode(
        tooltip=[
            "Donor ID:N",
            "Overall AD neuropathological Change:N",
            alt.Tooltip(
                "percent AT8 positive area_Grey matter:Q",
                format=".2f",
                title="AT8 (%)"
            )
        ]
    )

    # Median per category gives a robust central tendency
    median = base.mark_tick(
        color="black",
        thickness=3
    ).encode(
        y="median(percent AT8 positive area_Grey matter):Q"
    )

    chart = (points + median).properties(height=HEIGHT)

    st.altair_chart(chart, use_container_width=True)

def abeta_vs_adnc(df, abeta_col="percent 6e10 positive area_Grey matter"):
    """
    Plot Aβ plaque burden (6E10) across ADNC stages.

    This uses:
    - jittered donor-level points (to show density within categories)
    - a mean rule per category (simple summary statistic)

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain 'Donor ID', 'Overall AD neuropathological Change', and `abeta_col`.
    abeta_col : str
        Column name representing Aβ burden (default: 6E10 % positive area in grey matter).

    Returns
    -------
    None
        Renders a layered Altair chart.
    """
    required = {"Donor ID", "Overall AD neuropathological Change", abeta_col}
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing columns for plot: {missing}")
        st.write("Available columns:", df.columns.tolist())
        return

    plot_df = df[["Donor ID", "Overall AD neuropathological Change", abeta_col]].copy()
    plot_df[abeta_col] = pd.to_numeric(plot_df[abeta_col], errors="coerce")
    plot_df = plot_df.dropna(subset=[abeta_col, "Overall AD neuropathological Change"])

    adnc_order = ["Not AD", "Low", "Intermediate", "High"]

    base = alt.Chart(plot_df).encode(
        x=alt.X(
            "Overall AD neuropathological Change:N",
            sort=adnc_order,
            title="AD neuropathological change (ADNC)",
            axis=alt.Axis(labelAngle=0),
        )
    )

    # Jitter points to reduce overlap within categories
    points = base.mark_circle(size=70, opacity=0.7).encode(
        y=alt.Y(f"{abeta_col}:Q", title="Aβ plaque burden (6E10) — % positive area (Grey matter)"),
        color=alt.Color("Overall AD neuropathological Change:N", legend=None),
        tooltip=[
            alt.Tooltip("Donor ID:N"),
            alt.Tooltip("Overall AD neuropathological Change:N", title="ADNC"),
            alt.Tooltip(f"{abeta_col}:Q", title="6E10 % area", format=".2f"),
        ],
    ).transform_calculate(
        jitter="(random() - 0.5) * 0.35"
    ).encode(
        xOffset=alt.XOffset("jitter:Q")
    )

    # Mean per category (rule)
    mean_rule = base.mark_rule(size=3).encode(
        y=alt.Y(f"mean({abeta_col}):Q"),
        color=alt.value("black"),
        tooltip=[alt.Tooltip(f"mean({abeta_col}):Q", title="Mean", format=".2f")],
    )

    chart = (points + mean_rule).properties(height=350)
    st.altair_chart(chart, use_container_width=True)



def correlation_heatmap_pathology(df):
    """
    Display a Spearman correlation heatmap across pathology markers.

    Notes
    -----
    - Spearman correlation is used to be robust to non-normal distributions.
    - `min_periods=10` ensures correlations are not computed on too few donors.
    - We keep only columns present in the dataframe to avoid crashes if some markers
      are missing in the subset.

    Parameters
    ----------
    df : pandas.DataFrame
        MTG pathology dataframe containing marker columns.

    Returns
    -------
    None
        Renders a seaborn heatmap via matplotlib in Streamlit.
    """
    cols = [
        "percent AT8 positive area_Grey matter",
        "percent 6e10 positive area_Grey matter",
        "number of NeuN positive cells per area_Grey matter",
        "percent Iba1 positive area_Grey matter",
        "percent GFAP positive area_Grey matter",
        "percent pTDP43 positive area_Grey matter",
        "percent aSyn positive area_Grey matter",
        # Optional:
        # "ripa abeta42_Grey matter",
    ]

    # Keep only existing columns (makes the function robust to missing markers)
    cols = [c for c in cols if c in df.columns]
    if len(cols) < 3:
        st.error("Not enough marker columns found to compute correlations.")
        st.write("Available columns:", df.columns.tolist())
        return

    # Convert to numeric; non-numeric entries become NaN
    X = df[cols].apply(pd.to_numeric, errors="coerce")

    # Spearman correlations (rank-based)
    corr = X.corr(method="spearman", min_periods=10)

    # Replace raw column names with more readable labels for the figure
    rename = {
        "percent AT8 positive area_Grey matter": "pTau (AT8) %",
        "percent 6e10 positive area_Grey matter": "Aβ (6E10) %",
        "number of NeuN positive cells per area_Grey matter": "NeuN cells/area",
        "percent Iba1 positive area_Grey matter": "Iba1 %",
        "percent GFAP positive area_Grey matter": "GFAP %",
        "percent pTDP43 positive area_Grey matter": "pTDP-43 %",
        "percent aSyn positive area_Grey matter": "αSyn %",
        "ripa abeta42_Grey matter": "Aβ42 (ripa)",
    }
    corr = corr.rename(index=rename, columns=rename)

    # Small figure size keeps the dashboard compact
    fig, ax = plt.subplots(figsize=(3.4, 2.8))

    hm = sns.heatmap(
        corr,
        ax=ax,
        cmap="RdBu_r",
        vmin=-1, vmax=1,
        annot=True,             # show correlation values   
        square=True,            # square cells for readability
        linewidths=0.25,            
        linecolor="white",
        annot_kws={"size": 5.5},
        cbar_kws={"shrink": 0.65, "aspect": 30, "pad": 0.02},
    )

    # Improve tick readability on small plots
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=6)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=6)

    # Make colorbar label explicit
    cbar = hm.collections[0].colorbar
    cbar.set_label("Spearman ρ", fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    plt.tight_layout(pad=0.4)
    st.pyplot(fig)

    # Optional: show how many donors per pair (non-NaN)
    st.caption(f"Computed on n={len(df)} donors (pairwise complete observations, min_periods=10).")

def neun_vs_adnc(df):
    """
    Boxplot of NeuN+ cells per area across ADNC stages.

    Why boxplot?
    ------------
    NeuN measures vary across donors; boxplots show median, IQR, and outliers,
    making group differences easy to spot.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain:
        - 'Overall AD neuropathological Change'
        - 'number of NeuN positive cells per area_Grey matter'

    Returns
    -------
    None
        Renders an Altair boxplot.
    """
    chart = alt.Chart(df).mark_boxplot(size=40).encode(
        x=alt.X(
            "Overall AD neuropathological Change:N",
            sort=["Not AD", "Low", "Intermediate", "High"],
            title="AD neuropathological change (ADNC)"
        ),
        y=alt.Y(
            "number of NeuN positive cells per area_Grey matter:Q",
            title="NeuN+ cells per area (Grey matter)"
        ),
        color=alt.Color(
            "Overall AD neuropathological Change:N",
            legend=None,
            scale=alt.Scale(scheme="blues")
        )
    ).properties(height=350)

    st.altair_chart(chart, use_container_width=True)

def neun_vs_at8(df):
    """
    Scatter plot of NeuN+ cells per area vs pTau burden (AT8), colored by ADNC stage,
    with a LOESS trend line.

    Why LOESS?
    ----------
    LOESS provides a smooth, non-parametric trend line that is useful for exploratory
    analysis when the relationship may not be strictly linear.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain:
        - 'percent AT8 positive area_Grey matter'
        - 'number of NeuN positive cells per area_Grey matter'
        - 'Overall AD neuropathological Change'
        - 'Donor ID'

    Returns
    -------
    None
        Renders a layered Altair chart.
    """
    chart = alt.Chart(df).mark_circle(size=70, opacity=0.7).encode(
        x=alt.X(
            "percent AT8 positive area_Grey matter:Q",
            title="pTau burden (AT8, % area)"
        ),
        y=alt.Y(
            "number of NeuN positive cells per area_Grey matter:Q",
            title="NeuN+ cells per area (Grey matter)"
        ),
        color=alt.Color(
            "Overall AD neuropathological Change:N",
            sort=["Not AD", "Low", "Intermediate", "High"],
            scale=alt.Scale(scheme="viridis"),
            title="ADNC"
        ),
        tooltip=[
            "Donor ID:N",
            "Overall AD neuropathological Change:N"
        ]
    )

    # LOESS trend across all donors (not per-group) for an overall pattern
    loess = chart.transform_loess(
        "percent AT8 positive area_Grey matter",
        "number of NeuN positive cells per area_Grey matter"
    ).mark_line(color="black")

    st.altair_chart((chart + loess).properties(height=350), use_container_width=True)

