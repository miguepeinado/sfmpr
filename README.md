# Base de datos del SFMPR

Base de datos para la gestión del SFMPR.
Realizada en **Python 2.7/Django 1.11.**

## *Versión 0.1 (27/09/18)*

Es capaz de gestionar los centros y los servicios
a los que el SFMPR presta servicios.

## *Versión 0.2*

* Importada la base de datos con los centros y servicios
* Importada la tabla de equipos
* Badge en el botón de los hijos
* Vista detalle de un registro de una forma más pitónica
(en las plantillas "ver..." no se detallan todos los campos sino que
 se hace con un bucle) 
* Añadida funcionalidad para los equipos

### TODO

1. Cambiar la interfaz de usuario
    1. Poner los formularios como *pop-ups*.
    1. Incluir dos tablas en una sola vista.
    1. Personalizar los widgets de los formularios.
    1. Poner una barra de navegacion debajo del epigrafe
1. Pedir ususario/contraseña al comienzo.
1. Hacer un *log out* al final 
1. Barra de búsqueda
1. Cambiar a un motor de bases de datos más seguro que sqlite
1. Completar la tabla de modalidades y cambiarlas en los equipos
1. ...y por supuesto añadir nuevas funcionalidades:
    1. Equipos-> Incidencias: Gestión y equipos declarados en un año
    1. Dosímetros
    1. Licencias

...con informes y notificaciones de todo. 

### BUGS

No se han detectado Bugs