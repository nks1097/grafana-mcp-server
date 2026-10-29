# Guia de Contribuição

Agradecemos o seu interesse em contribuir com o **Grafana MCP Server**!

## Diretrizes de Desenvolvimento

1. **Python 3.11+:** Utilize tipos estritos com Pydantic e tipagem estática do Python.
2. **Estilo de Código:** Utilize o `ruff` para formatação e linting:
   ```bash
   ruff check src tests
   ruff format src tests
   ```
3. **Nomes de Ferramentas:** Devem sempre ser em ASCII `snake_case`, com prefixo `grafana_`.
4. **Descrições:** Todas as descrições de ferramentas, parâmetros e mensagens de erro devem ser em português claro.
5. **Testes:** Qualquer nova funcionalidade deve vir acompanhada de testes unitários com mocks em `tests/unit`.
6. **Segurança:** Nunca comite tokens, senhas ou URLs internas de teste.

## Como Submeter Pull Requests

1. Faça um Fork do repositório.
2. Crie uma branch para sua funcionalidade: `git checkout -b feature/minha-feature`.
3. Certifique-se de que todos os testes passam: `pytest tests/unit -v`.
4. Faça commit com mensagens descritivas no padrão Conventional Commits.
5. Abra o Pull Request detalhando as alterações.
