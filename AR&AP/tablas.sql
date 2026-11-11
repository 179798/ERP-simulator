-- Tabla de Órdenes de Compra
CREATE TABLE IF NOT EXISTS OrdenesCompra (
    OCID SERIAL PRIMARY KEY,
    Folio VARCHAR(20) UNIQUE NOT NULL,
    ProveedorID INT NOT NULL,  -- FK Provedores
    Fecha DATE NOT NULL,
    Estatus CHAR(1) DEFAULT 'A' CHECK (Estatus IN ('A','C','X')),
    Subtotal NUMERIC(12,2) NOT NULL CHECK (Subtotal >= 0),
    IVA NUMERIC(12,2) NOT NULL CHECK (IVA >= 0),
    Total NUMERIC(12,2) NOT NULL CHECK (Total >= 0),
    CreadoPor VARCHAR(50),
    FechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ModificadoPor VARCHAR(50),
    CHECK (Total = Subtotal + IVA)
);