# **SnapGram**  

O **SnapGram** é uma plataforma de rede social desenvolvida para conectar pessoas e permitir o compartilhamento de fotos e interações por meio de postagens, curtidas e comentários.  

## **Sumário**  
1. [Status do Projeto](#status-do-projeto)  
2. [Problemas Conhecidos](#problemas-conhecidos)  
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)  
4. [Como Executar o Projeto](#como-executar-o-projeto)  

---

## **1. Status do Projeto**  

### 🚧 Em Desenvolvimento 🚧  

Atualmente, todas as paginas e rotas ja estão em funcionamento, você roda a api, depois você tem que selecionar algum html para abrir no navegador(o javaScript do perfil.js e feed.js te rerediciona para a tela de login caso não tenha o token de autenticação). Depois a API do SnapGram gera um **token JWT** após o login/cadastro, enviado em formato JSON para o usuário. Esse token permite realizar requisições autenticadas enquanto estiver válido, possibilitando ações como:  

- Acessar o html de perfil
- Comentar  
- Postar  
- Curtir  

O **token é temporário** e será excluído automaticamente ao sair da conta. Caso o usuário deseje reentrar, um novo token será gerado. Essa estratégia visa manter o **frontend e o backend independentes**.  


## **3. Tecnologias Utilizadas**  

### **Backend**  
- **Python**  
- **Flask** (Framework web)  
- **Flask-SQLAlchemy** (ORM para banco de dados)  
- **Flask-JWT-Extended** (Autenticação com JWT)  
- **Flask-Bcrypt** (Criptografia de senhas)  
- **Flask-Migrate** (Gerenciamento de migrações do banco de dados) 
- **Flask-Restful** (Controle de requisições) 

### **Frontend**  
- **HTML/CSS**  
- **JavaScript**  

### **Banco de Dados**  
- **SQLite** (inicialmente, com migração futura para **PostgreSQL**)  

---

## **4. Como Executar o Projeto**  

### **Pré-requisitos**  
Antes de iniciar, certifique-se de ter instalado:  
- **Python 3.8** ou superior  
- **Git** (opcional, para clonar o repositório)  

### **Passos para Execução**  

#### **1. Clone o Repositório**  
```bash  
git clone https://github.com/EvertonHSP/snapGram.git
cd snapGram  
```  

#### **2. Crie um Ambiente Virtual**  
```bash  
python -m venv venv  
venv\Scripts\activate  # No linux: source venv/bin/activate  
```  

#### **3. Instale as Dependências**  
```bash  
pip install -r requirements.txt  
```  

#### **4. Inicialize o Banco de Dados**  
Não é nescessário, pois o app.py já faz isso automaticamente.
```bash  
flask db init  
flask db migrate  
flask db upgrade  
```  

#### **5. Execute o Servidor**  
```bash  
python app.py  
```  

#### **6. Acesse o SnapGram**  
Na pasta **frontend** abra o arquivo homepage.html ou criarconta.html no navegador manualmente

