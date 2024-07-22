import streamlit as st
import pandas as pd

# Initialisierung von table1 im Session State mit Daten aus ranking_table
if 'ranking_table' in st.session_state:
    st.session_state.table1 = st.session_state['ranking_table']
else:
    st.error("No ranking table found in session state")
    

if 'table2' not in st.session_state:
    st.session_state.table2 = []  # table2 wird bereits leer initialisiert


def move_items(source, target, items):
    for item in items:
        source.remove(item)
        target.append(item)

st.title("Move Items Between Tables")

# Display table 1 with checkboxes
st.write("Table 1")
selected_table1 = []
for item in st.session_state.table1:
    if st.checkbox(item, key=f"table1_{item}"):
        selected_table1.append(item)
        
# Display table 2 with checkboxes
st.write("Table 2")
selected_table2 = []
for item in st.session_state.table2:
    if st.checkbox(item, key=f"table2_{item}"):
        selected_table2.append(item)

# Buttons to move items
if st.button(">>"):
    if selected_table1:
        move_items(st.session_state.table1, st.session_state.table2, selected_table1)
        st.experimental_rerun()

if st.button("<<"):
    if selected_table2:
        move_items(st.session_state.table2, st.session_state.table1, selected_table2)
        st.experimental_rerun()
