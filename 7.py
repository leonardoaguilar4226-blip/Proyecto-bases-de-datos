import psycopg2 as psy
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtGui import QPixmap, QIcon, QCursor
import sys
import os
import smtplib
from email.message import EmailMessage
from fpdf import FPDF
import datetime


ventanas_abiertas = []

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
        uic.loadUi(os.path.join(base_path, 'main.ui'), self)
        
        img_path = os.path.join(base_path, 'online-library.png')
        if not os.path.exists(img_path):
            img_path = os.path.join(os.path.dirname(base_path), 'online-library.png')
        self.imagen.setPixmap(QPixmap(img_path))
        self.imagen.setScaledContents(True)
        self.setWindowTitle("BIBLIOTECA - LibraryControl")
        
        icon_path = os.path.join(base_path, 'icono.ico')
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(base_path), 'icono.ico')
        self.setWindowIcon(QIcon(icon_path))


        # 🔥 Mostrar usuario en la interfaz (asegúrate de tener un QLabel llamado label_user)
        try:
            self.saludo.setText(f"Hola Bienvenid@!,")
            self.rol.setText(f"{usuario}")
        except:
            pass

        # Conectar los botones que ya vienen diseñados en main.ui.
        self.btnEmp01Registrar.clicked.connect(self.abrir_registro)
        self.btnEmp02ConsultaInd.clicked.connect(self.abrir_consulta_individual_emp)
        self.btnEmp03ConsultaGen.clicked.connect(self.abrir_consulta_gral)
        self.btnEmp04Cambiar.clicked.connect(self.abrir_editar_emp)
        self.btnEmp05Eliminar.clicked.connect(self.abrir_eliminar_emp)

        self.btnAluRegistrar.clicked.connect(self.abrir_registro_alumno)
        self.btnAluConsultaInd.clicked.connect(self.abrir_consulta_individual_al)
        self.btnAluConsultaGen.clicked.connect(self.abrir_consulta_gral_alumno)
        self.btnAluCambiar.clicked.connect(self.abrir_editar_al)
        self.btnAluEliminar.clicked.connect(self.abrir_eliminar_al)

        self.btnProfRegistrar.clicked.connect(self.abrir_registro_profesor)
        self.btnProfConsultaInd.clicked.connect(self.abrir_consulta_individual_prof)
        self.btnProfConsultaGen.clicked.connect(self.abrir_consulta_profesores)
        self.btnProfCambiar.clicked.connect(self.abrir_editar_prof)
        self.btnProfEliminar.clicked.connect(self.abrir_eliminar_prof)

        self.btnPrestRegistrar.clicked.connect(self.abrir_registro_prestamo)
        self.btnPrestDevolver.clicked.connect(self.abrir_devolver_prestamo)
        self.btnPrestConsulta.clicked.connect(self.abrir_consulta_prestamo)
        self.btnPrestConsultas.clicked.connect(self.abrir_consultas_prestamos)

        # Los botones de libros estan en el diseno
        self.btnLibRegistrar.clicked.connect(self.abrir_registro_libro)
        self.btnLibConsultaInd.clicked.connect(self.abrir_consulta_individual_lib)
        self.btnLibConsultaGen.clicked.connect(self.abrir_consulta_general_lib)
        self.btnLibCambiar.clicked.connect(self.abrir_editar_lib)
        self.btnLibEliminar.clicked.connect(self.abrir_eliminar_lib)


        self.btnCerrarSesion.clicked.connect(self.cerrar_sesion)

        # 🔹 Control de Acceso: Solo el 'admin' ve estos menus
        if usuario.lower() != "admin":
            self.employeeColumn.hide()
            self.studentColumn.hide()
            self.professorColumn.hide()



    def abrir_registro(self):
        self.ventana_registro = RegistroEmpleado()
        self.ventana_registro.exec_()

    def abrir_consulta_gral(self):
        self.ventana_consulta = ConsultaGeneral()
        self.ventana_consulta.exec_()

    def abrir_registro_alumno(self):
        self.ventana_registro_al = RegistroAlumno()
        self.ventana_registro_al.exec_()

    def abrir_consulta_gral_alumno(self):
        self.ventana_consulta_al = ConsultaGeneralAlumno()
        self.ventana_consulta_al.exec_()

    def abrir_registro_profesor(self):
        self.ventana_reg_prof = RegistroProfesor()
        self.ventana_reg_prof.exec_()

    def abrir_consulta_profesores(self):
        self.ventana_cons_prof = ConsultaProfesores()
        self.ventana_cons_prof.exec_()

    def abrir_consulta_individual_emp(self):
        self.ventana = ConsultaIndividual("empleado")
        self.ventana.exec_()

    def abrir_editar_emp(self):
        self.ventana = EditarEmpleado()
        self.ventana.exec_()

    def abrir_eliminar_emp(self):
        self.ventana = EliminarRegistro("empleado")
        self.ventana.exec_()

    def abrir_consulta_individual_al(self):
        self.ventana = ConsultaIndividual("alumnos")
        self.ventana.exec_()

    def abrir_editar_al(self):
        self.ventana = EditarAlumno()
        self.ventana.exec_()

    def abrir_eliminar_al(self):
        self.ventana = EliminarRegistro("alumnos")
        self.ventana.exec_()

    def abrir_consulta_individual_prof(self):
        self.ventana = ConsultaIndividual("maestros")
        self.ventana.exec_()

    def abrir_editar_prof(self):
        self.ventana = EditarProfesor()
        self.ventana.exec_()

    def abrir_eliminar_prof(self):
        self.ventana = EliminarRegistro("maestros")
        self.ventana.exec_()

    def abrir_registro_prestamo(self):
        self.ventana = RegistroPrestamo()
        self.ventana.exec_()

    def abrir_devolver_prestamo(self):
        self.ventana = DevolverPrestamo()
        self.ventana.exec_()

    def abrir_consulta_prestamo(self):
        self.ventana = ConsultaPrestamo()
        self.ventana.exec_()

    def abrir_consultas_prestamos(self):
        self.ventana = ConsultasPrestamos()
        self.ventana.exec_()

    def abrir_registro_libro(self):
        self.ventana = RegistroLibro()
        self.ventana.exec_()

    def abrir_consulta_individual_lib(self):
        self.ventana = ConsultaIndividual("libros")
        self.ventana.exec_()

    def abrir_consulta_general_lib(self):
        self.ventana = ConsultaGeneralLibro()
        self.ventana.exec_()

    def abrir_editar_lib(self):
        self.ventana = EditarLibro()
        self.ventana.exec_()

    def abrir_eliminar_lib(self):
        self.ventana = EliminarRegistro("libros")
        self.ventana.exec_()

    def cerrar_sesion(self):
        self.login = MiVentana()
        self.login.show()
        self.close()


