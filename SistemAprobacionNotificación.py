import flet as ft
import pyodbc

def main(page: ft.Page):
    page.title = "Sistema de Aprobación y Notificación"

    def on_submit(e):
        employee_id = int(employee_id_input.value)
        if is_supervisor(employee_id):
            pending_requests = get_pending_requests(employee_id)
            result_text.value = format_pending_requests(pending_requests)
        else:
            result_text.value = "El ID ingresado no pertenece a un supervisor."
        page.update()

    def is_supervisor(employee_id):
        conn = pyodbc.connect( f'DRIVER=ODBC Driver 17 for SQL Server;SERVER=Duque;DATABASE=GestionPerApp;UID=UsrGes;PWD=Bogota123456*')
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM [dbo].[Empleados] WHERE [id] = ? AND [supervisor] = 1", employee_id)
        result = cursor.fetchone()
        conn.close()
        return result[0] > 0

    def get_pending_requests(employee_id):
        conn = pyodbc.connect( f'DRIVER=ODBC Driver 17 for SQL Server;SERVER=Duque;DATABASE=GestionPerApp;UID=UsrGes;PWD=Bogota123456*')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                d.id_solicitud,
                e.[nombreCompleto],
                CASE d.Estadoaprobacion
                    WHEN 0 THEN 'Pendiente'
                    WHEN 2 THEN 'Rechazada'
                END as Estadoaprobacion,
                d.observaciones,
                d.fechaActualizacion as ultimaActulizacion
            FROM 
                Empleados as e 
                INNER JOIN Solicitud as s ON e.id = s.id_empleado 
                INNER JOIN detalle_aprobacion as d ON s.id_solicitud = d.id_solicitud 
            WHERE 
                d.fechaActualizacion = (SELECT MAX(fechaActualizacion) FROM detalle_aprobacion WHERE id_solicitud = d.id_solicitud)
                AND d.Estadoaprobacion <> 1
        """)
        results = cursor.fetchall()
        conn.close()
        return results

    def format_pending_requests(requests):
        formatted = "Solicitudes Pendientes:\n"
        for req in requests:
            formatted += f"ID Solicitud: {req.id_solicitud}, Nombre: {req.nombreCompleto}, Estado: {req.Estadoaprobacion}, Observaciones: {req.observaciones}, Última Actualización: {req.ultimaActulizacion}\n"
        return formatted

    employee_id_input = ft.TextField(label="Supervisor ID", width=200)
    submit_button = ft.ElevatedButton(text="Submit", on_click=on_submit)
    result_text = ft.Text()

    page.add(
        ft.Column([
            ft.Text("Sistema de Aprobación y Notificación", size=24, weight="bold"),
            employee_id_input,
            submit_button,
            result_text
        ])
    )

ft.app(target=main)