import pandera as pa
from app.etl import ExtractTransformLoad
from data.sql.os_capa_sql import stmt_os_capa

controller = ExtractTransformLoad()
df_os_capa = controller.extract_sql(stmt_os_capa)


schema_os_capa = pa.infer_schema(df_os_capa)

path_schema = 'app/data/schemas/'

with open(f'{path_schema}schema_os_capa.py', 'w', encoding='utf-8') as file:
  file.write(str(schema_os_capa.to_script()))

print(schema_os_capa)

