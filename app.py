import streamlit as st
import pandas as pd
import plotly.express as px

from PIL import Image
from helper import calculate_emissions

logo_page = Image.open("logo_page.png")
image = Image.open("logo.png")
st.set_page_config(
    page_title="GHG Emissions Calculator",
    page_icon=logo_page,
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

        # adding extra source of emissions
        add_extra_source = st.checkbox("Add additional source")
        if add_extra_source:
            extra_source_selected = st.multiselect("Select additional source you want to calculate",
                                                   options=emiss_factors)

    ####################################################################################
    # Page
    ####################################################################################

    total_df = pd.DataFrame()
    count = 0

    for source in selected_sources:
        st.subheader(source)
        count += 1
        ghg_emiss = calculate_emissions(guide_df, source, count)
        total_df = total_df.append(ghg_emiss)

    if add_extra_source:
        for extra_source in extra_source_selected:
            st.subheader(extra_source)
            count += 2
            ghg_emiss = calculate_emissions(guide_df, extra_source, count)
            total_df = total_df.append(ghg_emiss)
    else:
        pass

    # generate dataframe with results
    try:
        # group by Scope
        df_scope_ghg = total_df.groupby(['Scope']).sum()
        # create bar chart
        fig_1 = px.bar(df_scope_ghg)
        fig_1.update(layout_showlegend=False)
        st.plotly_chart(fig_1, use_container_width=True)

        # group by GHG gas
        df_ghg = total_df.groupby(['GHG']).sum()
        df_ghg = df_ghg.drop("Scope", axis=1)
        # create bar chart
        fig_2 = px.bar(df_ghg)
        fig_2.update(layout_showlegend=False)
        st.plotly_chart(fig_2, use_container_width=True)
    except KeyError:
        pass


if __name__ == '__main__':
    app()