class RegistroPrestamo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrar préstamo")
        self.resize(470, 420)

        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()

        self.combo_solicitante = QtWidgets.QComboBox()
        self.combo_solicitante.addItem("Alumno", "A")
        self.combo_solicitante.addItem("Profesor", "P")

        self.input_codigo = QtWidgets.QLineEdit()
        self.input_codigo.setPlaceholderText("Código del alumno o profesor")

        self.input_isbn = QtWidgets.QLineEdit()
        self.input_num_ejemplar = QtWidgets.QSpinBox()
        self.input_num_ejemplar.setMinimum(1)
        self.input_num_ejemplar.setMaximum(999999)

        self.fecha_prestamo = QtWidgets.QDateEdit()
        self.fecha_prestamo.setCalendarPopup(True)
        self.fecha_prestamo.setDate(QtCore.QDate.currentDate())

        self.fecha_limite = QtWidgets.QDateEdit()
        self.fecha_limite.setCalendarPopup(True)
        self.fecha_limite.setDate(QtCore.QDate.currentDate().addDays(7))

        form_layout.addRow("Solicitante:", self.combo_solicitante)
        form_layout.addRow("Código:", self.input_codigo)
        form_layout.addRow("ISBN:", self.input_isbn)
        form_layout.addRow("Número de ejemplar:", self.input_num_ejemplar)
        form_layout.addRow("Fecha de préstamo:", self.fecha_prestamo)
        form_layout.addRow("Fecha límite:", self.fecha_limite)

        self.btn_registrar = QtWidgets.QPushButton("Registrar préstamo")
        self.btn_registrar.clicked.connect(self.registrar_prestamo)

        layout.addLayout(form_layout)
        layout.addWidget(self.btn_registrar)
        self.setLayout(layout)

    def obtener_tipo_solicitante(self):
        tipo = self.combo_solicitante.currentData()
        try:
            cursor.execute(
                """
                SELECT character_maximum_length
                FROM information_schema.columns
                WHERE table_name = 'prestamo'
                  AND column_name = 'tipo_solicitante'
                """
            )
            resultado = cursor.fetchone()
            longitud = resultado[0] if resultado else 1
        except Exception:
            longitud = 1

        if longitud == 1:
            return tipo
        return "Alumno" if tipo == "A" else "Maestro"

    def registrar_prestamo(self):
        tipo = self.obtener_tipo_solicitante()
        codigo = self.input_codigo.text().strip()
        isbn = self.input_isbn.text().strip()

        if not codigo or not isbn:
            QtWidgets.QMessageBox.warning(self, "Datos incompletos", "Captura el código del solicitante y el ISBN.")
            return

        codigo_alumno = codigo if tipo == "A" else None

        try:
            codigo_profesor = int(codigo) if tipo == "P" else None
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Código inválido", "El código del profesor debe ser numérico.")
            return

        consulta_sql = '''
            INSERT INTO prestamo (
                tipo_solicitante, codigo_alumno, codigo_profesor, isbn, num_ejemplar,
                fecha_prestamo, fecha_limite, estatus, multa
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'prestado', 0.00)
        '''

        datos = (
            tipo,
            codigo_alumno,
            codigo_profesor,
            isbn,
            self.input_num_ejemplar.value(),
            self.fecha_prestamo.date().toPyDate(),
            self.fecha_limite.date().toPyDate()
        )

        try:
            cursor.execute(consulta_sql, datos)
            conexion.commit()
            QtWidgets.QMessageBox.information(self, "Éxito", "Préstamo registrado correctamente.")
            self.close()
        except Exception as e:
            conexion.rollback()
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudo registrar el préstamo:\n{e}")


