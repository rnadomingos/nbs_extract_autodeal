from main.usecases.destination.load_max_date_column import LoadMaxDateColumn
from main.usecases.transformation.format_column import FormatColumn
from main.usecases.destination.upsert_data import UpsertData
from main.usecases.source.extract_data import ExtractData
from data.models.os_capa_model import OSCapaModel
from data.schemas.os_capa_schema import OSCapaSchema
from data.sql.os_capa_sql import stmt_os_capa


class OSCapaController:
    def daily_update(self):
        # Verificar a maior data inserida na tabela de destino da OSCapa
        max_date_os_capa = LoadMaxDateColumn().load(
            date_column=OSCapaModel.data_emissao
            )
        extractData = ExtractData(
            query=stmt_os_capa, 
            query_params=max_date_os_capa,
            schema=OSCapaSchema, #type: ignore
            lazy=True
            )
        data_frame_os_capa = extractData.get_data_nbs()
        data_frame_os_capa = FormatColumn().formatDatetime(
            df=data_frame_os_capa
            )
        upsert_os_capa = UpsertData(
            data_frame=data_frame_os_capa,
            data_model=OSCapaModel,
            conflict_keys=['cod_empresa', 'numero_os']
        )
        saved_os_capa = upsert_os_capa.save_data()
        return len(saved_os_capa)