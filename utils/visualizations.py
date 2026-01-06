import altair as alt
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def gender_donutchart(df):
    """Generate a Plotly donut chart showing gender distribution of SEA-AD donors"""

    if df is None:
        st.error("df is None in gender_donutchart")
        return

    if "Sex" not in df.columns:
        st.error("Column 'Sex' not found in dataframe")
        st.write("Available columns:", df.columns.tolist())
        return

    gender_counts = df["Sex"].value_counts().reset_index()
    gender_counts.columns = ["Sex", "count"]

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
    """Distribution of age at death in the donor cohort"""

    if "Age at Death" not in df.columns:
        st.error("Column 'Age at Death' not found")
        return

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
    """Distribution of APOE genotypes in the SEA-AD cohort"""

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
    total = len(df)

    counts = df["Cognitive Status"].value_counts()

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
    df = df.copy()

    # Binary indicator for dementia
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

def at8_by_dementia_barplot(df):

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

HEIGHT = 350
 
def at8_scatter_by_dementia(df):

    value_col = "percent AT8 positive area_Grey matter"

    # Sécurité
    required = {"Dementia", value_col}
    if not required.issubset(df.columns):
        st.error("Missing required columns")
        st.write(df.columns.tolist())
        return

    # Créer une colonne lisible
    plot_df = df.copy()
    plot_df["Dementia_status"] = plot_df["Dementia"].map(
        {True: "Dementia", False: "No dementia"}
    )

    # Jitter horizontal
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

    # --- Scatter (each donor) ---
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

    # --- Median line per ADNC group ---
    median = base.mark_tick(
        color="black",
        thickness=3
    ).encode(
        y="median(percent AT8 positive area_Grey matter):Q"
    )

    chart = (points + median).properties(height=HEIGHT)

    st.altair_chart(chart, use_container_width=True)

def abeta_vs_adnc(df, abeta_col="percent 6e10 positive area_Grey matter"):
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

    mean_rule = base.mark_rule(size=3).encode(
        y=alt.Y(f"mean({abeta_col}):Q"),
        color=alt.value("black"),
        tooltip=[alt.Tooltip(f"mean({abeta_col}):Q", title="Mean", format=".2f")],
    )

    chart = (points + mean_rule).properties(height=350)
    st.altair_chart(chart, use_container_width=True)



def correlation_heatmap_pathology(df):
    """
    Heatmap of Spearman correlations between pathology markers (descriptive).
    Assumes columns exist in df.
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

    # Keep only columns that exist (avoids crashes)
    cols = [c for c in cols if c in df.columns]
    if len(cols) < 3:
        st.error("Not enough marker columns found to compute correlations.")
        st.write("Available columns:", df.columns.tolist())
        return

    X = df[cols].apply(pd.to_numeric, errors="coerce")

    # Spearman correlation
    corr = X.corr(method="spearman", min_periods=10)

    # Pretty labels
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

    fig, ax = plt.subplots(figsize=(3.4, 2.8))

    hm = sns.heatmap(
        corr,
        ax=ax,
        cmap="RdBu_r",
        vmin=-1, vmax=1,
        annot=True,                
        square=True,
        linewidths=0.25,            
        linecolor="white",
        annot_kws={"size": 5.5},
        cbar_kws={"shrink": 0.65, "aspect": 30, "pad": 0.02},
    )

    # ticks plus lisibles
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=6)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=6)

    # colorbar discrète
    cbar = hm.collections[0].colorbar
    cbar.set_label("Spearman ρ", fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    plt.tight_layout(pad=0.4)
    st.pyplot(fig)

    # Optional: show how many donors per pair (non-NaN)
    st.caption(f"Computed on n={len(df)} donors (pairwise complete observations, min_periods=10).")

def neun_vs_adnc(df):
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

    loess = chart.transform_loess(
        "percent AT8 positive area_Grey matter",
        "number of NeuN positive cells per area_Grey matter"
    ).mark_line(color="black")

    st.altair_chart((chart + loess).properties(height=350), width='stretch')
