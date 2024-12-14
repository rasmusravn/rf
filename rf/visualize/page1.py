import sys

import matplotlib.pyplot as plt
import pandas as pd
import skrf as rf
import streamlit as st


def load_data(source: str, file_type: str):
    """
    Load data based on the file type.
    """
    try:
        if file_type == "s2p":
            network = rf.Network(source)
            return network
        elif file_type == "csv":
            return pd.read_csv(source)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None


def s2p_script(data: rf.Network) -> None:
    col1, col2, col3 = st.columns([1, 1, 1])
    st.write("Displaying all possible plots from the provided S2P data.")

    with col1:
        # Plot 1: Smith Chart
        st.header("Smith Chart")
        fig, ax = plt.subplots()
        data.plot_s_smith(ax=ax)
        st.pyplot(fig)

    with col2:
        # Plot 2: Magnitude of S-parameters
        st.header("Magnitude of S-parameters")
        fig, ax = plt.subplots()
        data.plot_s_db(ax=ax)
        st.pyplot(fig)

    with col3:
        # Plot 3: Phase of S-parameters
        st.header("Phase of S-parameters")
        fig, ax = plt.subplots()
        data.plot_s_deg(ax=ax)
        st.pyplot(fig)

    with col1:
        # Plot 4: Real and Imaginary parts of S-parameters
        st.header("Real and Imaginary Parts of S-parameters")
        fig, ax = plt.subplots()
        data.plot_s_re(ax=ax)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        data.plot_s_im(ax=ax)
        st.pyplot(fig)

    with col3:
        # Plot 5: Group Delay
        st.header("stats")
        fig, ax = plt.subplots()
        data.plot_it_all(ax=ax)
        st.pyplot(fig)


def csv_script(data):
    st.dataframe(data)


def main():
    st.set_page_config(layout="wide")
    st.title("RF Visualization Tool")

    # Read arguments from the CLI
    if len(sys.argv) > 2:
        data_source = sys.argv[1]
        file_type = sys.argv[2].lower()
    else:
        st.error("No file or file type provided!")
        return

    data = load_data(data_source, file_type)
    if data is not None:
        st.write("Preview of Data:")
        if file_type == "s2p":
            s2p_script(data)
        elif file_type == "csv":
            csv_script(data)


if __name__ == "__main__":
    main()
