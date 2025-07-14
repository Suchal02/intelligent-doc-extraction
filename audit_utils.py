import csv
from datetime import datetime

def log_audit(file_name, fields, correction=None):
    with open("outputs/audit_log.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), file_name, fields, correction])
