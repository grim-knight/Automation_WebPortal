from flask import Flask, render_template, request, jsonify
import pandas as pd
import subprocess
import os
 
app = Flask(__name__)
 
class Dashboard:
    def __init__(self, filename, alias, encoding='utf-8'):
        self.filename = filename
        self.alias = alias
        self.data = pd.read_csv(filename, encoding=encoding)
 
# Run PowerShell script
def run_powershell_script(update_status):
    try:
        subprocess.run(["powershell", "C:\\installer\\wsuscmd.ps1", update_status])
    except subprocess.CalledProcessError as e:
        print(f'Error {e}')
 
# Update CSV files and dashboards
def update_csv_and_dashboards():
    global dashboards
    # Dashboard files and aliases
    dashboards = [
            Dashboard('Book1.csv', 'Stage', encoding='UTF-8'),
            Dashboard('Book2.csv', 'Prod', encoding='UTF-8'),
            Dashboard('temp.csv', 'Infra', encoding='UTF-16')
    ]
    
    return dashboards
 
# Initial run to populate dashboards
dashboards = update_csv_and_dashboards()
 
@app.route('/')
def index():
    print(dashboards)
    return render_template('dashboard.html', dashboards=dashboards)
 
@app.route('/get_csv/<filename>')
def get_csv(filename):
    try:
        dashboard = next(dashboard for dashboard in dashboards if dashboard.filename == filename)
        selected_data = dashboard.data.to_html(index=False)  # Exclude index from HTML
        return selected_data
    except StopIteration:
        return "Invalid filename"
 
@app.route('/update_script', methods=['POST'])
def update_script():
    update_status = request.form.get('updateStatus', 'Any')
    run_powershell_script(update_status)
    return "Update successful"
 
# Route to update dashboards after the script is executed
@app.route('/update_dashboards')
def update_dashboards():
    global dashboards
    dashboards = update_csv_and_dashboards()
    return render_template('dashboard_list.html', dashboards=dashboards)
 
if __name__ == '__main__':
    app.run(debug=True)