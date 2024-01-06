from LibDB import LibDB
from GUI import LibraryGuiTk

def main():
    db = LibDB(init=False, dbName='Library')
    app = LibraryGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()