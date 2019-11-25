"""
Database script for storing game data

"""
__author__ = "Joshua Akangah"

import sqlite3

class EnemyWaveDatabase():
    def __init__(self, wave=1):
        self.name = "database.db"
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        self.wave = wave
        self.currentType = 1
        try:
            self.cursor.execute("create table Waves(id integer, wave integer not null, currentType integer not null)")   
        except:
            # catching error to prevent termination
            pass
        finally:
            self.cursor.execute("select count(*) from Waves")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute(f"insert into Waves (id, wave, currentType) values (0, {self.wave}, {self.currentType})")
            self.connection.commit()
        self.connection.commit()
        self.connection.close()

    def updateWave(self, updateType=False):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            self.cursor.execute("select * from Waves where id=0")
            items = list(self.cursor.fetchall()[0][1:3])
            currentWave = items[0]
            currentType = items[1]
            if currentWave % 5 == 0:
                self.cursor.execute(f"update Waves set currentType={currentType+1} where id=0")
            self.cursor.execute(f"update Waves set wave={currentWave+1} where id=0")
            self.connection.commit()
            if updateType:# max type of enemies
                self.cursor.execute(f"update Waves set currentType={currentType+1} where id=0")
            if self.currentType > 18:
                self.cursor.execute(f"update Waves set currentType=1 where id=0")
            self.connection.commit()
        except sqlite3.OperationalError as error:
            return error
        finally:
            self.connection.close()

    def retrieveWave(self):
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("select * from Waves where id=0")
            return self.cursor.fetchall()[0][1:3]
            # first is current wave and second is type
        except sqlite3.OperationalError as error:
            return error
        finally:
            self.connection.close()

    def clearDatabase(self):
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("update Waves set wave=1 where id=0")
            self.connection.commit()
            self.cursor.execute("update Waves set currentType=1 where id=0")
            self.connection.commit()
        except sqlite3.OperationalError as error:
            return error
        finally:
            self.connection.close()

class PlayerDatabase():
    def __init__(self, newPlayer="True"):
        self.name = "database.db"
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("""
                create table PlayerDatabase(score integer,
                level integer, rockets integer,
                shield integer not null""")
            self.connection.commit()
            self.cursor.execute("""
                insert into PlayerDatabase (score, level, rockets, shield)
                values (0, 0, 0, 0)
            """)
            self.connection.commit()
        except:
            pass
        finally:
            self.connection.close()

    def getItem(self, item):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute("""
                select * from PlayerDatabase
            """)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as error:
            return error
    
    def updateItem(self, item, amount):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            
            if item == "score":
                self.cursor.execute(f"""
                    insert into PlayerDatabase (score) 
                    values ({amount})
                """)
                self.connection.commit()
            elif item == "level":
                self.cursor.execute(f"""
                    update PlayerDatabase set (level)
                    values ({amount})
                """)
        except:
            pass
