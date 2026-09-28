# 💳 Lumi - Agente Financeira Inteligente (Cartões de Crédito)

Lumi é uma assistente virtual inteligente e proativa desenvolvida para o setor financeiro. O projeto resolve um dos momentos de maior atrito para os clientes: a contestação de compras, suspeita de fraudes e dúvidas sobre a fatura do cartão de crédito.

O agente utiliza a API do **Google Gemini (3.8 Flash)** combinada com uma interface web interativa construída em **Streamlit**, aplicando técnicas de **RAG (Geração Aumentada por Recuperação)** para acessar extratos, regras de negócio e limites de crédito em tempo real, sem alucinar valores ou expor dados sensíveis.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Streamlit** (Interface Web)
- **Google Generative AI** (LLM Gemini)
- **Pandas** (Manipulação de dados CSV)
- **Dotenv** (Gerenciamento de variáveis de ambiente)

---

## 📚 Documentação do Projeto

Todo o processo de ideação, arquitetura e testes estruturados foi documentado. Acesse os links abaixo para entender como a Lumi foi construída:

1. [Caso de Uso, Persona e Arquitetura](./docs/01-documentacao-agente.md)
2. [Estratégia da Base de Conhecimento e RAG](./docs/02-base-conhecimento.md)
3. [Engenharia de Prompts e Edge Cases](./docs/03-prompts.md)
4. [Avaliação e Métricas de Qualidade](./docs/04-metricas.md)
5. [Roteiro do Pitch](./docs/05-pitch.md)

---

## 🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e rodar a aplicação na sua máquina:

**1. Clone o repositório**
```bash
git clone [https://github.com/SEU_USUARIO/dio-lab-bia-do-futuro.git](https://github.com/SEU_USUARIO/dio-lab-bia-do-futuro.git)
cd dio-lab-bia-do-futuro
```

**2. Acesse a pasta do código-fonte e instale as dependências**
```bash
cd src
pip install -r requirements.txt
```

**3. Configure a Chave de API**
No arquivo chamado `.env.example` dentro da pasta `src/` adicione a sua chave do Google AI Studio. O conteúdo do arquivo deve ser exatamente este:
```env
GEMINI_API_KEY=sua_chave_aqui
```

**4. Execute a aplicação Streamlit**
Ainda dentro da pasta `src`, digite o comando abaixo no terminal:
```bash
streamlit run app.py
```

O navegador abrirá automaticamente a interface de chat da Lumi. Você pode testar interações como:
- *"Qual o valor da minha fatura atual e quanto tenho de limite?"*
- *"Tem uma compra de 1499 reais na minha fatura que eu não fiz!"*
- *"Quero cancelar um curso online de 299 reais que assinei ontem."*