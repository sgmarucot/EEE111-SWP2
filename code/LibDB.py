
import csv
import json
from LibDBEntry import LibDbEntries

class LibDB:
    def __init__(self, init=False, dbName='Library'):       
        self.dbName = dbName
        self.entry = []

    def fetch_entry(self):
        return self.entry

    def insert_entry(self, id, Title, Author, Genre, status):
        newEntry = LibDbEntries(id=id, Title=Title, Author=Author, Genre=Genre, status=status)
        self.entry.append((newEntry.id, newEntry.Title, newEntry.Author, newEntry.Genre, newEntry.status))

    def delete_entry(self, id):
        for entry in self.entry:
            if entry[0] == id:
                self.entry.remove(entry)
                return

    def update_entry(self, new_Title, new_Author, new_Genre, new_status, id):
        for i, entry in enumerate(self.entry):
            if entry[0] == id:
                new = (entry[0], new_Title, new_Author, new_Genre, new_status)
                self.entry[i] = new
                return

    def export_csv(self):
        csv_file_name = f"{self.dbName}.csv"
        with open(csv_file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(self.entry)

    def id_exists(self, id):
        for entry in self.entry:
            if entry[0] == id:
                return True
        return False
    
    def export_json(self, json_file_name='library_data.json'):
        data_to_export = {'books': self.entry}
        with open(json_file_name, 'w') as json_file:
            json.dump(data_to_export, json_file, indent=4)
        
    def process_csv(self, file_path):
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader) 
            data = [row for row in csv_reader]
            print("Header:", header)
            print("Data:", data)
