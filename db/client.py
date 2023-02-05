from pymongo import MongoClient

#Base de datos de manera local#
#client_db = MongoClient().local

#Base de datos de manera remota ( C/Atlas)
client_db = MongoClient("Inserta tu Url aqui de MondoDB Atlas").test