class DevolverPrestamo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Devolver préstamo")
        self.resize(430, 320)

        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()

        self.input_id = QtWidgets.QSpinBox()
        self.input_id.setMinimum(1)
        self.input_id.setMaximum(999999)

        self.fecha_devolucion = QtWidgets.QDateEdit()
        self.fecha_devolucion.setCalendarPopup(True)
        self.fecha_devolucion.setDate(QtCore.QDate.currentDate())

        self.input_multa = QtWidgets.QDoubleSpinBox()
        self.input_multa.setMinimum(0)
        self.input_multa.setMaximum(999999.99)
        self.input_multa.setDecimals(2)
        self.input_multa.setPrefix("$ ")

        self.input_multa.setReadOnly(True)

        form_layout.addRow("ID préstamo:", self.input_id)
        form_layout.addRow("Fecha devolución:", self.fecha_devolucion)
        form_layout.addRow("Multa:", self.input_multa)

        self.info = QtWidgets.QTextEdit()
        self.info.setReadOnly(True)

        self.btn_buscar = QtWidgets.QPushButton("Buscar préstamo")
        self.btn_buscar.clicked.connect(self.buscar_prestamo)

        self.btn_devolver = QtWidgets.QPushButton("Marcar como entregado")
        self.btn_devolver.clicked.connect(self.devolver_prestamo)

        self.fecha_devolucion.dateChanged.connect(self.calcular_multa)
        self.prestamo_actual = None

        layout.addLayout(form_layout)
        layout.addWidget(self.btn_buscar)
        layout.addWidget(self.info)
        layout.addWidget(self.btn_devolver)
        self.setLayout(layout)

    def buscar_prestamo(self):
        try:
            cursor.execute(
                """
                SELECT id_prestamo, tipo_solicitante, codigo_alumno, codigo_profesor,
                       isbn, num_ejemplar, fecha_prestamo, fecha_limite, estatus, multa
                FROM prestamo
                WHERE id_prestamo = %s
                """,
                (self.input_id.value(),)
            )
            fila = cursor.fetchone()

            if not fila:
                self.info.setText("No se encontró ese préstamo.")
                self.prestamo_actual = None
                self.input_multa.setValue(0)
                return

            self.prestamo_actual = fila
            self.calcular_multa()

            etiquetas = [
                "ID", "Tipo", "Código alumno", "Código profesor", "ISBN",
                "Ejemplar", "Fecha préstamo", "Fecha límite", "Estatus", "Multa"
            ]
            self.info.setHtml("<br>".join(f"<b>{etiqueta}:</b> {valor}" for etiqueta, valor in zip(etiquetas, fila)))
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudo consultar el préstamo:\n{e}")

    def calcular_multa(self):
        if not self.prestamo_actual:
            self.input_multa.setValue(0)
            return
            
        fecha_limite = self.prestamo_actual[7]
        tipo = self.prestamo_actual[1]
        
        fecha_dev = self.fecha_devolucion.date().toPyDate()
        dias_retraso = (fecha_dev - fecha_limite).days
        
        if dias_retraso > 0:
            if tipo == "Alumno" or tipo == "A":
                multa = dias_retraso * 5
            else:
                multa = dias_retraso * 10
        else:
            multa = 0
            
        self.input_multa.setValue(multa)

    def devolver_prestamo(self):
        if not self.prestamo_actual:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Busca un préstamo primero.")
            return

        multa_calculada = self.input_multa.value()
        correo_remitente = "leonardo.aguilar4226@alumnos.udg.mx"
        password_correo = "bkoz omvr mjnp iuqu"
        
        if multa_calculada > 0:
            # Intentar procesar y enviar el correo primero
            email_enviado = self.procesar_multa(multa_calculada, correo_remitente, password_correo)
            if not email_enviado:
                # Si falló el envío y el usuario eligió NO continuar, salimos sin actualizar la BD
                return

        try:
            cursor.execute(
                """
                UPDATE prestamo
                SET fecha_devolucion = %s,
                    estatus = 'entregado',
                    multa = %s
                WHERE id_prestamo = %s
                """,
                (
                    self.fecha_devolucion.date().toPyDate(),
                    multa_calculada,
                    self.input_id.value()
                )
            )
            conexion.commit()

            if cursor.rowcount > 0:
                if multa_calculada == 0:
                    QtWidgets.QMessageBox.information(self, "Éxito", "Préstamo marcado como entregado (Sin multa).")
                else:
                    QtWidgets.QMessageBox.information(self, "Éxito", "Préstamo marcado como entregado en la base de datos.")
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Sin cambios", "No se encontró el préstamo indicado.")
        except Exception as e:
            conexion.rollback()
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudo devolver el préstamo:\n{e}")

    def procesar_multa(self, monto, correo_remitente, password_correo):
        isbn = self.prestamo_actual[4]
        cursor.execute("SELECT titulo, autores, editorial FROM libros WHERE isbn = %s", (isbn,))
        libro = cursor.fetchone()
        if not libro:
            libro = ("Desconocido", "Desconocido", "Desconocido")
            
        tipo = self.prestamo_actual[1]
        if tipo == "Alumno" or tipo == "A":
            cod = self.prestamo_actual[2]
            cursor.execute("SELECT nombre, correo FROM alumnos WHERE codigo = %s", (cod,))
        else:
            cod = self.prestamo_actual[3]
            cursor.execute("SELECT nombre, correo FROM maestros WHERE codigo = %s", (cod,))
            
        usuario = cursor.fetchone()
        if not usuario:
            QtWidgets.QMessageBox.warning(self, "Error", "No se encontraron los datos del usuario en la base de datos.")
            return False
            
        nombre_usuario = usuario[0]
        correo_usuario = usuario[1]
        fecha_limite = self.prestamo_actual[7]
        fecha_dev = self.fecha_devolucion.date().toPyDate()
        dias_retraso = (fecha_dev - fecha_limite).days
        
        pdf_path = f"multa_{self.input_id.value()}.pdf"
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Header
            pdf.set_fill_color(240, 240, 240)
            pdf.rect(0, 0, 210, 40, 'F')
            pdf.set_font("Arial", 'B', 20)
            pdf.set_text_color(40, 40, 40)
            pdf.cell(0, 20, text="LIBRARY CONTROL", ln=True, align='C')
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(220, 53, 69)
            pdf.cell(0, 10, text="RECIBO DE MULTA POR RETRASO", ln=True, align='C')
            pdf.ln(15)
            
            # User details
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(40, 10, text="Usuario:", border=0)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, text=str(nombre_usuario), ln=True)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(40, 10, text="Correo:", border=0)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, text=str(correo_usuario), ln=True)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(40, 10, text="Motivo:", border=0)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, text="Devolución de libro fuera de la fecha límite", ln=True)
            pdf.ln(5)
            
            # Book details
            pdf.set_font("Arial", 'B', 12)
            pdf.set_fill_color(52, 152, 219)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, text="  DETALLES DEL LIBRO", ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
            
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(30, 8, text="Título:")
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 8, text=str(libro[0]), ln=True)
            
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(30, 8, text="Autor(es):")
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 8, text=str(libro[1]), ln=True)
            
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(30, 8, text="Editorial:")
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 8, text=str(libro[2]), ln=True)
            
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(30, 8, text="ISBN:")
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 8, text=str(isbn), ln=True)
            pdf.ln(5)
            
            # Delay details
            pdf.set_font("Arial", 'B', 12)
            pdf.set_fill_color(243, 156, 18)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, text="  DETALLES DEL RETRASO", ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
            
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(40, 8, text="Fecha Límite:")
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 8, text=str(fecha_limite), ln=True)
            
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(40, 8, text="Fecha Entrega:")
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 8, text=str(fecha_dev), ln=True)
            
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(40, 8, text="Días Retraso:")
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 8, text=str(dias_retraso), ln=True)
            pdf.ln(10)
            
            # Total
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(220, 53, 69)
            pdf.cell(0, 15, text=f"TOTAL A PAGAR: ${monto} MXN", ln=True, align='C', border=1)
            
            pdf.output(pdf_path)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error PDF", f"Error al generar el PDF: {e}")
            return False

        try:
            msg = EmailMessage()
            msg['Subject'] = 'Aviso de Multa - Biblioteca LibraryControl'
            msg['From'] = correo_remitente
            msg['To'] = correo_usuario
            msg.set_content(f"Hola {nombre_usuario},\n\nAdjuntamos el recibo de la multa generada por la devolución tardía del libro '{libro[0]}'.\n\nSaludos,\nEl equipo de la Biblioteca.\n\nFavor de ser puntual en futuras devoluciones\n\nGracias")

            with open(pdf_path, 'rb') as f:
                pdf_data = f.read()
                
            msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=f"Multa_{isbn}.pdf")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(correo_remitente, password_correo)
                smtp.send_message(msg)
                
            QtWidgets.QMessageBox.information(self, "Éxito", f"Correo enviado. Se envió el recibo de multa por ${monto} al correo: {correo_usuario}")
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            return True
        except Exception as e:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                
            respuesta = QtWidgets.QMessageBox.question(
                self, 
                "Aviso de Correo", 
                f"No se pudo enviar el correo (Detalle: {e}).\n\n¿Deseas registrar la devolución del libro en la base de datos de todos modos?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            
            if respuesta == QtWidgets.QMessageBox.Yes:
                return True
            else:
                return False


class ConsultaPrestamo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consulta de préstamo")
        self.resize(460, 330)

        layout = QtWidgets.QVBoxLayout()

        self.input_id = QtWidgets.QSpinBox()
        self.input_id.setMinimum(1)
        self.input_id.setMaximum(999999)

        self.btn_buscar = QtWidgets.QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar)

        self.resultado = QtWidgets.QTextEdit()
        self.resultado.setReadOnly(True)

        layout.addWidget(QtWidgets.QLabel("ID del préstamo:"))
        layout.addWidget(self.input_id)
        layout.addWidget(self.btn_buscar)
        layout.addWidget(self.resultado)
        self.setLayout(layout)

    def buscar(self):
        try:
            cursor.execute(
                """
                SELECT id_prestamo, tipo_solicitante, codigo_alumno, codigo_profesor,
                       isbn, num_ejemplar, fecha_prestamo, fecha_limite,
                       fecha_devolucion, estatus, multa
                FROM prestamo
                WHERE id_prestamo = %s
                """,
                (self.input_id.value(),)
            )
            fila = cursor.fetchone()

            if not fila:
                self.resultado.setText("No se encontró ningún préstamo con ese ID.")
                return

            columnas = [
                "ID préstamo", "Tipo solicitante", "Código alumno", "Código profesor",
                "ISBN", "Número de ejemplar", "Fecha préstamo", "Fecha límite",
                "Fecha devolución", "Estatus", "Multa"
            ]
            self.resultado.setHtml("<br>".join(f"<b>{columna}:</b> {valor}" for columna, valor in zip(columnas, fila)))
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Error en la búsqueda:\n{e}")


