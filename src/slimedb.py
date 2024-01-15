
#!/usr/bin/env python3

#=========================================================
# Slime
# SlimeDB  
# Actions for loading/querying with the SlimeDB
#=========================================================

import sqlite3

"""

SlimeDB

+-------------------+       		  
|       Slime       |        
+-------------------+       	 
| Slime ID (PK)     |               
| Version           |             
| Name              |              
| Color             | 		  
| Template          |        
| AuthslimeImage    |	    
+-------------------+      
        		     
         ^		     
         |
+-------------------+  
|    Accessories    |
+-------------------+  
| SlimeID (FK)      | 
| AccessoryName     |
+-------------------+ 

"""

#------------------Read------------------#

def check_tables():
	slimedb_connection = sqlite3.connect("slime.db")
	cursor = slimedb_connection.cursor()
	tablecheck = cursor.execute("SELECT name FROM sqlite_master").fetchall()
	
	if tablecheck == []:
		found = False
	else:
		found = True

	return found

def read_all_slime():
	slimedb_connection = sqlite3.connect("slime.db")
	cursor = slimedb_connection.cursor()

	cursor.execute("SELECT * FROM Slime")

	slimes = cursor.fetchall()

	# Print the column names
	columns = [description[0] for description in cursor.description]
	print("|".join(columns))

	# Print a separator line
	print("-" * (len("|".join(columns)) + len(columns) - 1))

	# Print each row
	for slime in slimes:
		print("|".join(map(str, slime)))

	slimedb_connection.close()


#------------------Write------------------#

def create_tables():

	slimedb_connection = sqlite3.connect("slime.db")
	cursor = slimedb_connection.cursor()
	
	#Create Slime Table
	cursor.execute('''
	CREATE TABLE Slime (
        SlimeID TEXT PRIMARY KEY,
        Version INTEGER,
        Name TEXT,
        Color TEXT,
        Template INTEGER,
        SlimeImage BLOB
        )
		''')

	#Create Accessories Table
	cursor.execute('''
    CREATE TABLE Accessories (
        SlimeID TEXT,
        AccessoryName TEXT,
        FOREIGN KEY (SlimeID) REFERENCES Slime(SlimeID)
    	)
	''')

	slimedb_connection.commit()
	slimedb_connection.close()


def insert_into_slime_table(slime_list,no_db_images):
	slimedb_connection = sqlite3.connect("slime.db")
	cursor = slimedb_connection.cursor()

	#Remove the image from the database if no_db_images is passed
	if no_db_images == True:
		del slime_list[5]
		cursor.execute('''
	    INSERT INTO Slime (SlimeID, Version, Name, Color, Template)
	    VALUES (?, ?, ?, ?, ?)
		''', slime_list)
	
	else:
		cursor.execute('''
	    INSERT INTO Slime (SlimeID, Version, Name, Color, Template, SlimeImage)
	    VALUES (?, ?, ?, ?, ?, ?)
		''', slime_list)
		
	slimedb_connection.commit()
	slimedb_connection.close()


def insert_into_accessories_table(accessory_list):
	slimedb_connection = sqlite3.connect("slime.db")
	cursor = slimedb_connection.cursor()

	cursor.execute('''
	INSERT INTO Accessories (SlimeID, AccessoryName)
	VALUES (?, ?)
		''',accessory_list)

	slimedb_connection.commit()
	slimedb_connection.close()