import abc
from database import Database
import sqlite3

class SQLite(Database):
    _db = None

    def create_database(self, database_path):
        """ Create the database and the table inside.
            Preconditions:
                database_path - The path to the database
            Postconditions:
                True if succeeds, else False.
                Database remains open if successful."""
        conn   = sqlite3.connect(database_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''CREATE TABLE todo
                (id INTEGER PRIMARY KEY, creation_date DATE, 
                completion_date DATE, entry TEXT, priority TEXT,
                completed TEXT)''')
        except sqlite3.Error, e:
            print "An error occurred: ", e.args[0]
            conn.close()

            return False

        self._db = conn

        return True

    def open_database(self, path):
        """ Open the database.
            Preconditions:
                Path - path to the database.
            Postconditions:
                If _db != None then return False,
                else open database and return True"""
        if self._db != None:
            print "A database is already open."
            return False

        self._db = sqlite3.connect(path)
        
        return True

    def close_database(self):
        """ Close the database"""
        self._db.close()
        self._db = None

        return True

    def add_entry(self, comp_date, entry, priority):
        """ Add an entry into the database.
            Preconditions:
                comp_date - Date to be completed (YYYY-MM-DD HH:MM)
                entry     = The goal
                priority  - Priority of the entry"""
        if self._db != None:
            cur = self._db.cursor()

            ident = None
            statement = '''INSERT INTO todo (id, creation_date,
                        completion_date, entry, priority, completed)
                        VALUES (''' + ident + ''', datetime(\'now\'),
                        ''' + comp_date + ''', ''' + entry + ''',
                        ''' + priority + ''', \')'''
            try:
                cur.execute(statement) 

            except sqlite3.Error, e:
                print "An error was encountered: ", e.args[0]
                return False
        
        return True 

    def edit_completion_date(self, ident, new_comp_date):
        raise NotImplementedError

    def edit_entry(self, ident, new_entry):
        raise NotImplementedError

    def edit_priority(self, ident, new_priority):
        raise NotImplementedError

    def delete_entry(self, ident):
        raise NotImplementedError

    def purge(self):
        if self._db == None:
            return False

        cur       = self._db.cursor()
        statement = "DELETE FROM todo"

        try:
            cur.execute(statement)
            self._db.commit()
        except sqlite3.Error, e:
            print "An error was encountered: ", e.args[0]
            return False

        return True

if __name__ == '__main__':
    print 'Subclass:', issubclass(SQLite, Database)
    print 'Instance:', isinstance(SQLite(), Database)
