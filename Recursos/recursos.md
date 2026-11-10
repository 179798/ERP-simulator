Recursos



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
