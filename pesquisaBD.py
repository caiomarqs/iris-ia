from connection import list_all_users
from os import listdir

# Lendo o diretório de Images

users_directories = listdir('Images')
users_directories.sort(key = int)
users_database = list_all_users()

# Inicializando variável
users_analyse = []

# Adiciona os clientes cadastrados que tem sua foto no diretório Image
for UserId, Name in users_database:
    if str(UserId) in users_directories:
        users_analyse.append(Name)


# Printa os nomes dos clientes que tem sua foto no diretório Images
print(users_analyse)

# Printa o nome do diretório de cada cliente
print(users_directories)

# Printa todos os usuários cadastrados
print(users_database)