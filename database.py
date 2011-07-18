import abc

class Database(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(self, database_name):
        """Create the database and set it up."""
        return

    @abc.abstractmethod
    def open(self, path):
        """Open the database."""
        return

    @abc.abstractmethod
    def close(self):
        """Close the database"""
        return

    @abc.abstractmethod
    def add(self, comp_date, entry, priority):
        """Create an entry in the database."""
        return

    @abc.abstractmethod
    def edit_completion_date(self, ident, new_comp_date):
        """Edit the completion date"""
        return

    @abc.abstractmethod
    def edit_entry(self, ident, new_entry):
        """Edit the entry"""
        return

    @abc.abstractmethod
    def edit_priority(self, ident, new_priority):
        """Edit the priority"""
        return

    @abc.abstractmethod
    def delete(self, ident):
        """Delete the entry"""
        return

    @abc.abstractmethod
    def purge(self):
        """Purge all entries from the database."""
        return

if __name__ == "__main__":
    print "Abstract class"
