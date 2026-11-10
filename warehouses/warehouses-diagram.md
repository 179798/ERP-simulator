```mermaid
flowchart TD
    classDef startEvent fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724;
    classDef endEvent fill:#f8d7da,stroke:#dc3545,stroke-width:2px,color:#721c24;
    classDef task fill:#e2e3e5,stroke:#383d41,stroke-width:1px,color:#383d41;
    classDef gateway fill:#fff3cd,stroke:#ffc107,stroke-width:2px,color:#856404;
    classDef subprocess fill:#d1ecf1,stroke:#17a2b8,stroke-width:1px,color:#0c5460;

    Start([Inicio: Necesidad de Planificación MRP]):::startEvent --> Sub1

    subgraph Sub1 [1. Prerrequisitos y Datos Maestros]
        direction TB
        T1_1[Configurar Artículo]:::task --> T1_2[Configurar Proveedor / Cliente ]:::task
    end

    Sub1 --> Sub2

    subgraph Sub2 [2. Demanda Inicial e Inventarios]
        direction TB
        T2_1[Registrar Orden de Compra]:::task --> T2_2[Recepción de Mercancía Goods Receipt PO]:::task
        T2_2 --> T2_3[Crear Orden de Venta Sales Order]:::task
        T2_3 --> T2_4[Verificar Estado de Inventario]:::task
    end

    Sub2 --> Sub3

    subgraph Sub3 [3. Pronóstico de Ventas Forecast]
        direction TB
        T3_1[Configurar Código y Fechas]:::task --> T3_2[Generar Pronóstico por Historial de Ventas]:::task
        T3_2 --> T3_3[Ajustar Cantidades Mensuales]:::task
    end

    Sub3 --> Sub4

    subgraph Sub4 [4. Asistente de MRP - MRP Wizard]
        direction TB
        T4_1[Paso 1: Escenario]:::task --> T4_2[Paso 2: Detalles y Horizonte de Fechas]:::task
        T4_2 --> T4_3[Paso 3: Selección de Artículo ]:::task
        T4_3 --> T4_4[Paso 4: Selección de Almacenes Consolidado vs. Individual]:::task
        T4_4 --> T4_5[Paso 5: Fuentes de Datos y Forecast PSF1]:::task
    end

    Sub4 --> Sub5

    subgraph Sub5 [5. Ejecución y Análisis de Resultados]
        direction TB
        T5_1[Ejecutar Cálculo del MRP]:::task --> T5_2[Analizar Pestaña Reporte: Stock Inicial + Oferta - Demanda]:::task
        T5_2 --> T5_3[Revisar Pestaña Recomendaciones]:::task
    end

    Sub5 --> G1{¿Se aprueban las Recomendaciones?}:::gateway

    G1 -- No --> T4_1
    G1 -- Sí --> Sub6

    subgraph Sub6 [6. Recomendación de Pedido Order Recommendation]
        direction TB
        T6_1[Configurar Criterios de Selección]:::task --> T6_2[Seleccionar Órdenes de Compra a Generar]:::task
        T6_2 --> T6_3[Procesar y Actualizar Recomendaciones]:::task
    end

    Sub6 --> End([Fin: Generación Automática de Órdenes de Compra]):::endEvent```
