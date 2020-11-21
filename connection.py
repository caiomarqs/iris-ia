import pyodbc

# Conexão com o Banco de Dados na Azure
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Server=tcp:irisdb.database.windows.net;'
                      'Database=irisdb;'
                      'UID=iris;'
                      'PWD=sql2020@;')

cursor = conn.cursor()

# Lista todos os cliente
def list_all_users():
    return  cursor.execute("SELECT UserId, Name FROM dbo.Users").fetchall()

# Obtém nome do cliente por ID
def get_user_by_id(user_id):
    cursor.execute("SELECT UserId, Name FROM dbo.Users WHERE UserId=?", user_id)
    row = cursor.fetchone()
    if row:
        return row.Name

# Obtém imagem do cliente por ID
def get_image_by_id(user_id):
    cursor.execute("SELECT UserId, PhotoBase64Location FROM dbo.Users WHERE UserId=?", user_id)
    row = cursor.fetchone()
    if row:
        return row.PhotoBase64Location
