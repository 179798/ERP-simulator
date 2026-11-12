CREATE EXTENSION IF NOT EXISTS btree_gist;

-- CATÁLOGOS BASE: UNIDADES DE MEDIDA Y CONVERSIONES
CREATE TABLE unidades_medida (
    uom_id VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    dimension VARCHAR(20) NOT NULL CHECK (dimension IN ('LONGITUD', 'MASA', 'VOLUMEN', 'CONTEO', 'TIEMPO')),
    precision_decimales SMALLINT NOT NULL DEFAULT 0 CHECK (precision_decimales >= 0 AND precision_decimales <= 6),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversiones_uom (
    conversion_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uom_origen_id VARCHAR(10) NOT NULL REFERENCES unidades_medida(uom_id) ON DELETE RESTRICT,
    uom_destino_id VARCHAR(10) NOT NULL REFERENCES unidades_medida(uom_id) ON DELETE RESTRICT,
    factor_multiplicador NUMERIC(18, 8) NOT NULL CHECK (factor_multiplicador > 0),
    sku_especifico VARCHAR(50) NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_conversion UNIQUE (uom_origen_id, uom_destino_id, sku_especifico),
    CONSTRAINT chk_distintas_unidades CHECK (uom_origen_id <> uom_destino_id)
);
