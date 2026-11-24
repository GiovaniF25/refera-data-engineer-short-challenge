import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import Text, create_engine, func, inspect, select, table
from sqlalchemy.dialects.postgresql import DOMAIN, ENUM
from sqlalchemy.engine import URL


def database_url(prefix, database, default_port):
    password_key = f"{prefix}_DB_PASSWORD"
    password = os.getenv(password_key)
    if not password:
        raise RuntimeError(f"Configure {password_key} no arquivo .env.")

    return URL.create(
        "postgresql+psycopg2",
        username="postgres",
        password=password,
        host=os.getenv(f"{prefix}_DB_HOST", "localhost"),
        port=int(os.getenv(f"{prefix}_DB_PORT", default_port)),
        database=database,
    )


def load_tables(source, destination):
    schema = "public"
    inspector = inspect(source)
    tables = inspector.get_table_names(schema=schema)
    if not tables:
        raise RuntimeError("Nenhuma tabela encontrada no banco de origem.")

    row_counts = {}
    for table_name in tables:
        column_types = {}
        for column in inspector.get_columns(table_name, schema=schema):
            column_type = column["type"]
            if isinstance(column_type, DOMAIN):
                column_type = column_type.data_type
            if isinstance(column_type, ENUM):
                column_type = Text()
            column_types[column["name"]] = column_type

        data = pd.read_sql_table(table_name, source, schema=schema, coerce_float=False)
        data.to_sql(
            table_name,
            destination,
            schema=schema,
            if_exists="replace",
            index=False,
            dtype=column_types,
        )
        destination_table = table(table_name, schema=schema)
        count_query = select(func.count()).select_from(destination_table)
        destination_count = destination.execute(count_query).scalar_one()
        if destination_count != len(data):
            raise RuntimeError(
                f"{schema}.{table_name}: {len(data)} linhas lidas, "
                f"{destination_count} linhas no destino."
            )
        row_counts[table_name] = destination_count

    return row_counts


def main():
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    source_engine = create_engine(
        database_url("TRANSACTIONAL", "dvdrental", 5432),
        isolation_level="REPEATABLE READ",
    )
    destination_engine = create_engine(
        database_url("ANALYTICS", "analytics", 5440),
    )
    # A carga só é confirmada após validar todas as contagens.
    with source_engine.begin() as source, destination_engine.begin() as destination:
        row_counts = load_tables(source, destination)

    for table, count in row_counts.items():
        print(f"{table}: {count} linhas copiadas")
    print(f"Carga concluída: {len(row_counts)} tabelas.")


if __name__ == "__main__":
    main()
