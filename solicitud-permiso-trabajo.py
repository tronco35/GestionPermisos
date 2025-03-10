import flet as ft
import logging
import pyodbc
import configparser

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

def get_db_config():
    config = configparser.ConfigParser()
    config.read('db_config.ini')
    
    db_config = {
        'server': config['database']['server'],
        'database': config['database']['database'],
        'username': config['database']['username'],
        'password': config['database']['password']
    }
    
    return db_config

def main(page: ft.Page):
    page.title = "Solicitud de Permiso de Trabajo"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.colors.LIGHT_BLUE_50

    # Create form fields
    user_id = ft.TextField(label="ID de usuario:")
    job_type = ft.TextField(label="Tipo de trabajo:")
    duration = ft.TextField(label="Duración (horas):", keyboard_type=ft.KeyboardType.NUMBER)
    risks = ft.TextField(label="Riesgos:")

    # Create radio buttons for "Urgencia"
    urgency = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="low", label="Bajo"),
                ft.Radio(value="medium", label="Medio"),
                ft.Radio(value="high", label="Alto"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    )

    # Create a FilePicker for document upload
    file_picker = ft.FilePicker(
        on_result=lambda e: print(f"Selected files: {e.files}")
    )
    page.overlay.append(file_picker)

    def pick_files(e):
        file_picker.pick_files()

    # Function to handle form submission
    def submit_form(e):
        try:
            # Validate form fields
            if not user_id.value or not job_type.value or not duration.value or not risks.value or not urgency.value:
                raise ValueError("Todos los campos son obligatorios")

            # Show confirmation dialog
            show_confirmation_dialog()

        except ValueError as ve:
            logging.error("Validation error during form submission", exc_info=True)
            show_error_dialog(page, f"Validation Error: {str(ve)}", page.route)
        except Exception as ex:
            logging.error("Error during form submission", exc_info=True)
            show_error_dialog(page, f"Error: {str(ex)}", page.route)

    # Function to show confirmation dialog
    def show_confirmation_dialog():
        def confirm_submission(e):
            try:
                # Get database configuration
                db_config = get_db_config()

                # Establish a database connection
                conn = pyodbc.connect(
                     f'DRIVER=ODBC Driver 17 for SQL Server;SERVER=Duque;DATABASE=GestionPerApp;UID=UsrGes;PWD=Bogota123456*'
                )
                cursor = conn.cursor()

                # Insert data into the Solicitud table
                insert_query = """
                INSERT INTO Solicitud (id_empleado, tipo_trabajo, duracion, riesgos, urgencia, fecha)
                VALUES (?, ?, ?, ?, ?,  GETDATE())
                """
                cursor.execute(insert_query, user_id.value, job_type.value, duration.value, risks.value, urgency.value)
                conn.commit()

                # Show success message
                show_success_message()

            except pyodbc.Error as db_err:
                logging.error("Database error during form submission", exc_info=True)
                show_error_dialog(page, f"Database Error: {str(db_err)}", page.route)
            except Exception as ex:
                logging.error("Error during form submission", exc_info=True)
                show_error_dialog(page, f"Error: {str(ex)}", page.route)
            finally:
                if 'conn' in locals():
                    conn.close()

        def close_confirmation_dialog(e):
            confirmation_dialog.open = False
            page.update()

        confirmation_dialog = ft.AlertDialog(
            title=ft.Text("Confirmación de Solicitud"),
            content=ft.Column(
                [
                    ft.Text(f"ID de usuario: {user_id.value}"),
                    ft.Text(f"Tipo de trabajo: {job_type.value}"),
                    ft.Text(f"Duración (horas): {duration.value}"),
                    ft.Text(f"Riesgos: {risks.value}"),
                    ft.Text(f"Urgencia: {urgency.value}"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            actions=[
                ft.ElevatedButton(text="Confirmar datos antes de enviar", bgcolor=ft.colors.GREEN_500, color=ft.colors.WHITE, on_click=confirm_submission),
                ft.ElevatedButton(text="Cancelar", bgcolor=ft.colors.RED_500, color=ft.colors.WHITE, on_click=close_confirmation_dialog)
            ],
            on_dismiss=close_confirmation_dialog
        )
        page.dialog = confirmation_dialog
        confirmation_dialog.open = True
        page.update()

    # Function to show success message
    def show_success_message():
        def close_success_dialog(e):
            success_dialog.open = False
            page.update()

        success_dialog = ft.AlertDialog(
            title=ft.Text("Solicitud Confirmada"),
            content=ft.Text("Su solicitud ha sido confirmada."),
            actions=[
                ft.ElevatedButton(text="OK", bgcolor=ft.colors.GREEN_500, color=ft.colors.WHITE, on_click=close_success_dialog)
            ],
            on_dismiss=close_success_dialog
        )
        page.dialog = success_dialog
        success_dialog.open = True
        page.update()

    # Function to show error dialog
    def show_error_dialog(page, message, return_view):
        def close_dialog(e):
            page.dialog.open = False
            page.update()
            page.go(return_view)

        error_dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=close_dialog)
            ],
            on_dismiss=close_dialog
        )
        page.dialog = error_dialog
        error_dialog.open = True
        page.update()

    # Create submit button
    submit_button = ft.ElevatedButton(text="Enviar", bgcolor=ft.colors.BLUE_500, color=ft.colors.WHITE, on_click=submit_form)

    # Create file upload button
    upload_button = ft.ElevatedButton(text="Cargar documentos", bgcolor=ft.colors.ORANGE_500, color=ft.colors.WHITE, on_click=pick_files)

    # Add fields and buttons to the page
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Solicitud de Permiso de Trabajo", size=30, color=ft.colors.BLUE_GREY_900, text_align=ft.TextAlign.CENTER),
                    user_id,
                    job_type,
                    duration,
                    risks,
                    ft.Text("Urgencia:", size=16, color=ft.colors.BLUE_GREY_700),
                    urgency,
                    upload_button,
                    submit_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=30,
            width=500,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLACK),
        )
    )

ft.app(target=main)

#to do: when return success message, return number ID_solictud