class ConsultasPrestamos(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consultas de préstamos")
        self.resize(1050, 500)

        layout = QtWidgets.QVBoxLayout()

        titulo = QtWidgets.QLabel("LISTADO GENERAL DE PRÉSTAMOS")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        titulo.setStyleSheet("font: bold 14pt 'Arial'; color: #b45309; margin-bottom: 10px;")

        self.tabla = QtWidgets.QTableWidget()
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setStyleSheet("QHeaderView::section { background-color: #f59e0b; color: white; font-weight: bold; }")

        self.btn_actualizar = QtWidgets.QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.cargar_datos)

        layout.addWidget(titulo)
        layout.addWidget(self.tabla)
        layout.addWidget(self.btn_actualizar)
        self.setLayout(layout)

        self.cargar_datos()

    def cargar_datos(self):
        try:
            cursor.execute(
                """
                SELECT id_prestamo, tipo_solicitante, codigo_alumno, codigo_profesor,
                       isbn, num_ejemplar, fecha_prestamo, fecha_limite,
                       fecha_devolucion, estatus, multa
                FROM prestamo
                ORDER BY id_prestamo ASC
                """
            )
            filas = cursor.fetchall()

            encabezados = [
                "ID", "Solicitante", "Alumno", "Profesor", "ISBN", "Ejemplar",
                "Fecha préstamo", "Fecha límite", "Fecha devolución", "Estatus", "Multa"
            ]

            self.tabla.setRowCount(len(filas))
            self.tabla.setColumnCount(len(encabezados))
            self.tabla.setHorizontalHeaderLabels(encabezados)

            for i, fila in enumerate(filas):
                for j, valor in enumerate(fila):
                    self.tabla.setItem(i, j, QtWidgets.QTableWidgetItem("" if valor is None else str(valor)))

            self.tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudieron cargar los préstamos:\n{e}")


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
        self.combo_turno.addItems(["Matutino", "Vespertino"])
        
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
        consulta_sql = '''
            INSERT INTO empleado (codigo, nombre, direccion, telefono, sexo, fecha_nac, turno)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        
        try:
            # Ejecutar la inserción en la base de datos
            datos_formateados = (
                int(self.input_codigo.text()), # Convertir a entero para el campo integer
                self.input_nombre.text(),
                self.input_direccion.text(),
                self.input_departamento.text(),
                self.combo_ .currentText(),
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

class RegistroAlumnos(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Alumnos")
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
        self.combo_turno.addItems(["Matutino", "Vespertino"])
        
        form_layout.addRow("Código:", self.input_codigo)
        form_layout.addRow("Nombre:", self.input_nombre)
        form_layout.addRow("Dirección:", self.input_direccion)
        form_layout.addRow("Teléfono:", self.input_telefono)
        form_layout.addRow("Sexo:", self.combo_sexo)
        form_layout.addRow("Fecha de nac:", self.input_fecha)
        form_layout.addRow("Turno:", self.combo_turno)
        
        self.btn_registrar = QtWidgets.QPushButton("Registrar")
        self.btn_registrar.clicked.connect(self.registrar_alumno)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_registrar)
        self.setLayout(layout)

    def registrar_alumno(self):
        # Instrucción de SQL empotrada para el alta (como se solicitó en el paso 8)
        consulta_sql = '''
            INSERT INTO alumno (codigo, nombre, direccion, telefono, sexo, fecha_nac, turno)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        
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
            
            QtWidgets.QMessageBox.information(self, "Éxito", "Alumno registrado correctamente en la base de datos.")
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


# 🔹 FORMULARIO DE REGISTRO DE ALUMNOS
class RegistroAlumno(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Alumno")
        self.resize(400, 300)
        
        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        
        self.input_codigo = QtWidgets.QLineEdit()
        self.input_nombre = QtWidgets.QLineEdit()
        self.input_carrera = QtWidgets.QLineEdit()
        self.input_correo = QtWidgets.QLineEdit()
        self.input_direccion = QtWidgets.QLineEdit()
        self.input_telefono = QtWidgets.QLineEdit()
        
        self.combo_sexo = QtWidgets.QComboBox()
        self.combo_sexo.addItems(["F", "M"])
        
        self.input_fecha_nac = QtWidgets.QLineEdit()
        self.input_fecha_nac.setPlaceholderText("DD-MM-YYYY")
        
        form_layout.addRow("Código:", self.input_codigo)
        form_layout.addRow("Nombre:", self.input_nombre)
        form_layout.addRow("Carrera:", self.input_carrera)
        form_layout.addRow("Correo:", self.input_correo)
        form_layout.addRow("Dirección:", self.input_direccion)
        form_layout.addRow("Teléfono:", self.input_telefono)
        form_layout.addRow("Sexo:", self.combo_sexo)
        form_layout.addRow("Fecha Nacimiento:", self.input_fecha_nac)
        
        self.btn_registrar = QtWidgets.QPushButton("Registrar")
        self.btn_registrar.clicked.connect(self.registrar_alumno)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_registrar)
        self.setLayout(layout)

    def registrar_alumno(self):
        consulta_sql = '''
            INSERT INTO alumnos (codigo, nombre, carrera, correo, direccion, telefono, sexo, fecha_nac)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        
        try:
            datos_formateados = (
                int(self.input_codigo.text()),
                self.input_nombre.text(),
                self.input_carrera.text(),
                self.input_correo.text(),
                self.input_direccion.text(),
                self.input_telefono.text(),
                self.combo_sexo.currentText(),
                self.input_fecha_nac.text()
            )
            
            cursor.execute(consulta_sql, datos_formateados)
            conexion.commit()
            
            QtWidgets.QMessageBox.information(self, "Éxito", "Alumno registrado correctamente.")
            self.close()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error de Datos", "El Código debe ser un número entero.")
        except Exception as e:
            conexion.rollback()
            QtWidgets.QMessageBox.warning(self, "Error", f"Hubo un problema al registrar en la BD: {e}")


# 🔹 VENTANA DE CONSULTA GENERAL DE ALUMNOS
class ConsultaGeneralAlumno(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consulta General de Alumnos")
        self.resize(850, 500)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.titulo = QtWidgets.QLabel("LISTADO GENERAL DE ALUMNOS")
        self.titulo.setStyleSheet("font: bold 14pt 'Arial'; color: #2980B9; margin-bottom: 10px;")
        self.titulo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.titulo)
        
        self.tabla = QtWidgets.QTableWidget()
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setStyleSheet("QHeaderView::section { background-color: #2980B9; color: white; font-weight: bold; }")
        
        layout.addWidget(self.tabla)
        self.setLayout(layout)
        
        self.cargar_datos()

    def cargar_datos(self):
        try:
            cursor.execute("SELECT * FROM alumnos ORDER BY codigo ASC")
            filas = cursor.fetchall()
            
            self.tabla.setRowCount(len(filas))
            self.tabla.setColumnCount(8)
            self.tabla.setHorizontalHeaderLabels(["Código", "Nombre", "Carrera", "Correo", "Dirección", "Teléfono", "Sexo", "Fecha Nacimiento."])
            
            for i, fila in enumerate(filas):
                for j, valor in enumerate(fila):
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    self.tabla.setItem(i, j, item)
            
            self.tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudieron cargar los datos: {e}")


# 🔹 FORMULARIO DE REGISTRO DE PROFESORES
class RegistroProfesor(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Profesor")
        self.resize(400, 350)
        
        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        
        self.input_codigo = QtWidgets.QLineEdit()
        self.input_nombre = QtWidgets.QLineEdit()
        self.input_departamento = QtWidgets.QLineEdit()
        self.input_correo = QtWidgets.QLineEdit()
        self.input_direccion = QtWidgets.QLineEdit()
        self.input_telefono = QtWidgets.QLineEdit()
        
        self.combo_sexo = QtWidgets.QComboBox()
        self.combo_sexo.addItems(["F", "M"])
        
        self.input_fecha_nac = QtWidgets.QLineEdit()
        self.input_fecha_nac.setPlaceholderText("DD-MM-YYYY")
        
        form_layout.addRow("Código:", self.input_codigo)
        form_layout.addRow("Nombre:", self.input_nombre)
        form_layout.addRow("Departamento:", self.input_departamento)
        form_layout.addRow("Correo:", self.input_correo)
        form_layout.addRow("Dirección:", self.input_direccion)
        form_layout.addRow("Teléfono:", self.input_telefono)
        form_layout.addRow("Sexo:", self.combo_sexo)
        form_layout.addRow("Fecha Nacimiento:", self.input_fecha_nac)
        
        self.btn_registrar = QtWidgets.QPushButton("Registrar")
        self.btn_registrar.clicked.connect(self.registrar_profesor)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_registrar)
        self.setLayout(layout)

    def registrar_profesor(self):
        consulta_sql = '''
            INSERT INTO maestros (codigo, nombre, departamento, correo, direccion, telefono, sexo, fecha_nac)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        
        try:
            datos = (
                int(self.input_codigo.text()),
                self.input_nombre.text(),
                self.input_departamento.text(),
                self.input_correo.text(),
                self.input_direccion.text(),
                self.input_telefono.text(),
                self.combo_sexo.currentText(),
                self.input_fecha_nac.text()
            )
            
            cursor.execute(consulta_sql, datos)
            conexion.commit()
            
            QtWidgets.QMessageBox.information(self, "Éxito", "Maestro registrado correctamente.")
            self.close()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "El código debe ser numérico.")
        except Exception as e:
            conexion.rollback()
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudo registrar: {e}")


