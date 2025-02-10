from __init__ import CURSOR, CONN
from area import Area
from route import Route

class Stage:

    all = {}

    def __init__(self, name, area_id, route_id, id=None):
        self.name = name
        self.area_id = area_id
        self.route_id = route_id
        self.id = id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string.")
        
    @property
    def area_id(self):
        return self._area_id
    
    @area_id.setter
    def area_id(self, area_id):
        if isinstance(area_id, int):
            self._area_id = area_id
        else:
            raise ValueError("Area ID must be an integer.")
    
    @property
    def route_id(self):
        return self._route_id
    
    @route_id.setter
    def route_id(self, route_id):
        if isinstance(route_id, int):
            self._route_id = route_id
        else:
            raise ValueError("Route ID must be an integer.")

    @classmethod
    def create_table():
        """ Create a new table to persist attributes of Stage instances. """
        sql = """
            CREATE TABLE IF NOT EXISTS stages (
            id INTEGER PRIMARY KEY,
            name TEXT,
            area_id INTEGER,
            route_id INTEGER,
            FOREIGN KEY (area_id) REFERENCES areas(id),
            FOREIGN KEY (route_id) REFERENCES routes(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def create(cls, name, area_id, route_id):
        """ Initialize a new Stage instance and save the object to the database.
        Save the object into local dictionary using the primary key as the dictionary key."""
        stage = cls(name, area_id, route_id)
        sql = """
            INSERT INTO stages (name, area_id, route_id)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (stage.name, stage.area_id, stage.route_id))
        CONN.commit()

        stage.id = CURSOR.lastrowid
        type(stage).all[stage.id] = stage

        return stage
    

    def delete(self):
        """ Delete the table row corresponding to the current Stage instance. """
        sql = """
            DELETE FROM stages
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None


    @classmethod
    def instance_from_db(cls, row):
        """ Return a Stage object having the attribute values from the corresponding table row. """
        stage = cls.all.get(row[0])
        
        if stage:
            stage.name = row[1]
            stage.area_id = row[2]
            stage.route_id = row[3]
        else:
            stage = cls(row[1], row[2], row[3])
            stage.id = row[0]
            cls.all[stage.id] = stage

        return stage
    

    @classmethod
    def find_by_id(cls, id):
        """ Return a Stage object corresponding to the table row with the specified primary key. """
        sql = """
            SELECT *
            FROM stages
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    