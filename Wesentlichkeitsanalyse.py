import streamlit as st

def display_page():

    # Sidebar navigation for Wesentlichkeitsanalyse
    st.sidebar.title("Wesentlichkeitsanalyse")
    page_option = st.sidebar.selectbox(
        "Wählen Sie eine Option:",
        [
            '1. Stakeholder Management',
            '2. Themenspezifische ESRS',
            '3. Interne Nachhaltigkeitspunkte',
            '4. Externe Nachhaltigkeitspunkte',
            '5. Bewertung der Longlist',
            '6. Erstellung der Shortlist'
        ]
    )

    # Navigation logic
    if page_option == '1. Stakeholder Management':
        st.Page("pages/Stakeholder_Management.py")
    elif page_option == '2. Themenspezifische ESRS':
        st.Page("pages/Themenspezifische_ESRS.py")
    elif page_option == '3. Interne Nachhaltigkeitspunkte':
        st.Page("pages/Interne_Nachhaltigkeitspunkte.py")
    elif page_option == '4. Externe Nachhaltigkeitspunkte':
        st.Page("pages/Externe_Nachhaltigkeitspunkte.py")
    elif page_option == '5. Bewertung der Longlist':
        st.Page("pages/Longlist.py")
    elif page_option == '6. Erstellung der Shortlist':
        st.Page("pages/Shortlist.py")
