import streamlit as st
import pandas as pd
import mysql.connector
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

# Verbindung zur MySQL-Datenbank herstellen
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )

# Funktion zum Speichern der Stakeholder-Daten in MySQL
def save_stakeholder_data_to_mysql(data):
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS stakeholder ("
                   "id INT AUTO_INCREMENT PRIMARY KEY,"
                   "gruppe VARCHAR(255),"
                   "bestehende_beziehung VARCHAR(255),"
                   "auswirkung VARCHAR(255),"
                   "engagements_level VARCHAR(255),"
                   "stakeholdergruppe VARCHAR(255),"
                   "kommunikation VARCHAR(255),"
                   "betroffenheit VARCHAR(255),"
                   "zeithorizont VARCHAR(255)"
                   ")")
    for index, row in data.iterrows():
        cursor.execute("INSERT INTO stakeholder (gruppe, bestehende_beziehung, auswirkung, engagements_level, stakeholdergruppe, kommunikation, betroffenheit, zeithorizont) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (row['Gruppe'], row['Bestehende Beziehung'], row['Auswirkung auf Interessen'],
                        row['Level des Engagements'], row['Stakeholdergruppe'], row['Kommunikation'],
                        row['Art der Betroffenheit'], row['Zeithorizont']))
    connection.commit()
    connection.close()

# Funktion zum Abrufen der Stakeholder-Daten aus MySQL
def load_stakeholder_data_from_mysql():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stakeholder")
    data = cursor.fetchall()
    connection.close()
    columns = ["Gruppe", "Bestehende Beziehung", "Auswirkung auf Interessen",
               "Level des Engagements", "Stakeholdergruppe", "Kommunikation",
               "Art der Betroffenheit", "Zeithorizont"]
    return pd.DataFrame(data, columns=columns)

# Funktion zum Anzeigen der Stakeholder-Tabelle
def display_stakeholder_table():
    st.header("Stakeholder Tabelle")
    stakeholder_data = load_stakeholder_data_from_mysql()
    if not stakeholder_data.empty:
        st.write(stakeholder_data)
    else:
        st.write("Keine Stakeholder-Daten vorhanden.")

# Streamlit-Anwendung definieren
def main():
    st.title("Stakeholder Management")

    display_stakeholder_table()

    # Stakeholder-Daten erfassen
    st.header("Neue Stakeholder hinzufügen")
    # Implementiere die Funktion zum Hinzufügen neuer Stakeholder hier

# Führe die Streamlit-Anwendung aus
if __name__ == "__main__":
    main()
