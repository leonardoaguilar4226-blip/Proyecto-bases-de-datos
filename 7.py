import psycopg2 as psy
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtGui import QPixmap, QIcon, QCursor
import sys
import os

# 🔹 Conexión a la BD
try:
    conexion = psy.connect(
        database="Biblioteca",
        host="localhost",
        port=5432,
        user="postgres",
        password="1234"
    )
    cursor = conexion.cursor()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    # Si falla la conexión, mostramos un error y cerramos
    app = QApplication(sys.argv)
    QtWidgets.QMessageBox.critical(None, "Error de Conexión", 
        f"No se pudo conectar a la base de datos 'Biblioteca'.\n\nDetalle: {e}\n\nAsegúrate de que PostgreSQL esté iniciado y la base de datos exista.")
    sys.exit(1)

#VENTANA PRINCIPAL OSEA EL MAIN
class Main(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        import os
        base_path = os.path.dirname(__file__)
        uic.loadUi(os.path.join(base_path, 'AV1', 'main.ui'), self)
        self.imagen.setPixmap(QPixmap(os.path.join(base_path, 'online-library.png')))
        self.imagen.setScaledContents(True)
        self.setWindowTitle("LibraryControl")
        self.setWindowIcon(QIcon(os.path.join(base_path, 'icono.ico')))


        # 🔥 Mostrar usuario en la interfaz (asegúrate de tener un QLabel llamado label_user)
        try:
            self.saludo.setText(f"Hola Bienvenid@!,")
            self.rol.setText(f"{usuario}")
        except:
            pass

        # 🔹 Crear el botón "EMPLEADOS" debajo del banner
        self.btn_empleados = QtWidgets.QPushButton("⚙️ MENÚ EMPLEADOS", self.centralwidget)
        self.btn_empleados.setGeometry(20, 100, 200, 40)
        self.btn_empleados.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_empleados.setStyleSheet("""
            QPushButton {
                background-color: #6829DB;
                color: white;
                font: bold 10pt "Berlin Sans FB Demi";
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #AB88EB;
            }
            QPushButton::menu-indicator {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                right: 10px;
            }
        """)

        # Acciones para el menú del botón
        accion_registrar = QtWidgets.QAction("📝 Registrar", self)
        accion_registrar.triggered.connect(self.abrir_registro)

        accion_logout = QtWidgets.QAction("🚪 Cerrar Sesión", self)
        accion_logout.triggered.connect(self.cerrar_sesion)
        
        # Crear el menú que se despliega al presionar el botón
        menu_desplegable = QtWidgets.QMenu(self)
        menu_desplegable.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #6829DB;
            }
            QMenu::item {
                padding: 8px 25px;
                font: 10pt "Arial";
            }
            QMenu::item:selected {
                background-color: #F5F6FA;
                color: #6829DB;
            }
        """)
        menu_desplegable.addAction(accion_registrar)
        menu_desplegable.addAction("🔍 Consulta Individual")
        menu_desplegable.addAction(accion_consulta_gral)
        menu_desplegable.addAction("✏️ Cambiar")
        menu_desplegable.addAction("❌ Eliminar")

        # Asignar el menú al botón
        self.btn_empleados.setMenu(menu_desplegable)

        # 🔹 Botón de Cerrar Sesión en el Banner (al lado del usuario)
        self.btn_logout = QtWidgets.QPushButton("🚪 CERRAR SESIÓN", self.barra)
        self.btn_logout.setGeometry(810, 20, 140, 40)
        self.btn_logout.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: rgba(23, 0, 35, 20);
                color: rgb(23, 0, 35);
                font: bold 8pt "Arial";
                border: 1px solid rgb(23, 0, 35);
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #6829DB;
                color: white;
                border: none;
            }
        """)
        self.btn_logout.clicked.connect(self.cerrar_sesion)



    def abrir_registro(self):
        self.ventana_registro = RegistroEmpleado()
        self.ventana_registro.exec_()

    def abrir_consulta_gral(self):
        self.ventana_consulta = ConsultaGeneral()
        self.ventana_consulta.exec_()

    def cerrar_sesion(self):
        self.login = MiVentana()
        self.login.show()
        self.close()


