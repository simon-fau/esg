
import webview
import subprocess
import threading

def start_streamlit():
    subprocess.run(["streamlit", "run", "main.py"])

if __name__ == '__main__':
    threading.Thread(target=start_streamlit).start()
    webview.create_window("Streamlit Desktop App", "http://localhost:8501")
    webview.start()
