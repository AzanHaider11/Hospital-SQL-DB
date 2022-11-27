import cx_Oracle
from tkinter import *
from tkinter import ttk

def mainMenu(items = []):
    if items:
        for x in items: x.destroy()
    clearFrame()
    ttk.Label(frame, text="Hospital SQL Database", font=(FONT, 35)).grid(column=1, row=0)
    ttk.Button(frame, text='Create Tables', command=createTable).grid(column=1, row=2)
    ttk.Button(frame, text='Delete Tables', command=deleteTable).grid(column=1, row=3)
    ttk.Button(frame, text='Populate Tables', command=popTable).grid(column=1, row=4)
    ttk.Button(frame, text='Query Tables', command=startQuery).grid(column=1, row=5)
    ttk.Button(frame, text='View Tables', command=startView).grid(column=1, row=6)
    ttk.Button(frame, text='Quit', command=root.destroy).grid(column=1, row=7)

def clearFrame():
    for widget in frame.winfo_children():
       widget.destroy()
    frame.pack_forget()  

def getQuery(inputBox):
    query = inputBox.get()
    results = ''
    cursor.execute(query)
    for row in cursor:
        results += str(row) + '\n'
    ttk.Label(frame, text="Results:", font=(FONT, 12)).grid(column=0, row=10)
    ttk.Label(frame, text=results, font=(FONT, 12)).grid(column=0, row=12)
    inputBox.destroy()


def createTable():
    clearFrame()
    with open('createtable', 'r') as create_table:
        string = create_table.readlines()
    makeTable = ''
    for line in string:
        makeTable += line
        ttk.Label(frame, text="Making Tables...", font=(FONT, 18)).grid(column=0, row=0)
        if '$' in line:
            print(f"making table: {makeTable}")
            cursor.execute(makeTable[:-3])
            makeTable = ''
    
    ttk.Label(frame, text="Tables Created", font=(FONT, 18)).grid(column=0, row=5)
    ttk.Button(frame, text='Back', command=mainMenu).grid(column=0, row=10)

def deleteTable():
    clearFrame()
    with open('droptable', 'r') as drop_tables:
        string = drop_tables.readlines()
    for j,lines in enumerate(string):
        cursor.execute(lines)
        ttk.Label(frame, text=f"Dropping: {lines[10:]} Table", font=(FONT, 18)).grid(column=0, row=j)
    ttk.Button(frame, text='Back', command=mainMenu).grid(column=0, row=15)
   
def popTable():
    clearFrame()
    ttk.Button(frame, text='Back', command=mainMenu).grid(column=0, row=0)
    with open('populate', 'r') as populate:
        string = populate.readlines()
    for j,lines in enumerate(string):
        print(lines)
        cursor.execute(lines)
        ttk.Label(frame, text=f"Populating Tables...", font=(FONT, 10)).grid(column=0, row=j+1)

def startQuery():
    clearFrame()
    ttk.Label(frame, text="Enter a Query", font=(FONT, 18)).grid(column=0, row=0)
    inputBox = ttk.Entry(root, width = 50)
    inputBox.grid(column=0, row=1)
    ttk.Button(frame, text="Submit", command=lambda: getQuery(inputBox)).grid(column=0, row=2)
    ttk.Button(frame, text="Back", command=mainMenu).grid(column=0, row=3)
    
def startView():
    clearFrame()
    ttk.Button(frame, text='Patient Table', command=lambda: show('patient')).grid(column=1, row=2)
    ttk.Button(frame, text='Employee Table', command=lambda: show('employees')).grid(column=1, row=3)
    ttk.Button(frame, text='Appointment Tables', command=lambda: show('appointments')).grid(column=1, row=4)
    ttk.Button(frame, text='Medical History Tables', command=lambda: show('medical_history')).grid(column=1, row=5)
    ttk.Button(frame, text='Schedule Tables', command=lambda: show('schedule')).grid(column=1, row=6)
    ttk.Button(frame, text='Training Tables', command=lambda: show('appointments')).grid(column=1, row=7)
    ttk.Button(frame, text='Medical Bill Tables', command=lambda: show('departments')).grid(column=1, row=8)
    ttk.Button(frame, text='Priority Patients Tables', command=lambda: show('priority_patients')).grid(column=1, row=9)
    ttk.Button(frame, text='Bill Tables', command=lambda: show('bill')).grid(column=1, row=10)
    ttk.Button(frame, text='Bill ID Tables', command=lambda: show('billID')).grid(column=1, row=11)
    ttk.Button(frame, text='Certifications Tables', command=lambda: show('certifications')).grid(column=1, row=12)

    ttk.Button(frame, text='Back', command=mainMenu).grid(column=1, row=14)

def show(table):
    clearFrame()
    items = []
    ttk.Button(frame, text='Back', command=lambda: mainMenu(items)).grid(column=0, row=0)
    cursor.execute(f'SELECT * FROM {table}')
    for x,cols in enumerate(cursor):
        for y, rows in enumerate(cols):
            e = ttk.Entry(root)
            e.grid(row=x+5, column=y)
            e.insert(END, rows)
            items.append(e)

FONT = "Helvetica"

cx_Oracle.init_oracle_client(lib_dir="instantclient_19_17")

login = "user/pass"
connection_string = "@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(Host=oracle.scs.ryerson.ca)(Port=1521))(CONNECT_DATA=(SID=orcl)))"
connection_string = login + connection_string
conn = cx_Oracle.connect(connection_string)

root = Tk()
frame = ttk.Frame(root, padding=10)

cursor = conn.cursor()



while True:
    frame.grid()
    mainMenu()

    root.mainloop()
    cursor.close()
    conn.close()
    


