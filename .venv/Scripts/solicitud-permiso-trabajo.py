import flet as ft
import logging
from blockchain import Blockchain1


Blockchain1 = Blockchain1()

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

            # Create a new view with the form information
            info_view = ft.View(
                "/info",
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Información de Solicitud", size=30, color=ft.colors.BLUE_GREY_900, text_align=ft.TextAlign.CENTER),
                                ft.Text(f"ID de usuario: {user_id.value}"),
                                ft.Text(f"Tipo de trabajo: {job_type.value}"),
                                ft.Text(f"Duración (horas): {duration.value}"),
                                ft.Text(f"Riesgos: {risks.value}"),
                                ft.Text(f"Urgencia: {urgency.value}"),
                                ft.ElevatedButton(text="Confirme envío de la información", bgcolor=ft.colors.GREEN_500, color=ft.colors.WHITE, on_click=confirm_submission)
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
                ]
            )

            # Navigate to the new view
            page.views.append(info_view)
            page.go("/info")

        except Exception as ex:
            logging.error("Error during form submission", exc_info=True)
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()

    # Function to handle confirmation and blockchain storage
    def confirm_submission(e):
        try:
            # Add transaction to the blockchain
            blockchain.new_transaction(
                sender="user",
                recipient="blockchain",
                amount={
                    "user_id": user_id.value,
                    "job_type": job_type.value,
                    "duration": duration.value,
                    "risks": risks.value,
                    "urgency": urgency.value
                }
            )
            last_proof = blockchain.last_block['proof']
            proof = blockchain.proof_of_work(last_proof)
            blockchain.new_block(proof)

            # Show success message
            success_view = ft.View(
                "/success",
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Información enviada con éxito a la base de datos blockchain", size=30, color=ft.colors.GREEN_900, text_align=ft.TextAlign.CENTER),
                                ft.ElevatedButton(text="Volver", bgcolor=ft.colors.BLUE_500, color=ft.colors.WHITE, on_click=lambda e: page.go("/"))
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
                ]
            )

            # Navigate to the success view
            page.views.append(success_view)
            page.go("/success")

        except Exception as ex:
            logging.error("Error during blockchain submission", exc_info=True)
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
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