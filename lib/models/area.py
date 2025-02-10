from . import CURSOR, CONN

class Area:

    all = {}

    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")


    @classmethod
    def create_table(cls):
        """ Create a new table to persist attributes of Area instances. """
        sql = """
            CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY,
            name TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def create(cls, name):
        """ Initialize a new Area instance and save the object to the database.
        Save the object into local dictionary using the primary key as the dictionary key. """
        area = cls(name)
        sql = """
            INSERT INTO areas (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (area.name,))
        CONN.commit()
        area.id = CURSOR.lastrowid
        type(area).all[area.id] = area

        return area
    

    def delete(self):
        """ Delete the table row corresponding to the current Area instance. """
        sql = """
            DELETE FROM areas
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None
    

    @classmethod
    def instance_from_db(cls, row):
        """ Return an Area object having the attributes from the corresponding table row. """
        area = cls.all.get(row[0])

        if area:
            area.name = row[1]
        else:
            area = cls(row[1])
            area.id = row[0]
            cls.all[area.id] = area

        return area
    

    @classmethod
    def find_by_id(cls, id):
        """ Return an Area object corresponding to the table row with the specified primary key. """
        sql = """
            SELECT *
            FROM areas
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    

    @classmethod
    def get_all(cls):
        """ Return a list containing an Area object per row in the table. """
        sql = """
            SELECT *
            FROM areas
        """
        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    

    def stages(self):
        """ Return a list of Stages associated with current Area instance. """
        from stage import Stage
        sql = """
            SELECT *
            FROM stages
            WHERE area_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [
            Stage.instance_from_db(row) for row in rows
        ]