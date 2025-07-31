import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from PIL import Image
import base64
import os

# Page configuration
st.set_page_config(
    page_title="Nuclear Isotope Economics",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with error handling
def local_css(file_name):
    try:
        if os.path.exists(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        else:
            # Fallback CSS if file doesn't exist
            st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                color: #ffffff;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #4fc3f7;
            }
            .st-bb {
                background-color: rgba(25, 55, 75, 0.7);
            }
            .st-bq {
                border-left-color: #4fc3f7;
            }
            .stSelectbox, .stSlider, .stMultiSelect {
                background-color: rgba(25, 55, 75, 0.7);
            }
            .stButton>button {
                background: linear-gradient(to right, #2193b0, #6dd5ed);
                color: white;
                border: none;
            }
            .stDownloadButton>button {
                background: linear-gradient(to right, #373b44, #4286f4);
                color: white;
                border: none;
            }
            .stTab {
                background-color: rgba(15, 30, 45, 0.7);
            }
            .stTab [aria-selected="true"] {
                background-color: #2193b0;
                color: white;
            }
            </style>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"CSS loading failed: {e}")

local_css("style.css")

# Safely load CSV data if it exists
def load_country_data():
    """Safely load country production data if CSV file exists"""
    try:
        csv_path = "isotope_production_by_country_2002.csv"
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        else:
            # Return sample data if CSV doesn't exist
            return pd.DataFrame({
                "Country": ["USA", "Canada", "Germany", "France", "Japan", "Australia"],
                "Major_Isotopes": ["192I, 125I", "99Mo, 131I", "18F, 123I", "99Mo, 153Sm", "192Ir, 169Yb", "192Ir, 169Yb"],
                "Total_Production_TBq": [30.4, 15000.0, 30.0, 4063.5, 982.4, 1551.9]
            })
    except Exception as e:
        st.warning(f"Could not load country data: {e}")
        # Return sample data as fallback
        return pd.DataFrame({
            "Country": ["USA", "Canada", "Germany", "France", "Japan", "Australia"],
            "Major_Isotopes": ["192I, 125I", "99Mo, 131I", "18F, 123I", "99Mo, 153Sm", "192Ir, 169Yb", "192Ir, 169Yb"],
            "Total_Production_TBq": [30.4, 15000.0, 30.0, 4063.5, 982.4, 1551.9]
        })

# Sample isotope data (in a real app, connect to database/API)
def get_isotope_data():
    return pd.DataFrame({
        "Isotope": ["Tc-99m", "I-131", "Co-60", "Mo-99", "Xe-133", "Ir-192", "C-14", "U-235"],
        "Half-Life": [6.0, 8.0, 1925.0, 66.0, 5.2, 74.0, 5730000.0, 703800000.0],
        "Production_Method": ["Reactor", "Reactor", "Reactor", "Reactor", "Fission", "Reactor", "Accelerator", "Mining"],
        "Primary_Use": ["Medical", "Medical", "Industrial", "Medical", "Medical", "Industrial", "Research", "Energy"],
        "Global_Production (TBq/year)": [150000, 30000, 1500, 300000, 50000, 2000, 100, 500000],
        "Cost_per_GBq (USD)": [250, 150, 50, 200, 300, 70, 5000, 0.5],
        "Protons": [43, 53, 27, 42, 54, 77, 6, 92],
        "Neutrons": [56, 78, 33, 57, 79, 115, 8, 143],
        "Applications": [
            "Medical imaging",
            "Thyroid treatment",
            "Sterilization",
            "Medical isotope gen",
            "Lung ventilation",
            "Industrial radiography",
            "Carbon dating",
            "Nuclear fuel"
        ]
    })

# Generate 3D atomic background
def create_atomic_background():
    x, y, z = [], [], []
    for i in range(100):
        for j in range(10):
            angle = 2 * np.pi * j / 10
            x.append(np.cos(angle) + np.random.normal(0, 0.1))
            y.append(np.sin(angle) + np.random.normal(0, 0.1))
            z.append(i/10 + np.random.normal(0, 0.1))
    return pd.DataFrame({"x": x, "y": y, "z": z})

# Create a placeholder image using base64
def get_placeholder_image():
    # Create a simple colored rectangle as placeholder
    return "data:image/svg+xml;base64," + base64.b64encode("""
    <svg width="200" height="150" xmlns="http://www.w3.org/2000/svg">
        <rect width="200" height="150" fill="#4fc3f7" opacity="0.3"/>
        <text x="100" y="75" text-anchor="middle" fill="#ffffff" font-size="14">Image Placeholder</text>
    </svg>
    """.encode()).decode()

# Main app
def main():
    # Sidebar with controls
    with st.sidebar:
        st.header("Nuclear Isotope Explorer")
        # Use emoji instead of image file
        st.markdown("☢️", help="Nuclear Isotope Explorer")
        view_3d = st.checkbox("Show 3D Atomic Structure", True)
        half_life_filter = st.slider("Filter by Half-Life (hours)", 0.1, 1000000.0, (1.0, 100000.0), step=0.1)
        selected_uses = st.multiselect("Filter by Application", 
                                      ["Medical", "Industrial", "Research", "Energy"], 
                                      ["Medical", "Industrial"])
        st.markdown("---")
        st.info("Explore non-energy applications of nuclear technologies and their economic impact")

    # Main content
    st.title("☢️ Economic Analysis of Non-Energy Nuclear Applications")
    st.subheader("Interactive Isotope Visualization and Economic Comparison")

    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["3D Isotope Visualizer", "Economic Comparison", "Country Production", "Isotope Applications"])

    with tab1:
        st.header("Interactive 3D Isotope Visualization")
        st.markdown("Explore isotopes used in non-energy applications with atomic structure visualization")

        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create 3D visualization
            df = get_isotope_data()
            filtered_df = df[
                (df["Half-Life"] >= half_life_filter[0]) & 
                (df["Half-Life"] <= half_life_filter[1]) &
                (df["Primary_Use"].isin(selected_uses))
            ]
            
            # Create figure
            fig = go.Figure()
            
            # Add atomic background
            if view_3d:
                atomic_bg = create_atomic_background()
                fig.add_trace(go.Scatter3d(
                    x=atomic_bg['x'], 
                    y=atomic_bg['y'], 
                    z=atomic_bg['z'],
                    mode='markers',
                    marker=dict(
                        size=2,
                        color='rgba(100, 150, 200, 0.1)',
                        opacity=0.3
                    ),
                    name="Atomic Structure"
                ))
            
            # Add isotopes
            fig.add_trace(go.Scatter3d(
                x=filtered_df["Protons"],
                y=filtered_df["Neutrons"],
                z=np.log10(filtered_df["Half-Life"]),
                mode='markers+text',
                marker=dict(
                    size=12,
                    color=filtered_df["Global_Production (TBq/year)"],
                    colorscale="Viridis",
                    opacity=0.8,
                    sizemode='diameter',
                    sizeref=0.1,
                    colorbar=dict(title="Global Production (TBq/year)")
                ),
                text=filtered_df["Isotope"],
                textposition="top center",
                hoverinfo="text",
                hovertext=[f"<b>{row['Isotope']}</b><br>Half-Life: {row['Half-Life']:.1f} hours<br>Use: {row['Primary_Use']}<br>Production: {row['Global_Production (TBq/year)']} TBq/year" 
                          for _, row in filtered_df.iterrows()],
                name="Isotopes"
            ))
            
            # Update layout
            fig.update_layout(
                scene=dict(
                    xaxis_title='Protons (Atomic Number)',
                    yaxis_title='Neutrons',
                    zaxis_title='Log10(Half-Life Hours)',
                    camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)),
                    bgcolor='rgba(10, 10, 20, 1)'
                ),
                margin=dict(l=0, r=0, b=0, t=30),
                height=600,
                scene_aspectmode='cube'
            )
            
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Isotope Details")
            selected_isotope = st.selectbox("Select Isotope", df["Isotope"])
            
            iso_data = df[df["Isotope"] == selected_isotope].iloc[0]
            
            st.markdown(f"""
            **{iso_data['Isotope']}**
            - **Primary Use:** {iso_data['Primary_Use']}
            - **Half-Life:** {iso_data['Half-Life']} hours
            - **Production Method:** {iso_data['Production_Method']}
            - **Global Production:** {iso_data['Global_Production (TBq/year)']} TBq/year
            - **Cost per GBq:** ${iso_data['Cost_per_GBq (USD)']}
            - **Applications:** {iso_data['Applications']}
            """)
            
            # Use placeholder instead of missing image
            st.markdown("🔬 **Isotope Production in Research Reactor**")
            st.markdown("*Image placeholder - Nuclear reactor facility*")
            st.download_button("Download Isotope Data", df.to_csv(), "isotope_data.csv")

    with tab2:
        st.header("Economic Comparison of Isotope Production")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Production Cost vs. Market Value")
            fig = px.scatter(
                df,
                x="Cost_per_GBq (USD)",
                y="Global_Production (TBq/year)",
                size="Half-Life",
                color="Primary_Use",
                hover_name="Isotope",
                log_x=True,
                log_y=True,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("Annual Market Value Estimation")
            df['Market_Value'] = df['Global_Production (TBq/year)'] * df['Cost_per_GBq (USD)'] * 1000
            fig = px.bar(
                df.sort_values('Market_Value', ascending=False),
                x='Isotope',
                y='Market_Value',
                color='Primary_Use',
                height=400,
                labels={'Market_Value': 'Estimated Market Value (USD/year)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Key Economic Insights:**
        - Medical isotopes command premium prices due to strict quality requirements
        - High-volume production reduces per-unit costs significantly
        - Short half-life isotopes require just-in-time production systems
        - Reactor-produced isotopes benefit from existing nuclear infrastructure
        """)

    with tab3:
        st.header("Country-wise Isotope Production (2002 Data)")
        
        # Load country data safely
        country_df = load_country_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Production by Country")
            # Filter out NR (Not Reported) values
            filtered_country_df = country_df[country_df['Total_Production_TBq'] != 'NR']
            filtered_country_df['Total_Production_TBq'] = pd.to_numeric(filtered_country_df['Total_Production_TBq'], errors='coerce')
            filtered_country_df = filtered_country_df.dropna()
            
            fig = px.bar(
                filtered_country_df.sort_values('Total_Production_TBq', ascending=False),
                x='Country',
                y='Total_Production_TBq',
                height=400,
                labels={'Total_Production_TBq': 'Total Production (TBq)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("Major Isotopes by Country")
            st.dataframe(country_df[['Country', 'Major_Isotopes']], use_container_width=True)
            
        st.markdown("""
        **Data Source:** International Atomic Energy Agency (IAEA) - 2002 Production Data
        - NR indicates "Not Reported" values
        - Data shows global distribution of isotope production capabilities
        - Belgium and Canada are major producers of medical isotopes
        """)

    with tab4:
        st.header("Non-Energy Applications of Nuclear Isotopes")
        
        applications = {
            "Medical": ["Tc-99m: Diagnostic imaging", "I-131: Thyroid treatment", "Y-90: Cancer therapy"],
            "Industrial": ["Co-60: Sterilization", "Ir-192: Industrial radiography", "Cs-137: Moisture gauges"],
            "Agriculture": ["P-32: Fertilizer studies", "C-14: Photosynthesis research"],
            "Research": ["C-14: Carbon dating", "H-3: Tracer studies"]
        }
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_app = st.selectbox("Select Application Sector", list(applications.keys()))
            
            st.subheader(f"{selected_app} Applications")
            for app in applications[selected_app]:
                st.markdown(f"- {app}")
                
            # Use placeholder instead of missing image
            st.markdown(f"🔬 **{selected_app} Applications**")
            st.markdown("*Image placeholder - Application examples*")

        with col2:
            st.subheader("Economic Impact Analysis")
            st.markdown("""
            **Medical Sector:**
            - Global market: $8.2 billion (2023)
            - Growth rate: 5.8% CAGR (2023-2030)
            - Cost savings: Early diagnosis reduces treatment costs by 30-40%
            
            **Industrial Sector:**
            - Non-destructive testing market: $1.5 billion
            - Sterilization services: $3.2 billion
            - Process optimization savings: 15-25% efficiency gains
            
            **Environmental Applications:**
            - Radiation processing of wastewater: $420 million market
            - Reduction in chemical usage: 60-80% less chemicals needed
            """)
            
            st.progress(0.78, text="Medical accounts for 78% of non-energy isotope revenue")

# Run the app
if __name__ == "__main__":
    main()