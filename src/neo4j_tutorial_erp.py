import os
from neo4j import GraphDatabase


COMPONENTS = [
    {"code": "CPU001", "name": "CPU Ryzen 7", "quantity": 1},
    {"code": "MB001", "name": "Motherboard B650", "quantity": 1},
    {"code": "RAM001", "name": "RAM 16GB DDR5", "quantity": 2},
    {"code": "SSD001", "name": "SSD 1TB NVMe", "quantity": 1},
    {"code": "PSU001", "name": "Power Supply 750W", "quantity": 1},
    {"code": "GPU001", "name": "Graphics Card RTX", "quantity": 1},
]


def check_indexes(driver):
    index_queries = [
        """
        CREATE INDEX product_code_index IF NOT EXISTS
        FOR (p:Product)
        ON (p.code)
        """,
        """
        CREATE INDEX material_code_index IF NOT EXISTS
        FOR (m:Material)
        ON (m.code)
        """
    ]

    for statement in index_queries:
        driver.execute_query(statement, database_="neo4j")

    print("Los índices de productos y materiales están listos.")


def _test_create_operation(tx):
    result = tx.run(
        """
        CREATE (sample:TutorialExample {name: $value})
        RETURN sample.name AS created_name
        """,
        value="Prueba de creación"
    )

    data = result.single()

    tx.run(
        """
        MATCH (sample:TutorialExample {name: $value})
        DELETE sample
        """,
        value=data["created_name"]
    ).consume()

    return data["created_name"]


def test_create(driver):
    with driver.session(database="neo4j") as session:
        created_name = session.execute_write(_test_create_operation)

    print(f"Se creó el nodo: {created_name}")
    print("El nodo de prueba fue eliminado correctamente.")


def _save_product_structure(tx, code, name, components):
    statement = """
    MERGE (p:Product {code: $code})
    SET p.name = $name
    WITH p
    UNWIND $components AS component
    MERGE (m:Material {code: component.code})
    SET m.name = component.name
    MERGE (p)-[r:REQUIRES]->(m)
    SET r.quantity = component.quantity
    RETURN count(m) AS total_components
    """

    result = tx.run(
        statement,
        code=code,
        name=name,
        components=components
    )

    record = result.single()
    summary = result.consume()

    return (
        record["total_components"],
        summary.counters.nodes_created,
        summary.counters.relationships_created
    )


def save_product_structure(driver):
    with driver.session(database="neo4j") as session:
        return session.execute_write(
            _save_product_structure,
            "PC001",
            "Gaming PC",
            COMPONENTS
        )


def _calculate_material_requirements(tx, code, quantity):
    statement = """
    MATCH (p:Product {code: $code})
          -[r:REQUIRES]->
          (m:Material)
    RETURN m.name AS material_name,
           r.quantity * $quantity AS total_required
    ORDER BY material_name
    """

    result = tx.run(
        statement,
        code=code,
        quantity=quantity
    )

    return [row.data() for row in result]


def calculate_material_requirements(driver, product_code, quantity):
    with driver.session(database="neo4j") as session:
        return session.execute_read(
            _calculate_material_requirements,
            product_code,
            quantity
        )


def main():
    host = os.getenv("NEO4J_HOST", "localhost")
    port = os.getenv("NEO4J_PORT", "7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    quantity = int(os.getenv("ORDER_QUANTITY", "30"))

    connection_uri = f"bolt://{host}:{port}"

    with GraphDatabase.driver(
        connection_uri,
        auth=(user, password)
    ) as driver:

        driver.verify_connectivity()
        print("Conexión establecida con la base de datos Neo4j.")

        check_indexes(driver)
        test_create(driver)

        total, created_nodes, created_relations = save_product_structure(driver)

        print(f"Total de materiales relacionados: {total}")
        print(f"Nodos nuevos: {created_nodes}")
        print(f"Relaciones nuevas: {created_relations}")

        materials = calculate_material_requirements(
            driver,
            product_code="PC001",
            quantity=quantity
        )

        print(f"\nComponentes requeridos para fabricar {quantity} Gaming PC:")

        for material in materials:
            print(
                f"{material['material_name']}: "
                f"{material['total_required']}"
            )


if __name__ == "__main__":
    main()