# 🔹 VENTANA DE CONSULTA GENERAL DE PROFESORES
class ConsultaProfesores(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consulta General de Profesores")
        self.resize(850, 500)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.titulo = QtWidgets.QLabel("LISTADO GENERAL DE PROFESORES")
        self.titulo.setStyleSheet("font: bold 14pt 'Arial'; color: #27AE60; margin-bottom: 10px;")
        self.titulo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.titulo)
        
        self.tabla = QtWidgets.QTableWidget()
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setStyleSheet("QHeaderView::section { background-color: #27AE60; color: white; font-weight: bold; }")
        
        layout.addWidget(self.tabla)
        self.setLayout(layout)
        
        self.cargar_datos()

    def cargar_datos(self):
        try:
            cursor.execute("SELECT codigo, nombre, departamento, correo, direccion, telefono, sexo, fecha_nac FROM maestros ORDER BY codigo ASC")
            filas = cursor.fetchall()
            
            self.tabla.setRowCount(len(filas))
            self.tabla.setColumnCount(8)
            self.tabla.setHorizontalHeaderLabels(["Código", "Nombre", "Departamento", "Correo", "Dirección", "Teléfono", "Sexo", "Fecha Nac."])
            
            for i, fila in enumerate(filas):
                for j, valor in enumerate(fila):
                    self.tabla.setItem(i, j, QtWidgets.QTableWidgetItem(str(valor)))
            
            self.tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudieron cargar los datos: {e}")


# 🔹 CLASES GENÉRICAS (Consulta Individual, Editar, Eliminar)

class ConsultaIndividual(QDialog):
    def __init__(self, tabla):
        super().__init__()
        self.tabla_nombre = tabla
        self.setWindowTitle(f"Consulta Individual - {tabla.capitalize()}")
        self.resize(400, 250)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.input_codigo = QtWidgets.QLineEdit()
        self.input_codigo.setPlaceholderText("Ingrese código a buscar")
        
        self.btn_buscar = QtWidgets.QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar)
        
        self.resultado = QtWidgets.QTextEdit()
        self.resultado.setReadOnly(True)
        
        layout.addWidget(QtWidgets.QLabel(f"Buscar en {tabla}:"))
        layout.addWidget(self.input_codigo)
        layout.addWidget(self.btn_buscar)
        layout.addWidget(self.resultado)
        self.setLayout(layout)

    def buscar(self):
        codigo = self.input_codigo.text()
        try:
            # Determinamos la columna de código según la tabla (alumnos usa 'codigo', empleado usa 'codigo', profesor usa 'codigo')
            key_col = "isbn" if self.tabla_nombre == "libros" else "codigo"
            cursor.execute(f"SELECT * FROM {self.tabla_nombre} WHERE {key_col} = %s", (codigo,))
            fila = cursor.fetchone()
            
            if fila:
                # Obtener nombres de columnas
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.tabla_nombre}' ORDER BY ordinal_position")
                columnas = [col[0] for col in cursor.fetchall()]
                
                texto = ""
                for col, val in zip(columnas, fila):
                    texto += f"<b>{col.capitalize()}:</b> {val}<br>"
                self.resultado.setHtml(texto)
            else:
                self.resultado.setText(f"No se encontró ningún registro con ese {'ISBN' if self.tabla_nombre == 'libros' else 'código'}.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Error en la búsqueda: {e}")


