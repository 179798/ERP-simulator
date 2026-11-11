Recursos

SISTEMAS ERP Y SAP:
GESTIÓN DE RECURSOS ALINEADOS A CALENDARIOS Y HORARIOS 

Especificación Funcional, Reglas de Negocio, Matriz de Pruebas e Integridad de Datos
1. Definición de Requerimientos Funcionales 
El módulo de planificación de capacidad y gestión de recursos en un sistema ERP requiere definir 
explícitamente la capacidad disponible y operativa de los centros de trabajo (Work Centers) y recursos 
humanos/técnicos. Los requerimientos funcionales principales comprenden: 
• RF-01 Gestión de Calendarios: Definición e integración de calendarios de fábrica (Factory Calendar) 
vinculados a la estructura organizacional (Sociedad/Centro). 
• RF-02 Programación de Turnos: Asignación de modelos de turnos (Shift Models) a puestos de 
trabajo y puestos de capacidad con desglose de pausas programadas y tiempo efectivo. 
• RF-03 Capacidad Neta: Cálculo dinámico de la capacidad neta disponible considerando fórmulas de 
utilización y eficiencia operativa. 
• RF-04 Excepciones y Paros: Mantenimiento de excepciones del calendario (días festivos locales, 
paros programados por mantenimiento preventivo, paros de planta). 
• RF-05 Chequeo de Disponibilidad: Verificación de disponibilidad de recursos en tiempo real al 
generar órdenes de producción o mantenimiento.

2. Descripción de las Reglas de Negocio
Las reglas de negocio garantizan la coherencia operativa y evitan la sobreasignación o inconsistencia en la planificación:
•
RN-01 Restricción de Festivos: Un recurso no puede ser asignado a operaciones en fechas/horas marcadas como festivas o no laborales en su calendario de fábrica asignado, salvo que exista una orden de sobretiempo aprobada.
•
RN-02 Continuidad entre Turnos: Si la duración de una operación excede la ventana operativa del turno actual, la programación debe pausarse dinámicamente y reanudarse al inicio del siguiente turno válido.
•
RN-03 Límite de Sobreasignación: Ningún recurso individual o centro de trabajo puede superar el 100% de su capacidad teórica configurada sin activar una alerta de sobrecapacidad. (Capacity Overload).
•
RN-04 Determinación de Tarifas: El costo de la hora hombre/máquina se determinará en función del tipo de turno (diurno, nocturno, festivo, horas extra) asociado a la tarifa del centro de coste.

3. Pruebas Unitarias: Esta prueba verifica de forma aislada que las funciones y BAPIs del sistema (como el cálculo de capacidades o la validación de calendarios) respondan correctamente ante entradas específicas, garantizando por ejemplo que un día festivo devuelva una disponibilidad nula de cero horas.

4. Pruebas Funcionales: Esta prueba evalúa el flujo de trabajo de extremo a extremo dentro de los módulos integrados del ERP —como la programación de órdenes ante días festivos, la nivelación automática de cargas mediante transacciones especializadas y la notificación de horas reales— para asegurar que los procesos de negocio operen de manera coherente.

5. Integridad de los Datos
Para asegurar la fiabilidad operativa y evitar inconsistencias en la base de datos relacional del ERP, se
implementan los siguientes controles de integridad:
• Integridad Referencial: Garantizar que todo registro de capacidad esté vinculado a un puesto de
trabajo y centro de coste existente en las tablas maestras.
• Consistencia Temporal: Validaciones a nivel de base de datos para impedir solapamiento de
horarios en la asignación de turnos a un mismo recurso.
• Trazabilidad y Auditoría: Registro detallado (Change Documents / Audit Trail) de cualquier
modificación realizada a los calendarios de fábrica o capacidades de recursos.
• Integridad Mapeada (Cross-Module): Sincronización bidireccional inmediata de la disponibilidad de
recursos entre el módulo de Producción (PP), Mantenimiento (PM), Proyectos (PS) y Recursos
Humanos (HCM).

```mermaid
flowchart TB
    Start(("Inicio: Solicitud de<br>Programación de Orden")) --> TimerEvent(("Evento de Tiempo:<br>Verificar Calendario de Fábrica"))
    TimerEvent --> Task1["RF-01 / RF-05: Validar disponibilidad<br>de Recurso y Turno (Shift Model)"]
    Task1 --> Gateway1{"¿Día laborable /<br>Turno válido?<br>(RN-01)"}
    Gateway1 -- No (Festivo/No hábil) --> TaskAdjust["RN-02: Reagendar inicio al<br>siguiente turno/día hábil hábil"]
    TaskAdjust --> Task1
    Gateway1 -- Sí --> TaskCapCheck["RF-03: Calcular Capacidad Neta<br>y evaluar Carga de Trabajo"]
    TaskCapCheck --> Gateway2{"¿Capacidad &lt;= 100%?<br>(RN-03)"}
    Gateway2 -- No (Sobreasignación &gt; 100%) --> TaskLeveling["FT-02: Ejecutar Nivelación<br>de Capacidad (CM25)"]
    TaskLeveling --> TaskCapCheck
    Gateway2 -- Sí --> TaskAssign["RF-02: Asignar Recurso,<br>Turno y Tarifas (RN-04)"]
    TaskAssign --> TaskExecute["Ejecutar Operación y<br>Notificar Horas Reales (CO11N)"]
    TaskExecute --> Gateway3{"¿Exceso de horas<br>o tiempo extra?"}
    Gateway3 -- Sí --> TaskOvertime["Calcular Liquidación con<br>Tarifa de Horas Extra"]
    Gateway3 -- No --> TaskStandard["Calcular Liquidación con<br>Tarifa Estándar"]
    TaskOvertime --> End(("Fin: Orden Programada<br>y Liquidada"))
    TaskStandard --> End
    TaskAssign -.- DataStore[/"Tablas Maestras ERP<br>(CRHD, KAKO - Integridad Data"/]

     Start:::startEvent
     TimerEvent:::intermediateEvent
     Task1:::task
     Gateway1:::gateway
     TaskAdjust:::task
     TaskCapCheck:::task
     Gateway2:::gateway
     TaskLeveling:::task
     TaskAssign:::task
     TaskExecute:::task
     Gateway3:::gateway
     TaskOvertime:::task
     TaskStandard:::task
     End:::endEvent
     DataStore:::dataObject
    classDef startEvent fill:#8bc34a,stroke:#333,stroke-width:2px,color:#000
    classDef intermediateEvent fill:#ffb74d,stroke:#333,stroke-width:2px,color:#000
    classDef endEvent fill:#ef5350,stroke:#333,stroke-width:2px,color:#fff
    classDef task fill:#ffca28,stroke:#333,stroke-width:1.5px,color:#000,rx:5,ry:5
    classDef gateway fill:#66bb6a,stroke:#333,stroke-width:2px,color:#000
    classDef dataObject fill:#ffffff,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5,color:#000
