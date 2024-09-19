import flet as ft

def main(page: ft.Page):
    page.title = "My Flet App"
    page.add(ft.Text("Hello, Flet!"))

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER