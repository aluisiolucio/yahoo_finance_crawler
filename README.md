# Yahoo Finance Crawler

Este projeto é um web crawler que coleta dados financeiros da Yahoo Finance, filtrando ações de acordo com a região fornecida pelo usuário. Utilizando `Selenium` e `BeautifulSoup` para web scraping e `Poetry` para gerenciamento de dependências, o crawler extrai informações como nome, símbolo e preço das ações, e as salva em um arquivo CSV.

## Requisitos

- **Python** 3.12 ou superior
- **Poetry** para gerenciamento de dependências
- **ChromeDriver** (instalado automaticamente pelo script com `webdriver_manager`)

## Instalação

1. **Clone o repositório**

   ```bash
   git clone https://github.com/aluisiolucio/yahoo_finance_crawler.git
   cd yahoo_finance_crawler
   ```

2. **Instale o Poetry**

   Caso ainda não tenha o Poetry instalado, siga as instruções oficiais [aqui](https://python-poetry.org/docs/#installation).

3. **Instale as dependências do projeto**

   Com o Poetry instalado, execute:

   ```bash
   poetry install
   ```

   Isso instalará todas as dependências, incluindo `Selenium`, `BeautifulSoup`, `webdriver_manager`, e outras bibliotecas necessárias.

## Estrutura do Projeto

```plaintext
yahoo_finance_crawler/
│
├── yahoo_finance_crawler/
│   ├── crawler.py              # Classe principal para execução do crawler
│   ├── selenium_scraper.py     # Classe que realiza o scraping usando Selenium
│   ├── data_processor.py       # Classe que processa e extrai os dados HTML
│   ├── csv_exporter.py         # Classe para exportar os dados para CSV
│   └── utils.py                # Funções utilitárias
│
├── tests/                          # Pasta para testes unitários
│   ├── test_crawler.py             # Testes para a classe principal
│   ├── test_selenium_scraper.py    # Testes para SeleniumScraper
│   └── test_data_processor.py      # Testes para DataProcessor
│
├── pyproject.toml              # Arquivo de configuração do Poetry
└── README.md                   # Documentação do projeto
```

## Uso

Para rodar o crawler e salvar os dados em um arquivo CSV:

1. **Inicie o ambiente virtual do Poetry**

   ```bash
   poetry shell
   ```

2. **Execute o crawler**

   Para buscar ações em uma região específica, como Argentina, execute:

   ```bash
   python yahoo_finance_crawler/main.py "Argentina"
   ```

   Após a execução, o arquivo `yahoo_finance_data.csv` será gerado na pasta raiz do projeto, contendo os dados coletados.

### Parâmetros

- `region` - Filtro da região para o crawler. O crawler buscará apenas ações associadas à região especificada.

## Testes

O projeto utiliza **pytest** para os testes unitários. Para rodar os testes:

```bash
poetry run pytest
```

Isso executará todos os testes dentro da pasta `tests/` e exibirá o resultado no terminal.

## Implementação

O projeto utiliza uma arquitetura orientada a objetos com classes separadas para cada responsabilidade:

- **YahooFinanceCrawler**: Controla o fluxo do processo de scraping.
- **SeleniumScraper**: Realiza o scraping da página usando Selenium, aplicando os filtros de região e carregando o HTML necessário.
- **DataProcessor**: Processa o HTML carregado, extrai os dados da tabela, usando BeautifulSoup e formata em dicionários.
- **CSVExporter**: Salva os dados extraídos em um arquivo CSV.

## Contribuição

Contribuições são bem-vindas! Se você deseja melhorar o projeto, siga estes passos:

1. Fork o repositório.
2. Crie uma branch com a nova funcionalidade (`git checkout -b feature/nova-funcionalidade`).
3. Faça commit das alterações (`git commit -m 'Adicionei nova funcionalidade'`).
4. Envie para o repositório remoto (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

## Licença

Este projeto é licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.