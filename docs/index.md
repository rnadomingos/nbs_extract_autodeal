# Extrator NBS ➡️ Postgres Autodeal

Esta é a documentação do Extrator de dados do NBS para um banco de dados intermediário do Postgres, onde outra aplicação irá consumir estes dados e enviar para o AWS da Autodeal (Sistema de gerenciamento de garantias enviadas para a montadora BMW).

### Fluxo do Processo: 
```mermaid
flowchart TD
    A[Parametrizar conexão com NBS] --> B[Ler dados do NBS e retornar em DataFrame];
    B --> V[Validação do Schema de Entrada];
    V -->|Falha| X[Alerta de Erro];
    V -->|Sucesso| Y[Validar dados de saida - Pandas DataFrame];
    Y -->|Falha| Z[Alerta de Erro];
    Y -->|Sucesso| E[Adicionar testes unitarios se possivel];
    E --> F[Salvar dados no Postgres];
```
### Diagrama explicativo:

```mermaid
classDiagram
    class Base {
        <<abstract>>
        +id: int
    }

    class OSCapaModel {
        +cod_empresa: int
        +numero_os: int
        +...
    }

    class OSDetalheModel {
        +cod_empresa: int
        +numero_item: int
        +...
    }

    class load_to_db {
        +data_frame: DataFrameModel
        +data_model: Type[T]
        +load_to_db()
    }

    Base <|-- OSCapaModel
    Base <|-- OSDetalheModel
    load_to_db ..> Base : Usa modelos que herdam
    load_to_db --> OSCapaModel : Pode receber
    load_to_db --> OSDetalheModel : Pode receber
```    
## Extract Transform Load (etl.py)
::: app.etl.ExtractTransformLoad

## Schema OS Capa
::: app.data.schemas.schema_os_capa.OSCapaSchema