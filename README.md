# 💧 WaterTimer — Backend

API REST desenvolvida para o **WaterTimer**, um projeto voltado ao acompanhamento e gerenciamento da hidratação diária dos usuários.

## 🚀 Tecnologias utilizadas

- **Python** — linguagem de programação.
- **FastAPI** — desenvolvimento da API REST.
- **SQLAlchemy** — ORM para comunicação com o banco de dados.
- **PostgreSQL** — banco de dados relacional.
- **Pydantic** — validação e estruturação dos dados.
- **JWT (JSON Web Token)** — autenticação baseada em tokens.
- **Passlib + Bcrypt** — criptografia e verificação de senhas.
- **Uvicorn** — servidor ASGI para execução da aplicação.

### Organização das responsabilidades

| Diretório | Responsabilidade |
|---|---|
| `database` | Configuração da conexão com o PostgreSQL e gerenciamento das sessões. |
| `models` | Definição das entidades e seus relacionamentos no banco de dados. |
| `routes` | Definição dos endpoints e recebimento das requisições HTTP. |
| `schemas` | Validação e estruturação dos dados utilizando Pydantic. |
| `services` | Implementação das regras de negócio e operações de persistência. |
| `utils` | Funções auxiliares, cálculo de metas e recursos de segurança. |

## ⚙️ Funcionalidades implementadas

### 1. Gerenciamento de usuários

- Cadastro de usuários.
- Consulta de todos os usuários cadastrados.
- Consulta de usuário por identificador.
- Atualização dos dados cadastrais.
- Exclusão de usuário.
- Validação de dados utilizando Pydantic.
- Armazenamento de senhas utilizando hash Bcrypt.

Os dados cadastrais incluem nome, e-mail, senha, idade, peso, horário de dormir, duração do sono e capacidade da garrafa.

### 2. Autenticação e segurança

O sistema utiliza autenticação baseada em JWT.

O processo de autenticação contempla:

1. Recebimento de e-mail e senha.
2. Busca do usuário no banco de dados.
3. Verificação da senha informada com o hash armazenado.
4. Geração de um token JWT em caso de autenticação válida.
5. Validação do token para identificar o usuário autenticado em operações protegidas.

O token possui tempo de expiração de **30 minutos** e utiliza o algoritmo HS256.

## 🔗 Endpoints da API

Os endpoints estão organizados em dois grupos principais: usuários e metas diárias.

### Usuários

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/usuarios` | Lista os usuários cadastrados. |
| GET | `/usuarios/{id_user}` | Busca um usuário pelo identificador. |
| POST | `/cadastrar` | Cadastra um novo usuário. |
| PUT | `/usuarios/{id_user}` | Atualiza os dados de um usuário autenticado. |
| DELETE | `/usuarios/{id_user}` | Exclui um usuário autenticado. |
| DELETE | `/usuarios` | Exclui todos os usuários cadastrados. |

### Autenticação

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/usuarios/login` | Realiza a autenticação e retorna um token JWT. |

O login utiliza formulário OAuth2 com os campos `username` (e-mail) e `password` (senha).

### Metas diárias

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/usuarios/metas` | Lista as metas cadastradas. |
| POST | `/cadastrar/{id_user}/meta` | Cadastra uma meta para um usuário. |
| PUT | `/usuarios/{id_user}/registro_hidratacao` | Registra o consumo de água. |
| DELETE | `/usuarios/{id_user}/meta` | Exclui a meta de um usuário. |
| DELETE | `/usuarios/metas` | Exclui todas as metas cadastradas. |

O registro de consumo recebe `ml_consumida` como parâmetro de consulta (query parameter).

## 🔒 Segurança

O backend implementa mecanismos de segurança, incluindo:

- Armazenamento de senhas utilizando hash Bcrypt.
- Autenticação baseada em JWT.
- Expiração de tokens de acesso.
- Validação de credenciais.
- Verificação de identidade do usuário em operações de atualização e exclusão individual.

## 📌 Observações

- O projeto possui uma implementação de lembretes de hidratação iniciada na estrutura de models e schemas, mas essa funcionalidade ainda não está implementada como recurso operacional da API.
- A configuração de conexão com o banco de dados é realizada por variáveis de ambiente.
- A aplicação possui configuração de CORS permitindo a origem `http://localhost:8080`.
- O projeto utiliza SQLAlchemy para operações com o banco de dados.

---

Desenvolvido como projeto de estudo e prática de desenvolvimento backend com Python, FastAPI e PostgreSQL.
