# Case IA Alura (Feedbacks Alumind)

## ℹ️ Descrição do projeto:
- **Entidades mapeadas:**
    - `Feedback`: tem uma id, o feedback e o sentiment (classificação através de uma LLM)
    - `Feature codes`: tem uma id (auto incremento) e o nome do código que deve ser único (ex: EDITAR_PERFIL); Dessa forma, será necessário realizar agrupamentos. Por exemplo, toda vez que algum usuário sugerir a edição de perfil, o código deve ser o mesmo. Um novo código só é adicionado ao banco de dados se ainda não existir lá.
    - `Requested feature`: tem uma id (auto incremento), descrição da feature (através da LLM), data de criação, code_id (chave estrangeira) e feedback_id (chave estrangeira)

- **Essa é uma API REST que possui as seguintes features:**
    - `Endpoint HTTP POST /feedbacks`: Esse endpoint recebe uma id de 36 caracteres e um feedback de um usuário
        - Primeiramente, um filtro por spam é realizado utilizando uma LLM
        - Se o feedback for classificado como spam, será retornado ao cliente a id do feedback e o sentiment = SPAM
        - Se o feedback for classificado como legítimo, uma nova chamada à LLM é feita para que ela retorne o sentiment como POSITIVO, NEGATIVO ou INCONCLUSIVO, além de retornar possíveis melhorias sugeridas pelo usuário
        - Nesse caso, essas informações são adicionadas ao banco de dados
    - `Função weekly_summary()`: Essa função é chamada todas as sextas-feiras às 18h
        - Essa função é responsável pelo envio de um e-mail com informações dos feedbacks da última semana
    - `Página web`: Ao acessar http://127.0.0.1:5000, será possível visualizar as porcentagens de feedbacks ponitivos, negativos e inconclusivos e também as porcentagens de ocorrência de cada feature sugerida pelos usuários

## 💻 Tecnologias utilizadas:
- Python
- Flask
- LangChain
- Cohere (Modelo Command R Plus)
- MySQL
- Pytest

## 🛰 Como rodar o projeto:
- Primeiro, faça o clone do repositório
<pre>
  <code>git clone https://github.com/francinehahn/case-ia-alura.git</code>
</pre>

- Acesse a raiz do projeto
<pre>
  <code>cd case-ia-alura</code>
</pre>

- Crie um arquivo .env e preencha as seguintes informações:
`OBS: site da cohere para obter a chave de acesso gratuito https://dashboard.cohere.com/welcome/register`
<pre>
  <code>
    DB_HOST =  host do mysql
    DB_USER = user do mysql
    DB_PASSWORD = password do mysql
    DB_NAME = database name do mysql

    COHERE_API_KEY = api key da cohere

    MAIL_SERVER = server do email
    MAIL_USERNAME = endereço de email que será o remetente
    MAIL_PASSWORD = senha do email que será o remetente
    EMAIL_RECEIVERS = uma string com todos os endereços de e-mails que receberão so reports semanais. ex: "test@email.com,test2@email.com" - nesse caso é importante adicionar todos os emails separados por vírgulas e sem espaçamentos entre eles 
  </code>
</pre>

- Crie um ambiente virtual na raiz do projeto
<pre>
    <code>virtualenv venv</code>
</pre>

- Ative o ambiente virtual
<pre>
    <code>.\venv\Scripts\activate</code>
</pre>

- Instale as dependencias
<pre>
    <code>pip install -r requirements.txt</code>
</pre>

- Rode o arquivo migrations.py
    - Esse arquivo irá criar as tabelas no MySQL

- Rode o arquivo app.py
    - Esse arquivo irá rodar a API

`**Algumas observações**`
- Para testar o endpoint POST /feedbacks é só acessar o arquivo request.rest e clicar em send request
- Para acessar a página web, é só acessar http://127.0.0.1:5000
- Para testar o funcionamento da função weekly_summary, será necessário editar o scheduler no arquivo app.py (linha 91) para o dia e hora que desejar.
<pre>
    <code>
        scheduler.add_job(weekly_summary, 'cron', day_of_week='fri', hour=18, minute=00)
    </code>
</pre>