class EditarEmpleado(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar Empleado")
        self.resize(400, 350)
        
        layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        
        self.input_buscar = QtWidgets.QLineEdit()
        self.btn_buscar = QtWidgets.QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar)
        
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(QtWidgets.QLabel("Código a editar:"))
        search_layout.addWidget(self.input_buscar)
        search_layout.addWidget(self.btn_buscar)
        layout.addLayout(search_layout)
        
        self.input_codigo = QtWidgets.QLineEdit()
        self.input_codigo.setReadOnly(True)
        self.input_nombre = QtWidgets.QLineEdit()
        self.input_direccion = QtWidgets.QLineEdit()
        self.input_telefono = QtWidgets.QLineEdit()
        self.combo_sexo = QtWidgets.QComboBox()
        self.combo_sexo.addItems(["F", "M"])
        self.input_fecha = QtWidgets.QLineEdit()
        self.combo_turno = QtWidgets.QComboBox()
        self.combo_turno.addItems(["Matutino", "Vespertino"])
        
        self.form_layout.addRow("Código (Bloqueado):", self.input_codigo)
        self.form_layout.addRow("Nombre:", self.input_nombre)
        self.form_layout.addRow("Dirección:", self.input_direccion)
        self.form_layout.addRow("Teléfono:", self.input_telefono)
        self.form_layout.addRow("Sexo:", self.combo_sexo)
        self.form_layout.addRow("Fecha de nac:", self.input_fecha)
        self.form_layout.addRow("Turno:", self.combo_turno)
        
        self.btn_actualizar = QtWidgets.QPushButton("Actualizar")
        self.btn_actualizar.setEnabled(False)
        self.btn_actualizar.clicked.connect(self.actualizar)
        
        layout.addLayout(self.form_layout)
        layout.addWidget(self.btn_actualizar)
        self.setLayout(layout)

    def buscar(self):
        codigo = self.input_buscar.text().strip()
        if not codigo: return
        try:
            cursor.execute("SELECT codigo, nombre, direccion, telefono, sexo, fecha_nac, turno FROM empleado WHERE codigo = %s", (codigo,))
            fila = cursor.fetchone()
            if fila:
                self.input_codigo.setText(str(fila[0]))
                self.input_nombre.setText(str(fila[1]) if fila[1] else "")
                self.input_direccion.setText(str(fila[2]) if fila[2] else "")
                self.input_telefono.setText(str(fila[3]) if fila[3] else "")
                self.combo_sexo.setCurrentText(str(fila[4]) if fila[4] else "F")
                self.input_fecha.setText(str(fila[5]) if fila[5] else "")
                self.combo_turno.setCurrentText(str(fila[6]) if fila[6] else "Matutino")
                self.btn_actualizar.setEnabled(True)
                QtWidgets.QMessageBox.information(self, "Encontrado", "Datos cargados. Ya puedes editarlos.")
            else:
                QtWidgets.QMessageBox.warning(self, "No encontrado", "No existe empleado con ese código.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Error de búsqueda: {e}")

    def actualizar(self):
        try:
            codigo = self.input_codigo.text()
            nombre = self.input_nombre.text()
            direccion = self.input_direccion.text()
            telefono = self.input_telefono.text()
            sexo = self.combo_sexo.currentText()
            fecha = self.input_fecha.text()
            turno = self.combo_turno.currentText()
            
            cursor.execute("UPDATE empleado SET nombre=%s, direccion=%s, telefono=%s, sexo=%s, fecha_nac=%s, turno=%s WHERE codigo=%s",
                           (nombre, direccion, telefono, sexo, fecha, turno, codigo))
            conexion.commit()
            if cursor.rowcount > 0:
                QtWidgets.QMessageBox.information(self, "Éxito", "Empleado actualizado correctamente.")
                self.close()
        except Exception as e:
            conexion.rollback()
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudo actualizar: {e}")

class EditarAlumno(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar Alumno")
        self.resize(400, 400)
        
        layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        
        self.input_buscar = QtWidgets.QLineEdit()
        self.btn_buscar = QtWidgets.QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar)
        
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(QtWidgets.QLabel("Código a editar:"))
        search_layout.addWidget(self.input_buscar)
        search_layout.addWidget(self.btn_buscar)
        layout.addLayout(search_layout)
        
        self.input_codigo = QtWidgets.QLineEdit()
        self.input_codigo.setReadOnly(True)
        self.input_nombre = QtWidgets.QLineEdit()
        self.input_carrera = QtWidgets.QLineEdit()
        self.input_correo = QtWidgets.QLineEdit()
        self.input_direccion = QtWidgets.QLineEdit()
        self.input_telefono = QtWidgets.QLineEdit()
        self.combo_sexo = QtWidgets.QComboBox()
        self.combo_sexo.addItems(["F", "M"])
        self.input_fecha_nac = QtWidgets.QLineEdit()
        
        self.form_layout.addRow("Código (Bloqueado):", self.input_codigo)
        self.form_layout.addRow("Nombre:", self.input_nombre)
        self.form_layout.addRow("Carrera:", self.input_carrera)
        self.form_layout.addRow("Correo:", self.input_correo)
        self.form_layout.addRow("Dirección:", self.input_direccion)
        self.form_layout.addRow("Teléfono:", self.input_telefono)
        self.form_layout.addRow("Sexo:", self.combo_sexo)
        self.form_layout.addRow("Fecha Nac.:", self.input_fecha_nac)
        
        self.btn_actualizar = QtWidgets.QPushButton("Actualizar")
        self.btn_actualizar.setEnabled(False)
        self.btn_actualizar.clicked.connect(self.actualizar)
        
        layout.addLayout(self.form_layout)
        layout.addWidget(self.btn_actualizar)
        self.setLayout(layout)

    def buscar(self):
        codigo = self.input_buscar.text().strip()
        if not codigo: return
        try:
            cursor.execute("SELECT codigo, nombre, carrera, correo, direccion, telefono, sexo, fecha_nac FROM alumnos WHERE codigo = %s", (codigo,))
            fila = cursor.fetchone()
            if fila:
                self.input_codigo.setText(str(fila[0]))
                self.input_nombre.setText(str(fila[1]) if fila[1] else "")
                self.input_carrera.setText(str(fila[2]) if fila[2] else "")
                self.input_correo.setText(str(fila[3]) if fila[3] else "")
                self.input_direccion.setText(str(fila[4]) if fila[4] else "")
                self.input_telefono.setText(str(fila[5]) if fila[5] else "")
                self.combo_sexo.setCurrentText(str(fila[6]) if fila[6] else "F")
                self.input_fecha_nac.setText(str(fila[7]) if fila[7] else "")
                self.btn_actualizar.setEnabled(True)
                QtWidgets.QMessageBox.information(self, "Encontrado", "Datos cargados.")
            else:
                QtWidgets.QMessageBox.warning(self, "No encontrado", "No existe alumno con ese código.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Error de búsqueda: {e}")

    def actualizar(self):
        try:
            codigo = self.input_codigo.text()
            nombre = self.input_nombre.text()
            carrera = self.input_carrera.text()
            correo = self.input_correo.text()
            direccion = self.input_direccion.text()
            telefono = self.input_telefono.text()
            sexo = self.combo_sexo.currentText()
            fecha = self.input_fecha_nac.text()
            
            cursor.execute("UPDATE alumnos SET nombre=%s, carrera=%s, correo=%s, direccion=%s, telefono=%s, sexo=%s, fecha_nac=%s WHERE codigo=%s",
                           (nombre, carrera, correo, direccion, telefono, sexo, fecha, codigo))
            conexion.commit()
            if cursor.rowcount > 0:
                QtWidgets.QMessageBox.information(self, "Éxito", "Alumno actualizado correctamente.")
                self.close()
        except Exception as e:
            conexion.rollback()
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudo actualizar: {e}")

