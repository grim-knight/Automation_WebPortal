from fileinput import filename
from flask import Blueprint, render_template
import pandas as pd
import subprocess

dashboard_bp = Blueprint('dashboard', __name__)

class Dashboard:
    def __init__(self, filename, alias, encoding='utf-8'):
        self.filename = filename
        self.alias = alias


    def update_csv_and_dashboards():
        global dashboards
        dashboards = [
            Dashboard('Stage.csv', 'Stage', encoding='UTF-16'),
            Dashboard('Prod.csv', 'Prod', encoding='UTF-16'),
            Dashboard('Infra.csv', 'Infra', encoding='UTF-16')
        ]

    # Run PowerShell script
    def run_powershell_script(update_status):
        try:
            subprocess.run(["powershell", "C:\\installer\\wsuscmd.ps1", update_status])
        except subprocess.CalledProcessError as e:
            print(f'Error {e}')

    @dashboard_bp.route('/get_csv/<filename>')
    def get_csv(self,filename):
        try:
            dashboard = next(dashboard for dashboard in dashboards if dashboard.filename == filename)
            selected_data = dashboard.data.to_html(index=False)
            return selected_data
        except StopIteration:
            return "Invalid filename"


    @dashboard_bp.route('/update_dashboards', methods=['POST'])
    def update_dashboards(self):
        try:
            # Add logic to update CSV files or trigger the process that updates them
            update_csv_and_dashboards()
            return jsonify({'message': 'Dashboards updated successfully'})
        except Exception as e:
            return jsonify({'message': f'Failed to update dashboards: {str(e)}'}), 500

