create DATABASE GestionPerApp;


                 --ft.Text("Información de Solicitud", size=30, color=ft.colors.BLUE_GREY_900, text_align=ft.TextAlign.CENTER),
                 --               ft.Text(f"ID de usuario: {user_id.value}"),
                 --               ft.Text(f"Tipo de trabajo: {job_type.value}"),
                 --               ft.Text(f"Duración (horas): {duration.value}"),
                 --               ft.Text(f"Riesgos: {risks.value}"),
                 --               ft.Text(f"Urgencia: {urgency.value}"),
                 --               ft.ElevatedButton(text="Confirme envío de la información", bgcolor=ft.colors.GREEN_500, color=ft.colors.WHIT
use GestionPerApp;
go

create table Empleados(
    id int primary key,
    nombre varchar(50),
    apellido varchar(50),
    edad int,
    telefono varchar(50),
    direccion varchar(50),
    correo varchar(50),
    puesto varchar(50),
    salario float
);

create table Solicitud(
    id_solicitud int primary key,
    id_empleado int,
    tipo_trabajo varchar(50),
    duracion int,
    riesgos varchar(50),
    urgencia varchar(50),
    fecha date,
    foreign key (id_empleado) references Empleados(id)
);