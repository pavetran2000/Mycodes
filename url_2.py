import pyshorteners
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('sample.db') # Open a database File

# Create a cursor object to interact with the database
cursor = conn.cursor()

class Tinyurl():

    def create_tiny_url(self,long_url):
        s = pyshorteners.Shortener()
        create_tiny_url = s.tinyurl.short(long_url)
        return create_tiny_url

    def get_long_url(self,tiny_url):
        s = pyshorteners.Shortener()
        get_long_url = s.tinyurl.expand(tiny_url)
        return get_long_url

    def create_url_table(self,Id,long_url,tiny_url):
        conn.execute(''' INSERT INTO Urls(Id,long_url,tiny_url)
            VALUES(?,?,?)''',(Id,long_url,tiny_url))
        conn.commit()
        print('Record inserted')
    
    def delete_tiny_url(self,del_Upd_Id):
        # Check if the URL exists in the database
        cursor.execute(''' SELECT * FROM Urls WHERE Id = ?''', (del_Upd_Id,))
        row = cursor.fetchone()
        if row:
            conn.execute(''' DELETE FROM Urls WHERE Id = ?''',(del_Upd_Id,))
            conn.commit()
            print("Tiny URL deleted for Id: ", del_Upd_Id)
            return True
        else:
            print("No URL found")
            return False

    def update_long_url(self, Upd_Id, updated_url):
        cursor = conn.cursor()
        # Check if the URL exists in the database
        cursor.execute('''SELECT * FROM Urls WHERE Id = ?''', (Upd_Id,))
        row = cursor.fetchone()
        if row:
        # URL found, update the long_url column
            conn.execute('''UPDATE Urls SET long_url = ? WHERE Id = ?''', (updated_url, Upd_Id))
            conn.commit()
            print("URL updated for ID", Upd_Id)
            return True
        else:
        # URL not found in the database
            print("No URL found")
            return False

url=input("Enter the URL: ")
Id=input("Enter the Value for ID: ")
obj=Tinyurl()
tiny_url=obj.create_tiny_url(url)
print(tiny_url)
long_url=obj.get_long_url(tiny_url)
print(long_url)
obj.create_url_table(Id,long_url,tiny_url)

# Ask for the updated URL and ID for update operation
updated_url=input('Updated URL: ')
Upd_Id=input('Need to update in which Id: ')

# Perform delete operation based on Upd_Id
del_Upd_Id=input('Url to be deleted: ')
del_tiny_url=obj.delete_tiny_url(del_Upd_Id)

# Perform update operation based on Upd_Id and updated URL
Url=obj.update_long_url(Upd_Id, updated_url)

