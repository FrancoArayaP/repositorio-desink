import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyATYekLCAB1shW9TlVdbQrjgyrE7PY-zdc",
  "authDomain": "proyecto-titulo-bcf7e.firebaseapp.com",
  "databaseURL": "https://proyecto-titulo-bcf7e-default-rtdb.firebaseio.com",
  "projectId": "proyecto-titulo-bcf7e",
  "storageBucket": "proyecto-titulo-bcf7e.firebasestorage.app",
  "messagingSenderId": "566825435290",
  "appId": "1:566825435290:web:a8f042d4d1b36c81331f23",
  "measurementId": "G-PYYYRX57L5"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
