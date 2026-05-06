import psycopg2 as psy
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

conexion = psy.connect(
    database = "Biblioteca",
    host = "localhost",
    port = 5432,
    user = "postgres",
    password = "12345"

)

cursor = conexion.cursor()

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("BiblioAlegria")
        relf.resize(300,200)

app = QtWidgets.QApplication([])
ventana = uic.loadUi(r'C:\Users\eric_\Desktop\BD_PROYECTO\AV1\6.ui')


def login():
    usuario = ventana.input_user.text()
    password = ventana.input_pass.text()

    consulta = 'SELECT * FROM "Usuario" WHERE nombre_del_usuario = %s AND contrasena = %s'
    cursor.execute(consulta, (usuario, password))

    resultado = cursor.fetchone()

    if resultado:
        print("Login correcto")
    else:
        print("Usuario o contraseña incorrectos")


ventana.btn_login.clicked.connect(login)

ventana.show()
app.exec()

cursor.close()
conexion.close()




