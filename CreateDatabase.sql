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

CREATE TABLE [dbo].[Empleados](
	[id] [int] NOT NULL,
	[nombreCompleto] [varchar](50) NULL,
	[edad] [int] NULL,
	[Genero] [varchar](50) NULL,
	[puesto] [varchar](50) NULL,
	[salario] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

alter table Empleados add supervisor bit;
update Empleados set supervisor = 1
where puesto = 'Manager'

alter table Empleados add  Correo nvarchar(50);
go
update Empleados set Correo = 'henry.troncoso@hotmail.es'
go



drop table Solicitud
go

CREATE TABLE [dbo].[Solicitud](
	[id_solicitud] [int] IDENTITY(1,1) NOT NULL,
	[id_empleado] [int] NULL,
	[tipo_trabajo] [varchar](50) NULL,
	[duracion] [int] NULL,
	[riesgos] [varchar](50) NULL,
	[urgencia] [varchar](50) NULL,
	[fecha] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[id_solicitud] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[Solicitud]  WITH CHECK ADD FOREIGN KEY([id_empleado])
REFERENCES [dbo].[Empleados] ([id])

-- alter table Solicitud add column aprobada kind binary;
alter table Solicitud add aprobada TINYINT
alter table Solicitud drop column aprobada

--0 pendiente
--1 Aprobada
--2 rechazada




create table detalle_aprobacion(
    id_detalle int identity (1,1) primary key,
    id_solicitud int,
    fechaActualizacion datetime,
	fechaAprobacion datetime,
    observaciones nvarchar(500),
    Estadoaprobacion TINYINT,
    foreign key (id_solicitud) references Solicitud(id_solicitud),
);


--etl para insertar en detalle_aprobacion
insert into  detalle_aprobacion ([id_solicitud],Estadoaprobacion, [fechaActualizacion], observaciones)
select 
[id_solicitud],
0 as 'Estadoaprobacion',
cast ([fecha] as datetime),
'Abrio la solicitud' as observaciones
from 
[dbo].[Solicitud]


--return more recent d.fechaActualizacion 
select
d.id_solicitud,
e.[nombreCompleto],
case d.Estadoaprobacion
when 0 then 'Pendiente'
when 2 then 'rechazada'
end as Estadoaprobacion,
d.observaciones
,d.fechaActualizacion as ultimaActulizacion
 from 
Empleados as e inner join 
Solicitud as s 
on e.id = s.id_empleado inner join 
detalle_aprobacion as d
on s.id_solicitud = d.id_solicitud 
where d.fechaActualizacion = (select max(fechaActualizacion) from detalle_aprobacion where id_solicitud = d.id_solicitud)
and d.Estadoaprobacion <> 1
