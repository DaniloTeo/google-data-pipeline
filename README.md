# [Projeto - Data Engineer - BI](https://www.notion.so/Projeto-Data-Engineer-BI-37f00ee7a9e14c308fed73cd2f86e07f)

## Descrição
Neste projeto você deverá construir um ETL que lê um conjunto de dados do Google Cloud Storage e os coloca no BigQuery . Faça uma análise exploratória em cima dos dados do BigQuery.

## Aprendizados
Todo o processo de desenvolvimento dessa visualização pode ser dividio em 3 principais etapas:
1. Obtenção, tratamento e carregamento dos dados (ETL);
2. Desenvolvimento da query no Bigquery que melhor fornecesse insights;
3. Montagem da Dashboard no Data Studio.

### ETL
O processo de ETL foi onde houve mais aprendizado, sem sombra de dúvidas. O primeiro obstáculo enfrentado foi a autenticação da aplicação desenvolvida. Com um pouco de pesquisa e leitura da documentação da SDK do Google Cloud, constatou-se a necessidade de rodar o comando `gcloud auth application-default login` que define as credenciais _default_ para qualquer aplicação que tente acessar recursos do Google Cloud Project.

O segundo obstáculo encontrado foi o formato dos dados. A princípio estava otimista sobre a compatibilidade dos arquivos para upload no Bigquery, portanto fiz um teste simples de carregamento para um tabela diretamente do Cloud Storage. Não é necessário explicar que houve um erro devido à incompatibilidade entre os dados fornecidos nos arquivos `.ndjson` e o esquema definido para a tabela.

Sendo assim, precisava baixar os dados do GCS(Google Cloud Storage) para que pudesse tratá-los e, somente então, carregá-los para uma tabela no BQ(Bigquery). O download dos dados foi feito através do envio de um comando ao terminal da máquina que faz a requisição dos dados em paralelo. A etapa de tratamento em si foi simples. Trocar `"null"` por `null` e eliminar o campo `unique_key` que não constava no esquema desejado. Também havia a necessidade de criar um campo referente à data somente, mas isso poderia ser feito no BQ, após o carregamento.

O requerimento era de um código que obtesse os dados de uma data específica. Contudo, acreditei ser mais explicativo, ao menos para a etapa de visualização. Fazer a concatenação dos diversos arquivos e manter o formato `ndjson` foi um aprendizado interessante.

### Bigquery
A etapa de desenvolvimento envolvendo o Bigquery já foi um tanto mais simples. O principal foco dessa etapa era gerar uma métrica, coisa que não existia no esquema dos dados. Sendo assim, foi criada a métrica `Total` que consiste, na verdade, na contagem dos dados dependendo de seu agrupamento, o que fornece o total de ocorrências por tipo, por local etc.

### Visualização no Data Studio
A dashboard desenvolvida contém 3 páginas cada uma com uma forma de visualização. A primeira página contém uma tabela exploratória simples com dimensões de tipo de ocorrência, endereço, mês e ano.

A segunda página contém dois gráficos afetados pelo mesmo filtro de período, permitindo verificar o total de ocorrências de um determinado tipo e em um determinado endereço, dado um período de tempo.

A última página apresenta a tentativa de uma visualização de um mapa de balões. Houve a tentativa de usar o valor da coluna `Location` do esquema da tabela, mas a interação com o Data Studio se mostrou falha. Não era possível mesmo diferenciar as cores de cada tipo de ocorrência pela necessidade de haver apenas um tipo por local(?). Assim, o resultado apresenta um mapa utilizando o endereço expandido (com cidade e estado) e filtros para Ano e tipo de Ocorrência.

### [Link para Dashboard no Data Studio](https://datastudio.google.com/reporting/a27ff67f-a546-43f5-9796-8a3ff8796ef4/page/1hUyB)
### Project Status: <span style="color: lightgreen">Completed<span>