class EditarProfesor(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar Profesor")
        self.resize(400, 400)
        
        layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        
        self.input_buscar = QtWidgets.QLineEdit()
        self.btn_buscar = QtWidgets.QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar)
        
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(QtWidgets.QLabel("Código a editar:"))
        search_layout.addWidget(self.input_buscar)
        search_layout.addWidget(self.btn_buscar)
        layout.addLayout(search_layout)
        
        self.input_codigo = QtWidgets.QLineEdit()
        self.input_codigo.setReadOnly(True)
        self.input_nombre = QtWidgets.QLineEdit()
        self.input_departamento = QtWidgets.QLineEdit()
        self.input_correo = QtWidgets.QLineEdit()
        self.input_direccion = QtWidgets.QLineEdit()
        self.input_telefono = QtWidgets.QLineEdit()
        self.combo_sexo = QtWidgets.QComboBox()
        self.combo_sexo.addItems(["F", "M"])
        self.input_fecha_nac = QtWidgets.QLineEdit()
        
        self.form_layout.addRow("Código (Bloqueado):", self.input_codigo)
        self.form_layout.addRow("Nombre:", self.input_nombre)
        self.form_layout.addRow("Departamento:", self.input_departamento)
        self.form_layout.addRow("Correo:", self.input_correo)
        self.form_layout.addRow("Dirección:", self.input_direccion)
        self.form_layout.addRow("Teléfono:", self.input_telefono)
        self.form_layout.addRow("Sexo:", self.combo_sexo)
        self.form_layout.addRow("Fecha Nac.:", self.input_fecha_nac)
        
        self.btn_actualizar = QtWidgets.QPushButton("Actualizar")
        self.btn_actualizar.setEnabled(False)
        self.btn_actualizar.clicked.connect(self.actualizar)
        
        layout.addLayout(self.form_layout)
        layout.addWidget(self.btn_actualizar)
        self.setLayout(layout)

    def buscar(self):
        codigo = self.input_buscar.text().strip()
        if not codigo: return
        try:
            cursor.execute("SELECT codigo, nombre, departamento, correo, direccion, telefono, sexo, fecha_nac FROM maestros WHERE codigo = %s", (codigo,))
            fila = cursor.fetchone()
            if fila:
                self.input_codigo.setText(str(fila[0]))
                self.input_nombre.setText(str(fila[1]) if fila[1] else "")
                self.input_departamento.setText(str(fila[2]) if fila[2] else "")
                self.input_correo.setText(str(fila[3]) if fila[3] else "")
                self.input_direccion.setText(str(fila[4]) if fila[4] else "")
                self.input_telefono.setText(str(fila[5]) if fila[5] else "")
                self.combo_sexo.setCurrentText(str(fila[6]) if fila[6] else "F")
                self.input_fecha_nac.setText(str(fila[7]) if fila[7] else "")
                self.btn_actualizar.setEnabled(True)
                QtWidgets.QMessageBox.information(self, "Encontrado", "Datos cargados.")
            else:
                QtWidgets.QMessageBox.warning(self, "No encontrado", "No existe profesor con ese código.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Error de búsqueda: {e}")

    def actualizar(self):
        try:
            codigo = self.input_codigo.text()
            nombre = self.input_nombre.text()
            departamento = self.input_departamento.text()
            correo = self.input_correo.text()
            direccion = self.input_direccion.text()
            telefono = self.input_telefono.text()
            sexo = self.combo_sexo.currentText()
            fecha = self.input_fecha_nac.text()
            
            cursor.execute("UPDATE maestros SET nombre=%s, departamento=%s, correo=%s, direccion=%s, telefono=%s, sexo=%s, fecha_nac=%s WHERE codigo=%s",
                           (nombre, departamento, correo, direccion, telefono, sexo, fecha, codigo))
            conexion.commit()
            if cursor.rowcount > 0:
                QtWidgets.QMessageBox.information(self, "Éxito", "Maestro actualizado correctamente.")
                self.close()
        except Exception as e:
            conexion.rollback()
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudo actualizar: {e}")

class EditarLibro(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar Libro")
        self.resize(400, 350)
        
        layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        
        self.input_buscar = QtWidgets.QLineEdit()
        self.btn_buscar = QtWidgets.QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar)
        
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(QtWidgets.QLabel("ISBN a editar:"))
        search_layout.addWidget(self.input_buscar)
        search_layout.addWidget(self.btn_buscar)
        layout.addLayout(search_layout)
        
        self.input_isbn = QtWidgets.QLineEdit()
        self.input_isbn.setReadOnly(True)
        self.input_titulo = QtWidgets.QLineEdit()
        self.input_autores = QtWidgets.QLineEdit()
        self.input_editorial = QtWidgets.QLineEdit()
        self.input_anio = QtWidgets.QLineEdit()
        self.input_ejemplares = QtWidgets.QLineEdit()
        
        self.form_layout.addRow("ISBN (Bloqueado):", self.input_isbn)
        self.form_layout.addRow("Título:", self.input_titulo)
        self.form_layout.addRow("Autores:", self.input_autores)
        self.form_layout.addRow("Editorial:", self.input_editorial)
        self.form_layout.addRow("Año Pub.:", self.input_anio)
        self.form_layout.addRow("Nº Ejemplares:", self.input_ejemplares)
        
        self.btn_actualizar = QtWidgets.QPushButton("Actualizar")
        self.btn_actualizar.setEnabled(False)
        self.btn_actualizar.clicked.connect(self.actualizar)
        
        layout.addLayout(self.form_layout)
        layout.addWidget(self.btn_actualizar)
        self.setLayout(layout)

    def buscar(self):
        isbn = self.input_buscar.text().strip()
        if not isbn: return
        try:
            cursor.execute("SELECT isbn, titulo, autores, editorial, año_publicacion, num_ejemplar FROM libros WHERE isbn = %s", (isbn,))
            fila = cursor.fetchone()
            if fila:
                self.input_isbn.setText(str(fila[0]))
                self.input_titulo.setText(str(fila[1]) if fila[1] else "")
                self.input_autores.setText(str(fila[2]) if fila[2] else "")
                self.input_editorial.setText(str(fila[3]) if fila[3] else "")
                self.input_anio.setText(str(fila[4]) if fila[4] is not None else "")
                self.input_ejemplares.setText(str(fila[5]) if fila[5] is not None else "")
                self.btn_actualizar.setEnabled(True)
                QtWidgets.QMessageBox.information(self, "Encontrado", "Datos cargados.")
            else:
                QtWidgets.QMessageBox.warning(self, "No encontrado", "No existe libro con ese ISBN.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Error de búsqueda: {e}")

    def actualizar(self):
        try:
            isbn = self.input_isbn.text()
            titulo = self.input_titulo.text()
            autores = self.input_autores.text()
            editorial = self.input_editorial.text()
            anio_txt = self.input_anio.text().strip()
            ejemplares_txt = self.input_ejemplares.text().strip()
            
            anio = int(anio_txt) if anio_txt else None
            ejemplares = int(ejemplares_txt) if ejemplares_txt else None
            
            cursor.execute("UPDATE libros SET titulo=%s, autores=%s, editorial=%s, año_publicacion=%s, num_ejemplar=%s WHERE isbn=%s",
                           (titulo, autores, editorial, anio, ejemplares, isbn))
            conexion.commit()
            if cursor.rowcount > 0:
                QtWidgets.QMessageBox.information(self, "Éxito", "Libro actualizado correctamente.")
                self.close()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error de Datos", "El Año y Nº de Ejemplares deben ser números.")
        except Exception as e:
            conexion.rollback()
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudo actualizar: {e}")


