import abc
from database import Database
import sqlite3

class SQLite(Database):
    _db = None

    def create(self, database_path):
        """ Create the database and the table inside.
            Preconditions:
                database_path - The path to the database
            Postconditions:
                True if succeeds, else False.
                _db points to the database."""
        
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

    def open(self, path):
        """ Open the database.
            Preconditions:
                Path - path to the database.
            Postconditions:
                If _db != None then return False,
                else open database and return True."""
        
        if self._db != None:
            print "A database is already open."
            return False

        self._db = sqlite3.connect(path)
        
        return True

    def close(self):
        """ Close the database.
            Postconditions:
                Database is closed.
                _db set to None."""
        
        self._db.close()
        self._db = None

        return True

    def add(self, comp_date, entry, priority):
        """ Add an entry into the database.
            Preconditions:
                comp_date - Date to be completed (YYYY-MM-DD HH:MM)
                entry     = The goal
                priority  - Priority of the entry
            Postconditions:
                Returns True if successful, else False."""
        
        if self._db != None:
            cur = self._db.cursor()

            cur.execute('''SELECT id FROM todo ORDER BY rowid 
                        DESC LIMIT 1;''')
            
            lastrowid = cur.fetchone()
            ident     = int(lastrowid[0]) + 1 
            statement = '''INSERT INTO todo (id, creation_date,
                        completion_date, entry, priority, completed)
                        VALUES (''' + str(ident) + ''', datetime(\'now\'),
                        \"''' + comp_date + '''\",\"''' + entry + '''\",
                        \"''' + priority + '''\", "F");'''

            try:
                cur.execute(statement) 
                self._db.commit()
            except sqlite3.Error, e:
                print "An error was encountered: ", e.args[0]
                return False
        
        return True 

    def edit(self,statement):
        """ Edits the database given the sql query.
            Preconditions:
                statement - Str, sql query
            Postconditions:
                Returns True if successful, else False."""
        
        if self._db == None:
            return False

        cur = self._db.cursor()

        try:
            cur.execute(statement)
            self._db.commit()
        except sqlite3.Error, e:
            print "An error occured: ", e.args[0]
            return False

        return True
    
    def edit_completion_date(self, ident, new_comp_date):
        """ Edit completion date where id=ident
            Preconditions:
                ident           - Int, id of the row.
                new_comp_date   - Str
            Postconditions:
                Returns True if successful, else False."""
        
        statement = "UPDATE todo SET completion_date=\'" + new_comp_date
        + "\' WHERE id=" + str(ident)
        
        return edit(statement)

    def edit_entry(self, ident, new_entry):
        """ Edit entry where id=ident.
            Preconditions:
                ident     - Int, id of the row.
                new_entry - Str
            Postconditions:
                Return True if successful, else False"""
        
        statement = "UPDATE todo SET entry=\'" + new_entry
        + "\' WHERE id=" + str(ident)
        
        return edit(statement)

    def edit_priority(self, ident, new_priority):
        """ Edit priority of row with id=ident.
            Preconditions:
                ident        - Int, id of row
                new_priority - Str
            Postconditons:
                Return True is successful, else False"""
        
        statement = "UPDATE todo SET priority=\'" + new_priority
        + "\' WHERE id=" + str(ident)
        
        return edit(statement)

    def delete(self, ident):
        """ Delete a row where id=ident.
            Preconditions:
                ident - Int, id of the row.
            Postconditions:
                Returns True if successful, else False."""
        
        if self._db == None:
            return False

        cur       = self._db.cursor()
        statement = "DELETE FROM todo WHERE id=" + str(ident) 
        
        try:
            cur.execute(statement)

            statement = "UPDATE todo SET id=id-1 WHERE id >" + str(ident)
            cur.execute(statement)

            self._db.commit()
        except sqlite3.Error, e:
            print "An error was encountered ", e.args[0]
            return False

        return True
            
    def purge(self):
        """Purge all rows in the table."""
        
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
