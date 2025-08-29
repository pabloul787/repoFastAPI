## Entrega 1
### Integrantes: Joaquin Troncoso (jtroncoss) y Pablo Uribe (pabloul787)

#### El proyecto a realizar serán diversos endpoints los cuales al ser consultados utilizarán información tanto pesonal, como externa mediante APIs o webscraping y de base de datos para exponerle o realizar analisis a partir de la combinación de esta información. En particular realizaramos al menos 8 endpoints los cuales son detallados a continuación:

1. **Endpoint personal**: Este endpoint contendrá información personal sobre los integrantes de este grupo, la cual, a modo de ejemplo, es señalada a continuación:
    + **Nombres**: contiene ambos nombres de cada estudiante
    + **Apellidos**: contiene ambos apellidos de ambos estudiantes.
    + **Ciudad de origen**: muestra la ciudad y si el estudiante es de región o no.
    + Familia: 
        + Numero de integrantes: cantidad de miembros de la familia del estudiante.
        + Gasto en bencina mensual: $ gastado en bencina promedio durante el mes.
        + algun otro...
2. **Endpoint con datos externos**: este endpoint hara webscraping del sitio **astaraluxury.cl** para extraer todos los vehiculos de lujo usados que tiene en venta la empresa astara. A partir de esto, se podrá acceder a la siguiente información:
    + **Fabricante del vehiculo**: nombre de la empresa que fabricó el vehiculo
    + **Año de fabricación**: año en el que el vehiculo fue entregado al dueño original terminado.
    + **Modelo del vehiculo**: descripción con el nombre del modelo entregado por el fabricante.
    + **Kilometraje**: Kms recorridos por el vehiculo al momento de la venta.
    + **Precio**: valor del vehiculo publicado por astara.
    + Detalles:
        + Combustible: indica si es a gasolina o eléctrico.
        + Tranmisión: indica si es manual o automático.
3. **Endpoint analitico a partir del anterior**: a partir de la data de automóviles presentados anteriormente se calculará lo siguiente.
    + **Tasa de impuesto al lujo**: 2%
    + **Sujeto a impuesto al lujo**: indicara "Sí" en caso de que este sujeto a impuesto al lujo y "No" si no lo está. Para ello comparara el valor del auto con el umbral en UTA impuesto por el SII, el cual será extraido de las series del Banco Central.
    + **Impuesto al lujo**: indicará el valor del impuesto al lujo para el vehiculo en caso de no estar exento. Será calculado como Precio*tasa de impuesto.
    + **Gastos adicionales**: calculará cuanto gastos adicionales, aparte de la compra del vehiculo, implicará el auto por conceptos de bencina e impuestos durante el año, utilizando la serie del banco central de combustibles.
4. **Endpoint de Base de Datos (Registro de Gastos Personales)**: Este endpoint permitirá gestionar los gastos personales de cada integrante del grupo mediante una base de datos SQLite. Se podrá acceder a la siguiente información y funcionalidades.
    + **Fecha**: día en que se realizó el gasto.
    + **Categoría**: tipo de gasto, por ejemplo: alimentación, transporte, ocio, educación, salud.
    + **Monto**: valor en pesos chilenos del gasto realizado.

    + **Operaciones disponibles**:
        + Crear: ingresar un nuevo gasto en la base de datos.
        + Leer: consultar todos los gastos registrados o filtrar por fecha/categoría.
        + Actualizar: modificar la información de un gasto ya registrado.
        + Eliminar: eliminar un gasto de la base de datos.

5. **Endpoint Analítico (Presupuesto Personal)**: Este endpoint utilizará los datos almacenados en el endpoint de gastos personales para generar un resumen financiero mensual y métricas útiles para la planificación del presupuesto. Se podrá acceder a la siguiente información:
    + **Gasto total del mes**: suma de todos los gastos registrados en un mes determinado.
    + **Promedio diario**: gasto promedio diario basado en los días del mes con al menos un registro de gasto.
    + **Categoría más costosa**: la categoría donde se concentró el mayor gasto durante el mes.
    + **Semana mas estresante financieramente**: entregara la semana donde el gasto acumulado es mayor.
6. Endpoint externo (Transporte publico): permitira acceder a información sobre micros del sistema RED al ingresar un paradero, y conocer un tiempo esperado del proximo bus al paradero.
    + **Paradero**: entregara información sobre el paradero como nombre y si esta funcionando o no.
    + **Tiempo promedio de espera para el proximo bus**: entregara un promedio entre el minimo y maximo tiempo de llegada del bus.
    + **Mensaje**: sera como: Tu bus se encuentra {DISTANCIA} metros de distancia, esperalo ya que llegara en {TIEMPO} minutos.
    + **Fuente de los datos**: https://api.xor.cl/red/bus-stop/

