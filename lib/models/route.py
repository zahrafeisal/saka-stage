from __init__ import CURSOR, CONN

class Route:

    all = {}

    def __init__(self, route, id=None):
        self.route = route
        self.id = id

    @property
    def route(self):
        return self._route
    
    @route.setter
    def route(self, route):
        if isinstance(route, str) and len(route):
            self._route = route
        else:
            raise ValueError("Route must be a non-empty string")


    @classmethod
    def create_table():
        """ Create a new table to persist attributes of Route instances. """
        sql = """
            CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY,
            route TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
    

    @classmethod
    def create(cls, route):
        """ Initialize a new Department instance and save the object to the database.
        Save the object into local dictionary using the primary key as the dictionary key. """
        route_instance = cls(route)
        sql = """
            INSERT INTO routes (route)
            VALUES (?)
        """
        CURSOR.execute(sql, (route_instance.route,))
        CONN.commit()
        route_instance.id = CURSOR.lastrowid
        type(route_instance).all[route_instance.id] = route_instance

        return route_instance
    

    def delete(self):
        """ Delete the table row corresponding to the current Route instance. """
        sql = """
            DELETE FROM routes
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None
    

    @classmethod
    def instance_from_db(cls, row):
        """ Return a Route object having the attribute values from the corresponding table row. """
        route_instance = cls.all.get(row[0])

        if route_instance:
            route_instance.route = row[1]
        else:
            route_instance = cls(row[1])
            route_instance.id = row[0]
            cls.all[route_instance.id] = route_instance
        
        return route_instance


    @classmethod
    def get_all(cls):
        """ Return a list containing a Route object per row in the table. """
        sql = """
            SELECT *
            FROM routes
        """
        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    

    @classmethod
    def find_by_id(cls, id):
        """ Return a Route object corresponding to the table row with the specified primary key. """
        sql = """
            SELECT *
            FROM routes
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    

    def stages(self):
        """ Return a list of Stages associated with current Route instance. """
        from stage import Stage
        sql = """
            SELECT *
            FROM stages
            WHERE route_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [
            Stage.instance_from_db(row) for row in rows
        ]