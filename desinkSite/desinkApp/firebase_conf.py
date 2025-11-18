import firebase_admin
from firebase_admin import credentials, firestore, auth, storage

# Inicializar Firebase app
cred = credentials.Certificate("C:\Users\Franco\Documents\proyecto titulo")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://proyecto-de-titulo-fb092-default-rtdb.firebaseio.com/'
})

db = firestore.client()
bucket = storage.bucket()