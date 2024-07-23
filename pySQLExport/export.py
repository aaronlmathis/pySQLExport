import csv
import json
from pySQLExport.utils import print_colored

class Export:
    def __init__(self, results, outfile,  columns=None):
        self.results = results
        self.outfile = outfile
        self.columns = columns

    def export(self, output_type):
        if output_type == 'csv':
            self.export_to_csv()
        elif output_type == 'json':
            self.export_to_json()            
        else:
            raise ValueError(f"Unsupported output type: {output_type}")
        
    def export_to_csv(self):
        try:
            with open(self.outfile, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if self.columns:
                    writer.writerow(self.columns)  # Write column headers
                writer.writerows(self.results)
            print_colored(f"Results have been exported to {self.outfile} ({len(self.results)} rows) ", "green")
        except Exception as e:
            raise RuntimeError(f"Failed to export to CSV: {e}")
        
    def export_to_json(self):
        try:
            data = [dict(zip(self.columns, row)) for row in self.results]
            with open(self.outfile, 'w') as jsonfile:
                json.dump(data, jsonfile, indent=4)
            print_colored(f"Results have been exported to {self.outfile} ({len(self.results)} rows) ", "green")
        except Exception as e:
            raise RuntimeError(f"Failed to export to JSON: {e}")
