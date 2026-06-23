"""
ESI_Hab — Exoplanet Habitability Pipeline Demo
A visual walkthrough of the Phase 1 habitability analysis methodology

No installation required • No datasets needed • Pure demonstration
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Exolpanet Habitability Pipeline Demo",
    page_icon="🪐",
    layout="wide",
)

# ═════════════════════════════════════════════════════════════════════════════
# DATA: Exact values from notebook
# ═════════════════════════════════════════════════════════════════════════════

# Pipeline funnel counts (actual from notebook)
PIPELINE_COUNTS = {
    "Archive Total": 6153,
    "After Missing Data": 6146,
    "After Radius ≤ 1.6 R⊕": 1227,
    "After Radius-Mass Relation": 1227,  # Same (fills missing values)
    "After T_eq Calculation": 1120,
    "After Density Filter": 1067,
    "After HZ Check": 16,
    "After ESI & HZD Filtering": 8,
}

# Drop counts
DROP_COUNTS = {
    "No Radius/Mass": 7,
    "Radius > 1.6 R⊕": 4919,
    "No T_eq": 107,
    "Density > 20": 53,
    "Outside HZ": 1051,
    "ESI < 0.75 or HZD < 0.71": 8,
}

# Top 8 candidates from notebook (exact values)
TOP_CANDIDATES = [
    {"rank": 1, "name": "GJ 1061 d", "esi": 0.873787, "hzd": 0.999570, "sephi": 0.927434, "composite": 0.932182},
    {"rank": 2, "name": "GJ 667 C f", "esi": 0.835860, "hzd": 0.968433, "sephi": 0.967638, "composite": 0.921805},
    {"rank": 3, "name": "Kepler-442 b", "esi": 0.912707, "hzd": 0.826603, "sephi": 0.962354, "composite": 0.898782},
    {"rank": 4, "name": "Wolf 1069 b", "esi": 0.974170, "hzd": 0.895218, "sephi": 0.815817, "composite": 0.892727},
    {"rank": 5, "name": "TRAPPIST-1 e", "esi": 0.951359, "hzd": 0.903434, "sephi": 0.755585, "composite": 0.865980},
    {"rank": 6, "name": "Proxima Cen b", "esi": 0.889379, "hzd": 0.909200, "sephi": 0.801853, "composite": 0.865527},
    {"rank": 7, "name": "GJ 1002 b", "esi": 0.926202, "hzd": 0.864048, "sephi": 0.796679, "composite": 0.860681},
    {"rank": 8, "name": "TOI-715 b", "esi": 0.854830, "hzd": 0.807265, "sephi": 0.905702, "composite": 0.854989},
]

# Reference values for Earth
EARTH_REFERENCE = {
    "Radius": "1.0 R⊕",
    "Density": "5.51 g/cm³",
    "Escape Velocity": "11,186 m/s",
    "Equilibrium Temp": "255 K",
}

# ═════════════════════════════════════════════════════════════════════════════
# HEADER
# ═════════════════════════════════════════════════════════════════════════════

st.title("🪐 Exoplanet Habitability Pipeline")
st.caption("Phase 1 Methodology Demonstration • Interactive Visual Walkthrough")

st.markdown("""
This demo showcases the multi-stage filtering pipeline used to identify potentially habitable exoplanets 
from NASA's Exoplanet Archive. No installation or datasets required — this is a pure visual demonstration 
of the methodology.
""")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# TABS
# ═════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Phase I", 
    "🧮 Formulas & Metrics",
    "🏆 Results", 
    "📖 Methodology"
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: PIPELINE OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────

with tab1:
    st.header("Pipeline Funnel")
    
    # Funnel visualization
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    
    with col1:
        st.metric("🌌 Archive", f"{PIPELINE_COUNTS['Archive Total']:,}")
        st.caption("Total")
    
    with col2:
        dropped = DROP_COUNTS["No Radius/Mass"]
        st.metric("📊 Clean", f"{PIPELINE_COUNTS['After Missing Data']:,}", 
                 delta=f"−{dropped}", delta_color="off")
        st.caption("Has R or M")
    
    with col3:
        dropped = DROP_COUNTS["Radius > 1.6 R⊕"]
        st.metric("🪨 Rocky", f"{PIPELINE_COUNTS['After Radius ≤ 1.6 R⊕']:,}", 
                 delta=f"−{dropped:,}", delta_color="off")
        st.caption("R ≤ 1.6 R⊕")
    
    with col4:
        dropped = DROP_COUNTS["No T_eq"]
        st.metric("🌡️ T_eq", f"{PIPELINE_COUNTS['After T_eq Calculation']:,}", 
                 delta=f"−{dropped}", delta_color="off")
        st.caption("Temp known")
    
    with col5:
        dropped = DROP_COUNTS["Density > 20"]
        st.metric("⚖️ Dense", f"{PIPELINE_COUNTS['After Density Filter']:,}", 
                 delta=f"−{dropped}", delta_color="off")
        st.caption("ρ ≤ 20")
    
    with col6:
        dropped = DROP_COUNTS["Outside HZ"]
        st.metric("☀️ In HZ", f"{PIPELINE_COUNTS['After HZ Check']:,}", 
                 delta=f"−{dropped:,}", delta_color="off")
        st.caption("HZD ∈ [-1,1]")
    
    with col7:
        dropped = DROP_COUNTS["ESI < 0.75 or HZD < 0.71"]
        st.metric("✨ Final", f"{PIPELINE_COUNTS['After ESI & HZD Filtering']:,}", 
                 delta=f"−{dropped}", delta_color="off")
        st.caption("ESI & HZD")
    
    with col8:
        st.metric("🏆 Ranked", f"{PIPELINE_COUNTS['After ESI & HZD Filtering']:,}")
        st.caption("w/ SEPHI")
    
    st.markdown("")
    
    # Sankey diagram
    st.subheader("Filter Cascade")
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=[
                "NASA Archive<br>6,153",
                "Has Data<br>6,146",
                "Rocky<br>(R ≤ 1.6)<br>1,227",
                "T_eq Known<br>1,120",
                "Realistic ρ<br>1,067",
                "In HZ<br>16",
                "Final 8<br>(ESI & HZD)",
                "Ranked<br>8",
                "❌ No R/M<br>7",
                "❌ Too big<br>4,919",
                "❌ No T_eq<br>107",
                "❌ ρ > 20<br>53",
                "❌ Outside HZ<br>1,051",
                "❌ Low scores<br>8",
            ],
            color=[
                "#4A90D9", "#5FA3E8", "#7AB8F5", "#95CDFF", "#B0E0FF", "#D4F1F4", "#1ABC9C", "#27AE60",
                "#E74C3C", "#E74C3C", "#E74C3C", "#E74C3C", "#E74C3C", "#E74C3C"
            ],
            customdata=[
                "All exoplanets in NASA Archive",
                "Have either radius or mass data",
                "Terrestrial planets (R ≤ 1.6 R⊕)",
                "Equilibrium temperature calculated",
                "Realistic density (ρ ≤ 20 g/cm³)",
                "Within habitable zone boundaries",
                "Passed ESI ≥ 0.75 and HZD ≥ 0.71",
                "Ranked by composite score with SEPHI",
                "Missing both radius AND mass",
                "Radius > 1.6 R⊕ (gas giants)",
                "Cannot calculate equilibrium temp",
                "Unrealistic density > 20 g/cm³",
                "HZD outside [-1, 1] range",
                "ESI < 0.75 or HZD_norm < 0.71",
            ],
            hovertemplate='<b>%{label}</b><br>%{customdata}<extra></extra>'
        ),
        link=dict(
            source=[0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5],
            target=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            value=[6146, 1227, 1120, 1067, 16, 8, 8, 7, 4919, 107, 53, 1051, 8],
            color=["rgba(74, 144, 217, 0.3)", "rgba(95, 163, 232, 0.3)", 
                   "rgba(122, 184, 245, 0.3)", "rgba(149, 205, 255, 0.3)", 
                   "rgba(176, 224, 255, 0.3)", "rgba(212, 241, 244, 0.3)",
                   "rgba(26, 188, 156, 0.4)",
                   "rgba(231, 76, 60, 0.2)", "rgba(231, 76, 60, 0.2)",
                   "rgba(231, 76, 60, 0.2)", "rgba(231, 76, 60, 0.2)",
                   "rgba(231, 76, 60, 0.2)", "rgba(231, 76, 60, 0.2)"],
            customdata=[
                "✓ Has radius or mass → Continue",
                "✓ Rocky size → Terrestrial candidates",
                "✓ Temperature known → Can compute ESI",
                "✓ Realistic density → Physical validity",
                "✓ In habitable zone → Liquid water possible",
                "✓ Earth-like & well-placed → Final 8",
                "✓ Compute SEPHI → Rank by composite score",
                "❌ Missing both radius AND mass<br>Reason: Cannot estimate size or compute ESI",
                "❌ Radius > 1.6 R⊕<br>Reason: Gas giants/sub-Neptunes with H/He envelopes, not rocky",
                "❌ No equilibrium temperature<br>Reason: Missing stellar luminosity, radius, temp, or orbital distance",
                "❌ Density > 20 g/cm³<br>Reason: Unrealistic for rocky planets (Earth = 5.51, max known ~15-20)",
                "❌ HZD outside [-1, 1]<br>Reason: Too hot (HZD < -1) or too cold (HZD > 1) for liquid water",
                "❌ ESI < 0.75 or HZD_norm < 0.71<br>Reason: Not Earth-like enough or poorly placed in HZ",
            ],
            hovertemplate='<b>%{value} planets</b><br>%{customdata}<extra></extra>'
        )
    )])
    
    fig.update_layout(
        title="Exoplanet Pipeline Flow: 6,153 → 8 Candidates (Hover for details)",
        font_size=11,
        height=550,
        margin=dict(t=60, l=20, r=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Pipeline stages - flowing visual
    st.subheader("The Seven-Stage Journey")
    st.caption("From 6,153 exoplanets to 8 habitability candidates")
    
    st.markdown("")
    
    # Stage 1
    st.markdown("### 📊 Stage 1: Data Completeness Check")
    st.markdown("##### *Filtering Planets with No Size Information*")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Requirement", "Has R or M")
        st.metric("Result", "6,153 → 6,146", delta="−7", delta_color="off")
    with c2:
        st.markdown("""
        Before any analysis, we need basic size information. Planets must have **either radius OR mass** 
        recorded in the archive.
        
        7 planets had neither radius nor mass measurements and were dropped. The remaining 6,146 planets 
        proceed to the radius filter.
        """)
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Stage 2
    st.markdown("### 🪨 Stage 2: Radius Filter")
    st.markdown("##### *Identifying Terrestrial Planets*")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Threshold", "R ≤ 1.6 R⊕")
        st.metric("Result", "6,146 → 1,227", delta="−4,919", delta_color="off")
    with c2:
        st.markdown("""
        **The Fulton Gap** (Fulton et al., 2017) — an observed radius gap in the Kepler planet population 
        separates small, rocky planets from larger sub-Neptunes.
        
        Above 1.6 R⊕, planets retain thick hydrogen/helium envelopes, becoming gas giants structurally 
        unlike Earth. We keep only terrestrial-sized worlds. This is the largest filtering stage.
        """)
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Stage 3
    st.markdown("### 🌡️ Stage 3: Equilibrium Temperature")
    st.markdown("##### *Calculating or Verifying Temperature Data*")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Requirement", "T_eq calculable")
        st.metric("Result", "1,227 → 1,120", delta="−107", delta_color="off")
    with c2:
        st.markdown("""
        **Equilibrium temperature** is essential for ESI calculations. For planets missing T_eq, we calculate 
        it from stellar luminosity and orbital distance: T_eq = 278.5 × (1−albedo)^0.25 × L^0.25 / d^0.5
        
        107 planets lacked sufficient stellar data (luminosity, radius, temperature, or orbital distance) 
        to compute T_eq and were dropped.
        """)
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Stage 4
    st.markdown("### ⚖️ Stage 4: Density Validation")
    st.markdown("##### *Ensuring Physical Realism*")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Threshold", "ρ ≤ 20 g/cm³")
        st.metric("Result", "1,120 → 1,067", delta="−53", delta_color="off")
    with c2:
        st.markdown("""
        **Bulk density** is calculated from mass and radius. For rocky planets, typical densities range from 
        3-8 g/cm³ (Earth = 5.51 g/cm³). The densest known planets reach ~15-20 g/cm³.
        
        Densities above 20 g/cm³ indicate measurement errors or exotic compositions inconsistent with 
        terrestrial habitability. 53 planets with unrealistic densities were filtered out.
        """)
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Stage 5
    st.markdown("### ☀️ Stage 5: Habitable Zone Check")
    st.markdown("##### *Ensuring Orbital Position Allows Liquid Water*")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Threshold", "−1 ≤ HZD ≤ 1")
        st.metric("Result", "1,067 → 16", delta="−1,051", delta_color="off")
    with c2:
        st.markdown("""
        **Habitable Zone Distance** measures how far a planet is from its star's habitable zone.
        
        - HZD = 0 → planet at HZ center (ideal)
        - HZD = −1 → inner edge (too hot, runaway greenhouse)
        - HZD = +1 → outer edge (too cold, frozen)
        
        This is the second-largest drop: 1,051 planets fall outside the habitable zone. Only 16 remain 
        within the boundaries where liquid water could exist.
        """)
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Stage 6
    st.markdown("### 🎯 Stage 6: ESI & HZD Joint Filtering")
    st.markdown("##### *Earth-like Properties AND Well-Placed in HZ*")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Thresholds", "ESI ≥ 0.75 & HZD ≥ 0.71")
        st.metric("Result", "16 → 8", delta="−8", delta_color="off")
    with c2:
        st.markdown("""
        Two simultaneous filters are applied:
        
        **ESI ≥ 0.75:** Planet must be physically Earth-like (radius, density, escape velocity, temperature). 
        ESI = 1.0 is Earth-identical; ≥ 0.75 indicates strong similarity.
        
        **HZD_norm ≥ 0.71:** Planet must be well-centered in the HZ, not near the too-hot or too-cold edges. 
        HZD_norm = (1 − |HZD|)^0.5 normalizes the distance score.
        
        8 planets failed one or both criteria, leaving us with the **final 8 candidates**.
        """)
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Stage 7
    st.markdown("### ✨ Stage 7: SEPHI & Composite Ranking")
    st.markdown("##### *Comprehensive Habitability Assessment*")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Metric", "SEPHI + Composite")
        st.metric("Final Result", "8 → 8 (ranked)", delta="−0", delta_color="off")
    with c2:
        st.markdown("""
        **Statistical Exo-Planetary Habitability Index** (Rodríguez-Mozos & Moya, 2017) evaluates 
        four critical factors for all 8 candidates:
        
        - **L₁:** Rocky composition (telluric likelihood)
        - **L₂:** Atmosphere retention (escape velocity)
        - **L₃:** Liquid water potential (temperature + HZ position)
        - **L₄:** Magnetic field protection (stellar radiation shielding)
        
        All 8 planets successfully compute SEPHI. They are then ranked by **composite score** = 
        (ESI × HZD_norm × SEPHI)^(1/3), producing the final habitability ranking.
        """)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: FORMULAS & METRICS
# ─────────────────────────────────────────────────────────────────────────────

with tab2:
    st.header("Mathematical Framework")
    
    # ESI
    st.subheader("1️⃣ Earth Similarity Index (ESI)")
    st.latex(r"ESI = \prod_{i=1}^{4} \left(1 - \left|\frac{x_i - x_{i,\oplus}}{x_i + x_{i,\oplus}}\right|\right)^{w_i/n}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Parameters:**")
        st.markdown("- Radius (R)")
        st.markdown("- Density (ρ)")
        st.markdown("- Escape Velocity (v_esc)")
        st.markdown("- Equilibrium Temperature (T_eq)")
    
    with col2:
        st.markdown("**Earth Reference Values:**")
        for key, value in EARTH_REFERENCE.items():
            st.markdown(f"- {key}: **{value}**")
    
    st.markdown("**Weight Exponents:** w_radius=0.57, w_density=1.07, w_escvel=0.70, w_temp=5.58")
    
    st.divider()
    
    # HZD
    st.subheader("2️⃣ Habitable Zone Distance (HZD)")
    st.latex(r"HZD = \frac{d - d_{center}}{d_{width}}")
    st.latex(r"d_{center} = \frac{d_{inner} + d_{outer}}{2}, \quad d_{width} = \frac{d_{outer} - d_{inner}}{2}")
    st.latex(r"d_{inner} = 0.95\sqrt{L_\star}, \quad d_{outer} = 1.67\sqrt{L_\star}")
    
    st.markdown("**Normalized HZD:**")
    st.latex(r"HZD_{norm} = (1 - |HZD|)^{0.5}")
    
    st.divider()
    
    # SEPHI
    st.subheader("3️⃣ SEPHI (Statistical Exo-Planetary Habitability Index)")
    st.latex(r"SEPHI = (L_1 \times L_2 \times L_3 \times L_4)^{1/4}")
    
    st.markdown("""
    **Sub-indexes:**
    - **L₁:** Telluric likelihood (rocky composition)
    - **L₂:** Atmosphere retention (escape velocity)
    - **L₃:** Liquid water potential (HZ position + temperature)
    - **L₄:** Magnetic field likelihood (protection from stellar radiation)
    """)
    
    st.divider()
    
    # Composite Score
    st.subheader("4️⃣ Composite Habitability Score")
    st.latex(r"Score_{final} = (ESI \times HZD_{norm} \times SEPHI)^{1/3}")
    
    st.info("""
    **Why Geometric Mean?**
    
    Habitability factors are multiplicative — ALL conditions must be met simultaneously:
    - Liquid water requires BOTH appropriate temperature (ESI) AND orbital position (HZD)
    - Atmosphere retention (SEPHI) is meaningless without a habitable temperature range
    - A planet scoring 1.0 on two metrics but 0.0 on one is uninhabitable
    
    The geometric mean penalizes critical failures appropriately while rewarding strong multi-metric performance.
    """)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: RESULTS
# ─────────────────────────────────────────────────────────────────────────────

with tab3:
    st.header("Top Habitability Candidates")
    st.caption("Final 8 candidates ranked by composite score")
    
    # Top 8 table
    st.subheader("🏆 Top 8 Exoplanets")
    
    df_top = pd.DataFrame(TOP_CANDIDATES)
    
    # Color coding
    def color_score(val):
        if val >= 0.90:
            return 'background-color: #d4edda; color: #155724'
        elif val >= 0.85:
            return 'background-color: #d1ecf1; color: #0c5460'
        else:
            return 'background-color: #fff3cd; color: #856404'
    
    st.dataframe(
        df_top.style.format({
            "esi": "{:.6f}",
            "hzd": "{:.6f}",
            "sephi": "{:.6f}",
            "composite": "{:.6f}",
        }).applymap(color_score, subset=["composite"]),
        use_container_width=True,
        hide_index=True,
    )
    
    st.divider()
    
    # Scatter plot
    st.subheader("Candidate Landscape")
    
    fig = px.scatter(
        df_top,
        x="esi",
        y="composite",
        size="hzd",
        color="sephi",
        hover_name="name",
        hover_data={
            "esi": ":.6f",
            "hzd": ":.6f",
            "sephi": ":.6f",
            "composite": ":.6f",
        },
        color_continuous_scale="Viridis",
        size_max=20,
        labels={
            "esi": "ESI (Earth Similarity)",
            "composite": "Composite Score",
            "sephi": "SEPHI",
            "hzd": "HZD_norm"
        },
        title="Top 8 Candidates: ESI vs Composite Score"
    )
    
    fig.update_traces(marker=dict(line=dict(width=1, color='white')))
    fig.update_layout(height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Radar chart for top 3
    st.subheader("Top 3 Multi-dimensional Comparison")
    
    top3 = df_top.head(3)
    
    fig = go.Figure()
    
    for _, planet in top3.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[planet['esi'], planet['hzd'], planet['sephi'], planet['composite']],
            theta=['ESI', 'HZD_norm', 'SEPHI', 'Composite'],
            fill='toself',
            name=planet['name']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=True,
        height=500,
        title="Metric Comparison: Top 3 Candidates"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Notable planets
    st.divider()
    st.subheader("Notable Candidates")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🥇 GJ 1061 d")
        st.metric("Composite Score", "0.932182")
        st.markdown("**Highest overall score**")
        st.markdown("- ESI: 0.873787")
        st.markdown("- HZD: 0.999570 ⭐")
        st.markdown("- SEPHI: 0.927434")
        st.caption("Nearly perfect HZ placement")
    
    with col2:
        st.markdown("### 🌟 Wolf 1069 b")
        st.metric("Composite Score", "0.892727")
        st.markdown("**Best ESI score**")
        st.markdown("- ESI: 0.974170 ⭐")
        st.markdown("- HZD: 0.895218")
        st.markdown("- SEPHI: 0.815817")
        st.caption("Most Earth-like physically")
    
    with col3:
        st.markdown("### 🎯 TRAPPIST-1 e")
        st.metric("Composite Score", "0.865980")
        st.markdown("**Famous system**")
        st.markdown("- ESI: 0.951359")
        st.markdown("- HZD: 0.903434")
        st.markdown("- SEPHI: 0.755585")
        st.caption("Part of 7-planet system")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4: METHODOLOGY
# ─────────────────────────────────────────────────────────────────────────────

with tab4:
    st.header("Methodology & References")
    
    st.subheader("Phase 1 Pipeline Design")
    
    st.markdown("""
    This analysis implements a **conservative, physics-based filtering pipeline** to identify 
    potentially habitable exoplanets from NASA's Exoplanet Archive.
    
    ### Design Principles
    
    1. **Multi-stage filtering** — Each stage removes planets that fail a specific habitability criterion
    2. **Conservative thresholds** — Stricter than minimum requirements to focus on best candidates
    3. **Physical realism** — All metrics based on observable properties and established physics
    4. **Geometric aggregation** — Multiplicative scoring reflects that ALL conditions must be met
    
    ### Key Innovations
    
    - **Strict HZ placement:** HZD_norm ≥ 0.71 ensures planets are well within HZ, not at edges
    - **SEPHI integration:** Captures atmosphere retention, magnetic protection, and tidal effects
    - **Radius-mass relation:** Handles missing data using Chen & Kipping (2017) empirical law
    - **Composite scoring:** Geometric mean balances penalties and rewards appropriately
    """)
    
    st.divider()
    
    st.subheader("References")
    
    st.markdown("""
    **Primary Indices:**
    - **ESI:** Schulze-Makuch et al. (2011) — *A Two-Tiered Approach to Assessing the Habitability of Exoplanets*
    - **SEPHI:** Rodríguez-Mozos & Moya (2017) — *Statistical Likelihood Exo-Planetary Habitability Index (SEPHI)*
    - **HZ Boundaries:** Kopparapu et al. (2013) — *Habitable Zones Around Main-Sequence Stars*
    
    **Supporting Science:**
    - **Fulton Gap:** Fulton et al. (2017) — *The California-Kepler Survey. III. A Gap in the Radius Distribution of Small Planets*
    - **Mass-Radius:** Chen & Kipping (2017) — *Probabilistic Forecasting of Masses and Radii*
    - **Tidal Locking:** Sano et al. (2016) — *Magnetic field generation in tidally locked planets*
    
    **Data Source:**
    - NASA Exoplanet Archive — Planetary Systems Composite Parameters (PSCompPars)
    - Downloaded: 2026.03.31
    - Total planets: 6,153
    """)
    
    st.divider()
    
    st.subheader("Limitations & Future Work")
    
    with st.expander("Known Limitations", expanded=False):
        st.markdown("""
        1. **Missing data** — 12 planets dropped at SEPHI stage due to incomplete stellar parameters
        2. **Equilibrium vs. Surface Temperature** — Using T_eq instead of T_surface (not measurable)
        3. **Atmospheric assumptions** — Cannot directly measure atmospheric composition or pressure
        4. **Tidal locking** — SEPHI approximates but doesn't fully model tidally locked habitability
        5. **Magnetic field proxy** — Estimated from mass and age; rotation rates unavailable
        """)
    
    with st.expander("Future Enhancements (Phase 2)", expanded=False):
        st.markdown("""
        ### Phase 2: Tidally Locked Habitability Index (TLHI)
        
        **The Current Gap in Habitability Assessment:**
        
        Most potentially habitable exoplanets orbit close to their host stars (especially M-dwarfs) and are 
        likely **tidally locked** — one side permanently facing the star, the other in eternal darkness. 
        Yet existing habitability indices don't adequately handle this regime:
        
        **Three Critical Problems:**
        
        1. **Fragmented Modeling** — Individual components exist in isolation:
           - Rotation dynamics models
           - 3D climate simulations (GCMs)
           - Wind-magnetosphere interaction studies
           
           Papers exist for each separately, but **no unified scoring framework** integrates them all.
        
        2. **Binary Assumptions vs. Expensive Simulations** — The field is stuck between two extremes:
           - **Binary classification:** Planet is either "locked" or "not locked" (oversimplified)
           - **Case-by-case 3D GCMs:** Computationally prohibitive for large-scale surveys
           
           **Nothing exists in between** — no fast, scalable, probability-weighted metric.
        
        3. **All-or-Nothing Treatment** — Current indices:
           - **ESI, HZD:** Assume tidally rotating planets (don't model locking effects)
           - **SEPHI:** Partially addresses through magnetic field scaling only (L₄ sub-index)
           - **HITE (Barnes et al. 2015):** Habitability Index for Tidally-locked Exoplanets — 
             closest existing work, but uses **binary locked/unlocked assumption**
        
        ---
        
        **What Phase 2 Will Add:**
        
        **TLHI (Tidally Locked Habitability Index)** — A probability-weighted framework that:
        
        ✅ **Continuous Locking Probability (P_lock)** — Not binary. Handles the full spectrum:
        - Fully rotating (P_lock = 0)
        - Spin-orbit resonances (0 < P_lock < 1)
        - Partially locked states
        - Fully locked (P_lock = 1)
        
        ✅ **Unified Sub-Index System** — Integrates previously isolated components:
        - **L₁_TLHI:** Atmospheric circulation (day-night heat transport)
        - **L₂_TLHI:** Tidal heating flux (internal energy budget)
        - **L₃_TLHI:** XUV-driven atmospheric escape (M-dwarf radiation)
        - **L₄_TLHI:** Wind-magnetosphere coupling (protection mechanisms)
        
        ✅ **Blended Scoring** — Probability-weighted composite:
        ```
        Final_Score = (1 - P_lock) × SEPHI + P_lock × TLHI
        ```
        Smoothly transitions from rotating-planet physics to tidally-locked physics.
        
        ---
        
        **Key Distinction from HITE:**
        
        HITE (Barnes et al. 2015) addresses tidally locked planets but treats locking as **binary** — 
        a planet either is or isn't locked, and if it is, HITE applies.
        
        **TLHI's Innovation:** Uses P_lock as a **continuous probability**, meaning it handles:
        - 3:2 spin-orbit resonances (like Mercury)
        - Planets near the tidal locking boundary
        - Gradual transition states
        - Full spectrum without arbitrary cutoffs
        
        HITE has **no equivalent of the blending formula**. This is the genuine gap TLHI fills.
        
        ---
        
        **Phase 2 Methodology Structure:**
        
        1. Existing indices (ESI, HZD, SEPHI) handle **rotating planets**
        2. Most HZ candidates around M-dwarfs are **tidally locked**
        3. SEPHI partially addresses this (L₄ magnetic scaling only)
        4. 3D GCMs model individual cases but are **computationally prohibitive** for surveys
        5. HITE addresses locked planets but uses **binary assumptions**
        6. **The gap:** No unified, probability-weighted framework for the full locking spectrum
        7. **Our contribution:** TLHI + P_lock blending
        
        Phase 2 will make this analysis applicable to the vast population of M-dwarf exoplanets — 
        the most common potentially habitable worlds in the galaxy.
        """)

# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════

st.divider()

st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
<p><strong>ESI_Hab Pipeline Demo</strong> • Phase 1 Methodology Visualization</p>
<p>Data from NASA Exoplanet Archive (PSCompPars) • 2026.03.31</p>
<p>No installation required • No API calls • Pure demonstration</p>
</div>
""", unsafe_allow_html=True)
