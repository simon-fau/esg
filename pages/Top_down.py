import streamlit as st

def display_page():
    # Initialize the checkbox states if not already in the session state
    if 'eis' not in st.session_state:
        st.session_state.eis = {'Ja': False, 'Nein': False, 'Vielleicht': False}
    if 'kartoffeln' not in st.session_state:
        st.session_state.kartoffeln = {'Ja': False, 'Nein': False, 'Vielleicht': False}
    if 'handy' not in st.session_state:
        st.session_state.handy = {'Ja': False, 'Nein': False, 'Vielleicht': False}

    st.title('Produkt-Auswahl mit Erinnerung')

    with st.form("my_form"):
        # Use columns to arrange checkboxes horizontally
        options = ['Ja', 'Nein', 'Vielleicht']

        st.header("Eis:")
        cols_eis = st.columns(len(options))
        eis_inputs = {}
        for i, option in enumerate(options):
            with cols_eis[i]:
                eis_inputs[option] = st.checkbox(option, value=st.session_state.eis[option], key=f"eis_{option}")
        
        st.header("Kartoffeln:")
        cols_kartoffeln = st.columns(len(options))
        kartoffeln_inputs = {}
        for i, option in enumerate(options):
            with cols_kartoffeln[i]:
                kartoffeln_inputs[option] = st.checkbox(option, value=st.session_state.kartoffeln[option], key=f"kartoffeln_{option}")

        st.header("Handy:")
        cols_handy = st.columns(len(options))
        handy_inputs = {}
        for i, option in enumerate(options):
            with cols_handy[i]:
                handy_inputs[option] = st.checkbox(option, value=st.session_state.handy[option], key=f"handy_{option}")

        # Submit button to save the form inputs
        submitted = st.form_submit_button("Auswahl speichern")
        if submitted:
            # Update the session state based on the form inputs
            for key in eis_inputs:
                st.session_state.eis[key] = eis_inputs[key]
            for key in kartoffeln_inputs:
                st.session_state.kartoffeln[key] = kartoffeln_inputs[key]
            for key in handy_inputs:
                st.session_state.handy[key] = handy_inputs[key]
            st.success("Auswahl erfolgreich gespeichert!")