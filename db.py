# Module Imports
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="fs",
        password="fsociety1964",
        host="mariadb-21088-0.cloudclusters.net",
        port=21120,
        database="fsociety"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
conn.autocommit = False
cur = conn.cursor()

def addstep1(mass):
	cur.executemany("INSERT INTO rosreestr_step1 (cadastr,addr) VALUES (?, ?)", (mass))
	conn.commit()
	
def getallstep1():
	cur.execute("SELECT * FROM rosreestr_step1")
	rows = cur.fetchall()
	for i in rows:
		print(i)
		
