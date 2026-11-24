# Desafio de Engenharia de Dados da Refera

Este repositório reúne minha solução para o desafio proposto pela [Refera-Tech](https://github.com/Refera-Tech/refera-data-engineer-short-challenge), usando Python, PostgreSQL e a base de exemplo DVD Rental.

## Solução

Implementei um [script Python](app/pipeline.py) que copia as 15 tabelas da base DVD Rental para o PostgreSQL analítico. A carga é completa. A cada execução, o script substitui as tabelas no destino e confere a contagem de linhas antes de confirmar a operação.

## Como rodar

Copie `.env.example` para `.env` e preencha as duas variáveis com a senha de demonstração definida no Compose. Se os bancos já estiverem configurados, use as senhas atuais.

Na pasta do projeto, execute:

```bash
docker compose up -d
python -m pip install -r requirements.txt
```

Quando os dois bancos estiverem prontos, execute `python app/pipeline.py`. O script mostra quantas linhas foram copiadas por tabela.
