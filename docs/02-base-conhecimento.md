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
Os arquivos JSON e CSV estão armazenados na pasta `data/` do projeto. O aplicativo Streamlit (através do arquivo `app.py`) é responsável por ler esses arquivos utilizando a biblioteca `pandas` (para tabelas CSV) e o módulo nativo `json`. Os dados são armazenados em cache na memória (`@st.cache_data`) no início da execução da aplicação para garantir velocidade.

### Como os dados são usados no prompt?
Os dados lidos são convertidos em texto puro e injetados dinamicamente como uma string gigante formatada (Contexto de Dados) diretamente dentro do *System Prompt*. Dessa forma, antes mesmo da primeira mensagem do usuário, a API do Gemini já recebe todas as regras, o extrato e o perfil do cliente como base de conhecimento exclusiva para aquela sessão, impedindo que ela invente transações que não estão mapeadas ali.

---

## Exemplo de Contexto Montado

Quando o aplicativo Streamlit é iniciado, ele estrutura e envia o contexto para o agente da seguinte forma:

```text
[DADOS DO CLIENTE]
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "limite_total": 5000.00,
  "fatura_atual": 2643.80,
  "limite_disponivel": 2356.20,
  "vencimento_fatura": "2026-07-20"
}

[TRANSAÇÕES DA FATURA ATUAL]
data,descricao,categoria,valor,tipo
2026-07-01,Supermercado Central,alimentacao,450.00,saida
2026-07-03,Assinatura Netflix,lazer,55.90,saida
2026-07-10,ELETRO_SHOP*INTERNET,eletronicos,1499.00,saida
2026-07-11,Assinatura Curso Online,educacao,299.90,saida

[REGRAS DE NEGÓCIO DO BANCO]
- Cenário: Contestação por Fraude. Prazo de resolução: Estorno provisório em até 3 dias úteis. Ação: Bloqueio do cartão atual.