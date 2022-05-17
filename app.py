import streamlit as st
import pandas as pd

from PIL import Image

# from helper import sqlite_setup

image = Image.open("logo.png")
st.set_page_config(
    page_title="GHG Emissions Calculator",
    page_icon=image,
    layout="wide",
    menu_items={
        # 'Get Help': '',
        # 'Report a bug': "",
        'About': "Testing APP"
    }
)

sidebar_image = Image.open("logo.png")
st.sidebar.image(
    sidebar_image
)

guide_df = pd.read_csv("new.csv")
emiss_factors = guide_df["Level"].unique()


def app():
    ####################################################################################
    # Sidebar
    ####################################################################################

    with st.sidebar:
        # Select emission factors that are applicable for a company
        selected_sources = st.multiselect("Select emission source you want to calculate", options=emiss_factors)
        all_options = st.checkbox("Select all options")

        if all_options:
            selected_sources = emiss_factors

        with st.expander("Do you want to add more sources?"):
            selected_sources_extra = st.multiselect("Select emission sources",
                                                    options=emiss_factors)

    ####################################################################################
    # Page
    ####################################################################################

    total_df = pd.DataFrame()
    count = 0

    for item in selected_sources:
        st.subheader(item)
        count += 1

        selected_level1 = st.selectbox("Level - 1 source:",
                                       options=(guide_df["Level.1"][guide_df["Level"] == item]).unique(), key=count)

        selected_level2 = st.selectbox("Level - 2 source",
                                       options=(guide_df["Level.2"][guide_df["Level.1"] == selected_level1]).unique(),
                                       key=count)

        selected_level3 = st.selectbox("Level - 3 source",
                                       options=(guide_df["Level.3"][guide_df["Level.2"] == selected_level2]).unique(),
                                       key=count)

        if selected_level1 == "Water supply":
            selected_text = st.selectbox("Level - 4 units",
                                         options=(
                                             guide_df["Unit"][guide_df["Level.1"] == selected_level1]).unique(),
                                         key=count)

        elif selected_level3 == "None":
            selected_text = st.selectbox("Level - 4 source",
                                         options=(
                                             guide_df["Column Text"][guide_df["Level.2"] == selected_level2]).unique(),
                                         key=count)

        else:
            selected_text = st.selectbox("Level - 4 source", options=(
                guide_df["Column Text"][guide_df["Level.3"] == selected_level3]).unique(), key=count)

        if item == "Water supply":
            units = selected_text
            value = st.number_input(f"Enter value for {selected_level1} in {units}", key=count)

        else:
            units = guide_df["Unit"][guide_df["Column Text"] == selected_text].unique()
            value = st.number_input(f"Enter value for {selected_text} in {units[0]}", key=count)

        if item == "Water supply":
            ghg_emiss = guide_df[["Scope", "GHG", "GHG Emission factor"]][
                                                                    (guide_df["Level.1"] == selected_level1) &
                                                                    (guide_df["Unit"] == selected_text)
            ]
        else:
            ghg_emiss = guide_df[["Scope", "GHG", "GHG Emission factor"]][
                                                                     (guide_df["Level.1"] == selected_level1) &
                                                                     (guide_df["Level.2"] == selected_level2) &
                                                                     (guide_df["Level.3"] == selected_level3) &
                                                                     (guide_df["Column Text"] == selected_text) &
                                                                     (guide_df["Unit"] == units[0])
                                                                     ]

        emission_factors = pd.to_numeric(ghg_emiss["GHG Emission factor"], errors='coerce')
        ghg_emiss[f"{selected_level2} {selected_text} emissions"] = emission_factors * value

        st.write(ghg_emiss)

        total_df = total_df.append(ghg_emiss)
    st.write(total_df)
    x = total_df[total_df.GHG == "CO2e"]
    st.info(x.sum(axis=0, skipna=True))

if __name__ == '__main__':
    app()
