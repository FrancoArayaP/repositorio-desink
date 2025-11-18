from django.shortcuts import render
import pyrebase

# Configuración de Firebase (Python dict, no const)
firebaseConfig = {
    "apiKey": "AIzaSyATYekLCAB1shW9TlVdbQrjgyrE7PY-zdc",
    "authDomain": "proyecto-titulo-bcf7e.firebaseapp.com",
    "projectId": "proyecto-titulo-bcf7e",
    "storageBucket": "proyecto-titulo-bcf7e.appspot.com",
    "messagingSenderId": "566825435290",
    "appId": "1:566825435290:web:a8f042d4d1b36c81331f23",
    "measurementId": "G-PYYYRX57L5",
    "databaseURL": ""  # si usas Realtime Database, agrega la URL aquí
}

# Inicializar Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()



def index(request):
    return render(request, 'index.html')
