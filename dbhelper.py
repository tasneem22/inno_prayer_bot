import sqlite3


class DBHelper:
    def __init__(self, dbname="userid.sqlite"):
        self.dbname = dbname
        sqlite3.connect(":memory:", check_same_thread=False)
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS userids (userid text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_id(self, userid):
        stmt = "INSERT INTO userids (userid) VALUES (?)"
        args = (userid, )

        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_id(self, userid):
        stmt = "DELETE FROM userids WHERE userid = (?)"
        args = (userid, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT userid FROM userids"
        return [x[0] for x in self.conn.execute(stmt)]