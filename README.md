# Desafio de Engenharia de Dados da Refera

Este repositório reúne minha solução para o desafio proposto pela [Refera-Tech](https://github.com/Refera-Tech/refera-data-engineer-short-challenge), usando Python, PostgreSQL e a base de exemplo DVD Rental.

## Solução

Implementei um [script Python](app/pipeline.py) que copia as 15 tabelas da base DVD Rental para o PostgreSQL analítico. A carga é completa. A cada execução, o script substitui as tabelas no destino e confere a contagem de linhas antes de confirmar a operação.
