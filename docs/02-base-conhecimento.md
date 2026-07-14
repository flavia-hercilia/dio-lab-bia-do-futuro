# Base de Conhecimento

## Dados Utilizados

Os arquivos de dados foram totalmente reestruturados para refletir o cenário de suporte a cartões de crédito e contestação de faturas, garantindo consistência técnica entre os valores da fatura e o histórico de compras.

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_cliente.json` | JSON | Personalizar interação com o cliente |
| `regras_cartao.json` | JSON | Consultar regras operacionais do banco |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente |

---

## Adaptações nos Dados

Os dados originais voltados para investimentos foram adaptados para o ecossistema de cartões de crédito:

- **`transacoes.csv`:** Foram incluídas transações estratégicas para testes de fluxo -> uma compra suspeita de fraude (`ELETRO_SHOP*INTERNET` de R$ 1499,00) e uma compra online dentro do prazo de arrependimento de 7 dias (`Assinatura Curso Online` de R$ 299,90).
- **`perfil_cliente.json`:** Substituiu o perfil de investimentos anterior. Agora centraliza o limite total, a fatura atual e o limite disponível.
- **`regras_cartao.json`:** Arquivo totalmente novo que substituiu o catálogo de investimentos (`produtos_financeiros.json`), servindo como a referência de regras operacionais que a Lumi deve seguir.

---

## Estratégia de Integração

### Como os dados são carregados?
Os arquivos JSON e CSV estão armazenados na pasta `data` do projeto dentro do workspace da IDE **Antigravity**. O ambiente gerencia o escopo desses arquivos automaticamente, permitindo que o modelo Gemini os acesse como uma base de dados local associada ao agente.

### Como os dados são usados no prompt?
Os dados não são injetados de forma estática no System Prompt. Em vez disso, o agente utiliza a capacidade de RAG (Geração Aumentada por Recuperação) nativa do Antigravity. Ao receber uma pergunta do usuário (ex: *"Qual é o meu limite?"*), a Lumi faz uma varredura dinâmica no arquivo `perfil_cliente.json` para extrair a informação correta em tempo de execução, evitando alucinações de valores.

---

## Exemplo de Contexto Montado

Quando o usuário inicia uma interação, o Antigravity disponibiliza o contexto estruturado para o agente da seguinte forma:

```text
[PERFIL_CLIENTE]
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "limite_total": 5000.00,
  "fatura_atual": 2643.80,
  "limite_disponivel": 2356.20,
  "vencimento_fatura": "2026-07-20"
}

[ULTIMAS_TRANSACOES_RELEVANTES]
- 2026-07-01: Supermercado Central - R$ 450.00 (alimentacao)
- 2026-07-03: Assinatura Netflix - R$ 55.90 (lazer)
- 2026-07-10: ELETRO_SHOP*INTERNET - R$ 1499.00 (eletronicos)
- 2026-07-11: Assinatura Curso Online - R$ 299.90 (educacao)

[DIRETRIZ_DE_NEGOCIO_APLICAVEL]
- Cenário: Contestação por Fraude. Prazo de resolução: Estorno provisório em até 3 dias úteis. Ação: Bloqueio do cartão atual.
