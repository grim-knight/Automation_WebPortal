# from flask import Flask, render_template, request
# from flask_socketio import SocketIO
# import pandas as pd
# import subprocess
# import os
# import logging
# from apscheduler.schedulers.background import BackgroundScheduler

# logging.basicConfig(level=logging.INFO)

# app = Flask(__name__)
# socketio = SocketIO(app)
# dashboards = []

# class Dashboard:
#     def __init__(self, filename, alias):
#         self.filename = filename
#         self.alias = alias
#         self.data = pd.read_csv(filename)

# def run_powershell_script(script_path, update_status):
#     try:
#         subprocess.run(["powershell", script_path, update_status], check=True)
#         logging.info('Script execution completed successfully')
#     except subprocess.CalledProcessError as e:
#         logging.error(f'Script execution failed with error: {e}')

# def update_csv_and_dashboards():
#     global dashboards

#     print("Updating dashboards...")
#     folders = [
#         os.path.join(os.getcwd(), 'dashboard', 'failed'),
#         os.path.join(os.getcwd(), 'dashboard', 'installed'),
#         os.path.join(os.getcwd(), 'dashboard', 'any')
#     ]

#     for folder in folders:
#         for root, dirs, files in os.walk(folder):
#             for file in files:
#                 if file.endswith('.csv'):
#                     filepath = os.path.join(root, file)
#                     alias = f"{os.path.basename(folder)} - {os.path.splitext(file)[0]}"
#                     dashboards.append(Dashboard(filepath, alias))

#     print("Updated dashboards:", dashboards)


# def update_data_and_emit():
#     update_csv_and_dashboards()
#     print("Updated dashboards:", dashboards)
#     socketio.emit('update', namespace='/update')

# # Schedule the job every 15 minutes
# scheduler = BackgroundScheduler()
# scheduler.add_job(update_data_and_emit, 'interval', minutes=15)
# scheduler.start()

# @app.route('/')
# def index():
#     print(f'Checking existence of data in {dashboards}')
#     return render_template('dash.html', dashboards=dashboards)

# @app.route('/get_csv/<path:filename>')
# def get_csv(filename):
#     try:
#         dashboard = next(dashboard for dashboard in dashboards if dashboard.filename == filename)
#         selected_data = dashboard.data.to_html(index=False)
#         return selected_data
#     except StopIteration:
#         return "Invalid filename"

# @app.route('/update_script', methods=['POST'])
# def update_script():
#     update_status = request.form.get('updateStatus', 'Any')
#     return "Update request received"

# if __name__ == '__main__':
#     socketio.run(app, debug=True, use_reloader=False)


import chardet

def detect_encoding(filename):
    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Usage
filename = 'temp.csv'
detected_encoding = detect_encoding(filename)
print(detected_encoding)
