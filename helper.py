# functions to support app.py

import streamlit as st
import pandas as pd


def calculate_emissions(data, item, count):

    selected_level1 = st.selectbox("Level - 1 source:",
                                   options=(data["Level.1"][data["Level"] == item]).unique(), key=f"l1{count}")

    selected_level2 = st.selectbox("Level - 2 source",
                                   options=(data["Level.2"][data["Level.1"] == selected_level1]).unique(),
                                   key=f"l2{count}")

    selected_level3 = st.selectbox("Level - 3 source",
                                   options=(data["Level.3"][data["Level.2"] == selected_level2]).unique(),
                                   key=f"l3{count}")

    if selected_level1 == "Water supply":
        selected_text = st.selectbox("Level - 4 units",
                                     options=(
                                         data["Unit"][data["Level.1"] == selected_level1]).unique(),
                                     key=f"l4{count}")

    elif selected_level3 == "None":
        selected_text = st.selectbox("Level - 4 source",
                                     options=(
                                         data["Column Text"][data["Level.2"] == selected_level2]).unique(),
                                     key=f"l4_1{count}")

    else:
        selected_text = st.selectbox("Level - 4 source", options=(
            data["Column Text"][data["Level.3"] == selected_level3]).unique(), key=f"l4_2{count}")

    if item == "Water supply":
        units = selected_text
        value = st.number_input(f"Enter value for {selected_level1} in {units}", key=f"water{count}")

    else:
        units = data["Unit"][data["Column Text"] == selected_text].unique()
        value = st.number_input(f"Enter value for {selected_text} in {units[0]}", key=f"unit{count}")

    if item == "Water supply":
        ghg_emiss = data[["Scope", "GHG", "GHG Emission factor"]][
            (data["Level.1"] == selected_level1) &
            (data["Unit"] == selected_text)
            ]
    else:
        ghg_emiss = data[["Scope", "GHG", "GHG Emission factor"]][
            (data["Level.1"] == selected_level1) &
            (data["Level.2"] == selected_level2) &
            (data["Level.3"] == selected_level3) &
            (data["Column Text"] == selected_text) &
            (data["Unit"] == units[0])
            ]

    emission_factors = pd.to_numeric(ghg_emiss["GHG Emission factor"], errors='coerce')
    ghg_emiss[f"{selected_level1} {selected_level2} {selected_text} emissions"] = emission_factors * value

    # st.write(ghg_emiss)
    return ghg_emiss
