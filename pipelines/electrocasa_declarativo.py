from pyspark import pipelines as dp
from pyspark.sql.functions import count


@dp.materialized_view(
    name="electrocasa_catalogo_validado",
    comment="Catalogo Silver validado por Lakeflow Declarative Pipelines",
)
@dp.expect_or_drop(
    "producto_id_obligatorio",
    "producto_id IS NOT NULL AND TRIM(producto_id) <> ''",
)
@dp.expect_or_drop(
    "categoria_obligatoria",
    "categoria IS NOT NULL AND TRIM(categoria) <> ''",
)
def electrocasa_catalogo_validado():
    return spark.read.table("proyecto_final.silver.catalogo")


@dp.materialized_view(
    name="electrocasa_productos_por_categoria",
    comment="Productos validos agrupados por categoria normalizada",
)
def electrocasa_productos_por_categoria():
    return (
        spark.read.table("electrocasa_catalogo_validado")
        .groupBy("categoria")
        .agg(count("*").alias("total_productos"))
    )