# 🔹 FORMULARIO DE REGISTRO DE EMPLEADOS
class RegistroEmpleado(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Empleado")
        self.resize(400, 300)
        
        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        
        self.input_codigo = QtWidgets.QLineEdit()
        self.input_nombre = QtWidgets.QLineEdit()
        self.input_direccion = QtWidgets.QLineEdit()
        self.input_telefono = QtWidgets.QLineEdit()
        
        self.combo_sexo = QtWidgets.QComboBox()
        self.combo_sexo.addItems(["F", "M"])
        
        self.input_fecha = QtWidgets.QLineEdit()
        self.input_fecha.setPlaceholderText("DD-MM-YYYY")
        
        self.combo_turno = QtWidgets.QComboBox()
        self.combo_turno.addItems(["Matutino", "Vespertino", "Nocturno"])
        
        form_layout.addRow("Código:", self.input_codigo)
        form_layout.addRow("Nombre:", self.input_nombre)
        form_layout.addRow("Dirección:", self.input_direccion)
        form_layout.addRow("Teléfono:", self.input_telefono)
        form_layout.addRow("Sexo:", self.combo_sexo)
        form_layout.addRow("Fecha de nac:", self.input_fecha)
        form_layout.addRow("Turno:", self.combo_turno)
        
        self.btn_registrar = QtWidgets.QPushButton("Registrar")
        self.btn_registrar.clicked.connect(self.registrar_empleado)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_registrar)
        self.setLayout(layout)

    def registrar_empleado(self):
        # Instrucción de SQL empotrada para el alta (como se solicitó en el paso 8)
        # Nota: Dejé la ejecución comentada o preparada para cuando tengas lista la tabla Empleado.
        consulta_sql = '''
            INSERT INTO empleado (codigo, nombre, direccion, telefono, sexo, fecha_nac, turno)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        datos = (
            self.input_codigo.text(),
            self.input_nombre.text(),
            self.input_direccion.text(),
            self.input_telefono.text(),
            self.combo_sexo.currentText(),
            self.input_fecha.text(),
            self.combo_turno.currentText()
        )
        
        try:
            # Ejecutar la inserción en la base de datos
            datos_formateados = (
                int(self.input_codigo.text()), # Convertir a entero para el campo integer
                self.input_nombre.text(),
                self.input_direccion.text(),
                self.input_telefono.text(),
                self.combo_sexo.currentText(),
                self.input_fecha.text(),
                self.combo_turno.currentText()
            )
            
            cursor.execute(consulta_sql, datos_formateados)
            conexion.commit()
            
            QtWidgets.QMessageBox.information(self, "Éxito", "Empleado registrado correctamente en la base de datos.")
            self.close()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error de Datos", "El Código debe ser un número entero.")
        except Exception as e:
            conexion.rollback() # Revertir en caso de error
            QtWidgets.QMessageBox.warning(self, "Error", f"Hubo un problema al registrar en la BD: {e}")


# 🔹 VENTANA DE CONSULTA GENERAL
class ConsultaGeneral(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consulta General de Empleados")
        self.resize(850, 500)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.titulo = QtWidgets.QLabel("LISTADO GENERAL DE EMPLEADOS")
        self.titulo.setStyleSheet("font: bold 14pt 'Arial'; color: #6829DB; margin-bottom: 10px;")
        self.titulo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.titulo)
        
        self.tabla = QtWidgets.QTableWidget()
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # Solo lectura
        self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setStyleSheet("QHeaderView::section { background-color: #6829DB; color: white; font-weight: bold; }")
        
        layout.addWidget(self.tabla)
        self.setLayout(layout)
        
        self.cargar_datos()

    def cargar_datos(self):
        try:
            # Consultar todos los empleados
            cursor.execute("SELECT * FROM empleado ORDER BY codigo ASC")
            filas = cursor.fetchall()
            
            self.tabla.setRowCount(len(filas))
            self.tabla.setColumnCount(7)
            self.tabla.setHorizontalHeaderLabels(["Código", "Nombre", "Dirección", "Teléfono", "Sexo", "Fecha Nac.", "Turno"])
            
            for i, fila in enumerate(filas):
                for j, valor in enumerate(fila):
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    self.tabla.setItem(i, j, item)
            
            self.tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudieron cargar los datos: {e}")



#VENTANA DE LOGEO
class MiVentana(QDialog):
    def __init__(self):
        super().__init__()
        import os
        base_path = os.path.dirname(__file__)
        uic.loadUi(os.path.join(base_path, 'AV1', '6.ui'), self)
        
        self.setWindowTitle("LibraryControl - Login")
        self.setWindowIcon(QIcon(os.path.join(base_path, 'icono.ico')))

        self.btn_login.clicked.connect(self.login)

    def login(self):
        usuario = self.input_user.text()
        password = self.input_pass.text()

        consulta = 'SELECT * FROM usuario WHERE nombre_del_usuario = %s AND contrasena = %s'
        cursor.execute(consulta, (usuario, password))

        resultado = cursor.fetchone()

        if resultado:
            QtWidgets.QMessageBox.information(self, "Login", "Login correcto")

            #Abrir el main
            self.main = Main(usuario)
            self.main.show()

            #Cerrar login
            self.close()

        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")


#EJECUCIÓN
app = QApplication(sys.argv)

ventana = MiVentana()
ventana.show()

app.exec()

#Cerrar conexión al salir
cursor.close()
conexion.close()
=======
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