class EliminarRegistro(QDialog):
    def __init__(self, tabla):
        super().__init__()
        self.tabla_nombre = tabla
        self.setWindowTitle(f"Eliminar Registro - {tabla.capitalize()}")
        self.resize(350, 150)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.input_codigo = QtWidgets.QLineEdit()
        key_label = "ISBN a eliminar" if tabla == "libros" else "Código a eliminar"
        self.input_codigo.setPlaceholderText(key_label)
        
        self.btn_eliminar = QtWidgets.QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar)
        
        prompt_label = f"¿Qué ISBN deseas eliminar de {tabla}?" if tabla == "libros" else f"¿Qué código deseas eliminar de {tabla}?"
        layout.addWidget(QtWidgets.QLabel(prompt_label))
        layout.addWidget(self.input_codigo)
        layout.addWidget(self.btn_eliminar)
        self.setLayout(layout)

    def eliminar(self):
        codigo = self.input_codigo.text()
        if not codigo: return
        
        confirm = QtWidgets.QMessageBox.question(self, "Confirmar", f"¿Estás seguro de eliminar el registro {codigo} de {self.tabla_nombre}?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        
        if confirm == QtWidgets.QMessageBox.Yes:
            try:
                key_col = "isbn" if self.tabla_nombre == "libros" else "codigo"
                cursor.execute(f"DELETE FROM {self.tabla_nombre} WHERE {key_col} = %s", (codigo,))
                conexion.commit()
                
                if cursor.rowcount > 0:
                    QtWidgets.QMessageBox.information(self, "Éxito", "Registro eliminado correctamente.")
                    self.close()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", f"No se encontró el registro con ese {'ISBN' if self.tabla_nombre == 'libros' else 'código'}.")
            except Exception as e:
                conexion.rollback()
                QtWidgets.QMessageBox.warning(self, "Error", f"No se pudo eliminar: {e}")
class RegistroLibro(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrar Libro")
        self.resize(400, 300)
        
        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        
        self.input_isbn = QtWidgets.QLineEdit()
        self.input_titulo = QtWidgets.QLineEdit()
        self.input_autores = QtWidgets.QLineEdit()
        self.input_editorial = QtWidgets.QLineEdit()
        self.input_anio = QtWidgets.QLineEdit()
        self.input_ejemplares = QtWidgets.QLineEdit()
        
        form_layout.addRow("ISBN:", self.input_isbn)
        form_layout.addRow("Título:", self.input_titulo)
        form_layout.addRow("Autores:", self.input_autores)
        form_layout.addRow("Editorial:", self.input_editorial)
        form_layout.addRow("Año Publicación:", self.input_anio)
        form_layout.addRow("Nº Ejemplares:", self.input_ejemplares)
        
        self.btn_registrar = QtWidgets.QPushButton("Registrar")
        self.btn_registrar.clicked.connect(self.registrar)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_registrar)
        self.setLayout(layout)

    def registrar(self):
        isbn = self.input_isbn.text().strip()
        titulo = self.input_titulo.text().strip()
        autores = self.input_autores.text().strip()
        editorial = self.input_editorial.text().strip()
        anio = self.input_anio.text().strip()
        ejemplares = self.input_ejemplares.text().strip()
        
        if not isbn or not titulo:
            QtWidgets.QMessageBox.warning(self, "Error de Datos", "ISBN y Título son requeridos.")
            return
            
        try:
            anio_val = int(anio) if anio else None
            ejemplares_val = int(ejemplares) if ejemplares else None
            
            cursor.execute(
                "INSERT INTO libros (isbn, titulo, autores, editorial, año_publicacion, num_ejemplar) VALUES (%s, %s, %s, %s, %s, %s)",
                (isbn, titulo, autores, editorial, anio_val, ejemplares_val)
            )
            conexion.commit()
            QtWidgets.QMessageBox.information(self, "Éxito", "Libro registrado correctamente.")
            self.close()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error de Datos", "Año y Nº Ejemplares deben ser números enteros.")
        except Exception as e:
            conexion.rollback()
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudo registrar el libro: {e}")


class ConsultaGeneralLibro(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consulta General de Libros")
        self.resize(850, 500)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.titulo = QtWidgets.QLabel("LISTADO GENERAL DE LIBROS")
        self.titulo.setStyleSheet("font: bold 14pt 'Arial'; color: #10b981; margin-bottom: 10px;")
        self.titulo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.titulo)
        
        self.tabla = QtWidgets.QTableWidget()
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setStyleSheet("QHeaderView::section { background-color: #10b981; color: white; font-weight: bold; }")
        
        layout.addWidget(self.tabla)
        self.setLayout(layout)
        
        self.cargar_datos()

    def cargar_datos(self):
        try:
            cursor.execute("SELECT isbn, titulo, autores, editorial, año_publicacion, num_ejemplar FROM libros ORDER BY isbn ASC")
            filas = cursor.fetchall()
            
            self.tabla.setRowCount(len(filas))
            self.tabla.setColumnCount(6)
            self.tabla.setHorizontalHeaderLabels(["ISBN", "Título", "Autores", "Editorial", "Año Publicación", "Nº Ejemplares"])
            
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
        uic.loadUi(os.path.join(base_path, '6.ui'), self)
        
        # Reducir el tamaño de fuente conservando el tipo de letra original para que no se encimen
        self.titleLabel.setStyleSheet('color: white; background-color: none; font: 25 24pt "Bodoni MT Poster Compressed";')
        self.loginTitle.setStyleSheet('color: white; background-color: none; font: 25 24pt "Bodoni MT Poster Compressed";')
        
        self.setWindowTitle("LibraryControl - Login")
        icon_path = os.path.join(base_path, 'icono.ico')
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(base_path), 'icono.ico')
        self.setWindowIcon(QIcon(icon_path))

        self.btn_login.clicked.connect(self.login)
        
        # Enmascarar la contraseña
        self.input_pass.setEchoMode(QtWidgets.QLineEdit.Password)

    def login(self):
        try:
            usuario = self.input_user.text().strip()
            password = self.input_pass.text()

            consulta = 'SELECT * FROM usuario WHERE nombre_del_usuario = %s AND contrasena = %s'
            cursor.execute(consulta, (usuario, password))

            resultado = cursor.fetchone()

            if resultado:
                # Mantener una referencia fuerte para que Qt no destruya la ventana principal.
                self.main = Main(usuario)
                ventanas_abiertas.append(self.main)
                QtWidgets.QApplication.instance().main = self.main
                self.main.show()
                self.main.raise_()
                self.main.activateWindow()
                self.hide()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
        except Exception as e:
            conexion.rollback()
            QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo iniciar sesión:\n{e}")


#EJECUCIÓN
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(True)

ventana = MiVentana()
ventanas_abiertas.append(ventana)
ventana.show()

app.exec()

#Cerrar conexión al salir
cursor.close()
conexion.close()
