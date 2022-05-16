import streamlit as st
import pandas as pd

# from PIL import Image

# from helper import sqlite_setup

# image = Image.open("logo.png")
st.set_page_config(
    page_title="GHG Emissions Calculator",
    # page_icon=image,
    layout="wide",
    menu_items={
        # 'Get Help': '',
        # 'Report a bug': "",
        'About': "Testing APP"
    }
)

# sidebar_image = Image.open("sidebar_logo.png")
# st.sidebar.image(
#     sidebar_image
# )

guide_df = pd.read_csv("new.csv")
st.dataframe(guide_df)

emiss_factors = guide_df["Level"].unique()


def app():
    ####################################################################################
    # Sidebar
    ####################################################################################

    with st.sidebar:
        # Select emission factors that are applicable for a company
        selected_sources = st.multiselect("Select emission source you want to calculate", options=emiss_factors)

    ####################################################################################
    # Page
    ####################################################################################

    # def get_values(df, column_name, next_column):

    #     for item in selected_sources:
    #         st.subheader(item)

    #         if df[f"{column_name}"] != None:
    #             selected_option = st.selectbox(f"{column_name} source:",
    #             options=(df[f"{next_column}"][df[f"{column_name}"] == item]).unique())
    #         else:
    #             selected_option = st.info("Nothing to select!..")

    #             return selected_option

    # get_values(guide_df, column_name="Level", next_column="Level.1")
    total_df = pd.DataFrame()

    for item in selected_sources:
        st.subheader(item)

        selected_level1 = st.selectbox("Level - 1 source:",
                                       options=(guide_df["Level.1"][guide_df["Level"] == item]).unique())

        selected_level2 = st.selectbox("Level - 2 source",
                                       options=(guide_df["Level.2"][guide_df["Level.1"] == selected_level1]).unique())

        selected_level3 = st.selectbox("Level - 3 source",
                                       options=(guide_df["Level.3"][guide_df["Level.2"] == selected_level2]).unique())

        if selected_level3 is not None:
            selected_text = st.selectbox("Level - 4 source",
                                         options=(
                                         guide_df["Column Text"][guide_df["Level.2"] == selected_level2]).unique())
        else:
            selected_text = st.selectbox("Level - 4 source",
                                         options=(
                                         guide_df["Column Text"][guide_df["Level.3"] == selected_level3]).unique())

        units = guide_df["Unit"][guide_df["Column Text"] == selected_text].unique()

        value = st.number_input(f"Enter value for {selected_text} in {units[0]}")

        if selected_level3 is not None:
            ghg_emiss = guide_df[["GHG", "GHG Emission factor"]][(guide_df["Column Text"] == selected_text) &
                                                                 (guide_df["Level.2"] == selected_level2)]
        else:
            ghg_emiss = guide_df[["GHG", "GHG Emission factor"]][(guide_df["Column Text"] == selected_text) &
                                                                 (guide_df["Level.2"] == selected_level2) & (
                                                                             guide_df["Level.3"] == selected_level3)]

        ghg_emiss[f"{selected_level2} {selected_text} emissions"] = ghg_emiss["GHG Emission factor"] * value

        st.write(ghg_emiss)

        total_df = total_df.append(ghg_emiss)

        # total_df.append(total_df, ignore_index=True)

    st.write(total_df)

    # Stationary combustion fuel
    # st.info(f"CO2 = {}, CH4 = {}, N20 = {}, Total CO2 = {}")


if __name__ == '__main__':
    app()

