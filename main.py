import tkinter
import socket
import time
import mysql.connector

from tkinter import ttk
   
"""This functions is called after button is pushed"""
def button_action(top, name, title, message, mtime):
    top.destroy()
    try:
        connection = mysql.connector.connect(host='',
                                            database='',
                                            user='',
                                            password='')

        print("Connection with database has been established")
        h_name = socket.gethostname()                    
        sql_update_Query = ("UPDATE log SET %s = '0' WHERE time = '%s'" % (h_name, mtime))
        cursor = connection.cursor()
        cursor.execute(sql_update_Query)
        connection.commit()
        name = ""
        title = ""
        message = ""
        mtime = ""
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    try:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection has been closed")
    except:
        print("Connection variable has not been declared")

       
"""This function handles GUI"""
def gui_operator(name, title, message, mtime):
    top = tkinter.Tk()
    
    WIN_WIDTH = top.winfo_screenwidth() 
    WIN_HEIGHT = top.winfo_screenheight()  

    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=4)
    top.columnconfigure(2, weight=1)

    top.rowconfigure(0, weight=1)
    top.rowconfigure(1, weight=1)
    top.rowconfigure(2, weight=8)
    top.rowconfigure(3, weight=2)

    top.geometry("%dx%d"%(WIN_WIDTH, WIN_HEIGHT))
    top.overrideredirect(True)

    name_box = tkinter.Message(top, text = name, relief='raised', bd = 0, font = "Impact 18", width = 1024)
    name_box.grid(row = 0, column = 1, sticky = tkinter.N)

    message_date = tkinter.Message(top, text = "Czas wysłania: " + mtime, bd = 0, font = "Impact 18", width = 512)
    message_date.grid(row = 0, column = 1, sticky = tkinter.NE)
    
    title_box = tkinter.Message(top, text = title, relief = 'raised', bd = 0, font = "Impact 18", width = 1024)
    title_box.grid(row = 1, column = 1, sticky = tkinter.S)
    
    message_box = tkinter.Message(top, text = message, relief = 'raised', bd = 0,  font = "Arial 12", width = 2048)
    message_box.grid(row = 2, column = 1, sticky = tkinter.N)

    confirm_button = tkinter.Button(top, text = "OK", width = 30, height = 6, bg = "light blue", command = lambda: button_action(top, name, title, message, mtime))
    confirm_button.grid(row = 3, column = 1, sticky = tkinter.S)

    top.wm_attributes("-topmost", 1)
    top.mainloop()

def main():
                                       
    """This loop is establishing connection with database every 30 seconds and listens for a message"""
    while True:
        name = ""
        title = ""
        message = ""
        h_name = socket.gethostname() 

        try:   
            connection = mysql.connector.connect(host='',
                                                        database='',
                                                        user='',
                                                        password='') 
            print("Connection with database has been established")     
            sql_select_Query = ("select * from log where %s = '1' LIMIT 1" % (h_name))
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)
            """Copies data to specific variabales"""
            for row in records:
                name = row[1]
                title = row[2]
                message = row[3]
                mtime = row[4]  

        except mysql.connector.Error as e:
            print("Error reading data from MySQL table: ", e)
        """Closes connection with a database after data has been copied to local variables and initiates GUI"""
        try:
            if connection.is_connected() and message != "":
                connection.close()
                cursor.close()
                print("MySQL connection has been closed")
                gui_operator(name, title, message, mtime)
        except:
            print("Connection variable has not been declared")

        time.sleep(10)

if __name__ == "__main__":
    main()
