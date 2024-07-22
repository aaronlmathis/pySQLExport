import sys
import getpass
import os
from pySQLExport.cli import CLI
from pySQLExport.config import load_config
from pySQLExport.database import Database
from pySQLExport.query import Query
from pySQLExport.export import Export
from pySQLExport.utils import print_colored

class PySQLExport:
    def __init__(self):
        self.cli = CLI()
        self.args = self.cli.parse_args(sys.argv[1:])
        self.interactive = len(sys.argv) == 1
        self.config = {}
        self.password = None
        self.db = None
        self.results = None
        self.query = ''

    def load_config(self):
        if self.interactive:
            self.get_db_info()
        else: 
            if self.args.config_file and os.path.isfile(self.args.config_file):
                try:
                    self.config = load_config(self.args.config_file)
                except Exception as e:
                    print_colored(f"Failed to load config file: {e}", "red")
                    sys.exit(1)
            else:
                print_colored("Config file not found. Please provide the database information.", "yellow")
                self.get_db_info()

    def get_db_info(self):
        self.config['host'] = input("Enter database host: ")
        self.config['user'] = input("Enter database user: ")
        self.config['database'] = input("Enter database name: ")
        self.config['port'] = input("Enter database port (default 3306): ")
        self.config['port'] = int(self.config['port']) if  self.config['port'] else 3306


    def get_password(self):
        self.password = getpass.getpass(prompt='Enter database password: ')

    def connect_to_database(self):
        try:
            self.db = Database(
                self.config['host'], self.config['user'],
                self.password, self.config['database'], self.config['port']
            )
        except Exception as e:
            print_colored(f"Failed to connect to the database: {e}", "red")
            sys.exit(1)

    def execute_query(self):
        try:
            query = Query(self.db)
            self.results = query.execute(self.query)
        except Exception as e:
            print_colored(f"Failed to execute query: {e}", "red")
            sys.exit(1)

    def export_results(self):
        if self.args.output:
            if self.args.output not in ['csv']:
                print_colored("Invalid output type. Current options are CSV.", "red")
                sys.exit(1)
            if not self.args.outfile:
                print_colored("Please provide an output file path: ", "yellow", end='')
                self.args.outfile = input()
            try:
                exporter = Export(self.results, self.args.outfile)
                exporter.export(self.args.output)
                print_colored(f"Results have been exported to {self.args.outfile}", "green")
            except Exception as e:
                print_colored(f"Failed to export results: {e}", "red")
                sys.exit(1)
        else:
            for row in self.results:
                print(row)

    def interactive_menu(self):
        while True:
            print_colored("1. Run a query", 'cyan')
            print_colored("2. Export last query results", 'cyan')
            print_colored("3. Exit", 'cyan')
            choice = input("Choose an option: ").strip()
            if choice == '1':
                self.query = input("Enter SQL Query: ")
                self.execute_query()
                for row in self.results:
                    print(row)
            elif choice == '2':
                if self.results:
                    self.export_results()
                else:
                    print_colored("No results to export. Run a query first.", "yellow")
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print_colored("Invalid choice. Please try again.", "red")


    def run(self):
        try:
            self.load_config()
            self.get_password()
            self.connect_to_database()
            if self.interactive:
                self.interactive_menu()
            else:
                self.execute_query(self.args.query)
                self.export_results()
        except Exception as e:
            print_colored(f"An unexpected error occurred: {e}", "red")
            sys.exit(1)

def main():
    app = PySQLExport()
    app.run()

if __name__ == "__main__":
    main()
