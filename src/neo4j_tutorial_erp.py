import os

from neo4j import GraphDatabase


MATERIALS = [
    {"code": "CPU001", "name": "CPU Ryzen 7", "quantity": 1},
    {"code": "MB001", "name": "Motherboard B650", "quantity": 1},
    {"code": "RAM001", "name": "RAM 16GB DDR5", "quantity": 2},
    {"code": "SSD001", "name": "SSD 1TB NVMe", "quantity": 1},
    {"code": "PSU001", "name": "Power Supply 750W", "quantity": 1},
    {"code": "GPU001", "name": "Graphics Card RTX", "quantity": 1},
]


def create_bom_graph(driver):
    query = """
    MERGE (product:Product {code: $product_code})
    SET product.name = $product_name
    WITH product
    UNWIND $materials AS item
    MERGE (material:Material {code: item.code})
    SET material.name = item.name
    MERGE (product)-[requires:REQUIRES]->(material)
    SET requires.quantity = item.quantity
    RETURN count(material) AS components
    """
    records, summary, _ = driver.execute_query(
        query,
        product_code="PC001",
        product_name="Gaming PC",
        materials=MATERIALS,
        database_="neo4j",
    )
    return records[0]["components"], summary.counters


def get_required_materials(driver, product_code, order_quantity):
    query = """
    MATCH (product:Product {code: $product_code})
          -[requires:REQUIRES]->
          (material:Material)
    RETURN material.name AS material,
           requires.quantity * $order_quantity AS required
    ORDER BY material
    """
    records, _, _ = driver.execute_query(
        query,
        product_code=product_code,
        order_quantity=order_quantity,
        database_="neo4j",
    )

    return [record.data() for record in records]


def main():
    host = os.getenv("NEO4J_HOST", "localhost")
    port = os.getenv("NEO4J_PORT", "7687")
    username = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    order_quantity = int(os.getenv("ORDER_QUANTITY", "30"))

    uri = f"bolt://{host}:{port}"
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        driver.verify_connectivity()
        print("Conexión con Neo4j correcta.")

        component_count, counters = create_bom_graph(driver)
        print(f"Componentes relacionados: {component_count}")
        print(f"Nodos creados: {counters.nodes_created}")
        print(f"Relaciones creadas: {counters.relationships_created}")
        requirements = get_required_materials(
            driver,
            product_code="PC001",
            order_quantity=order_quantity,
        )
        print(f"\nMateriales necesarios para {order_quantity} Gaming PC:")
        for item in requirements:
            print(f"{item['material']}: {item['required']}")

if __name__ == "__main__":
    main()