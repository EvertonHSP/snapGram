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

Atualmente, apenas o cadastro de usuários no banco de dados através da página **"Criar Conta"** está funcionando corretamente. Outras funcionalidades ainda estão sendo implementadas, porém há erros no acesso ao **perfil**, devido a problemas na lógica dos tokens. A correção está em andamento.  

A API do SnapGram gera um **token JWT** após o login/cadastro, enviado em formato JSON para o usuário. Esse token permite realizar requisições autenticadas enquanto estiver válido, possibilitando ações como:  

- Acessar o template de perfil  
- Comentar  
- Postar  
- Curtir  

O **token é temporário** e será excluído automaticamente ao sair da conta. Caso o usuário deseje reentrar, um novo token será gerado. Essa estratégia visa manter o **frontend e o backend independentes**.  

As rotas do backend **não redirecionam páginas**, apenas as servem. O cliente (frontend) será responsável por gerenciar a interface utilizando scripts, enviando requisições para:  

- **Manipular a página** (dados dinâmicos) !podem exigir autenticação dependendo da ação 
- **Carregar templates** (migração de páginas) !podem exigir autenticação dependendo da página

O backend responderá às requisições servindo páginas via **Routes** ou fornecendo dados através da **API RESTful**, exigindo autenticação conforme necessário.  

### **Funcionalidades em Desenvolvimento**  
✅ Cadastro de usuários (**funcional**)  
🚧 **Feed de postagens** (**implementando**)  
🚧 **Integração completa do token JWT** (**Problemas de lógica**)  
🚧 **acesso ao perfil** (**Inacessível por Problemas de lógica**)

🔄 **Curtidas e comentários** (**falta implementação**)  
🔄 **Gerenciamento de perfil** (**falta implementação**)  


---

## **2. Problemas Conhecidos**  

- **Token JWT**: Erros na integração para autenticação.  
- **perfil**: não acessível pelos erros na integração para autenticação.
- **Curtidas e Comentários**: Em desenvolvimento.  

---

## **3. Tecnologias Utilizadas**  

### **Backend**  
- **Python**  
- **Flask** (Framework web)  
- **Flask-SQLAlchemy** (ORM para banco de dados)  
- **Flask-JWT-Extended** (Autenticação com JWT)  
- **Flask-Bcrypt** (Criptografia de senhas)  
- **Flask-Migrate** (Gerenciamento de migrações do banco de dados)  
- **Flask-WTF** (Validação de formulários)  

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
git clone https://github.com/seu-usuario/SnapGram.git
cd SnapGram  
```  

#### **2. Crie um Ambiente Virtual**  
```bash  
python -m venv venv  
source venv/bin/activate  # No Windows: venv\Scripts\activate  
```  

#### **3. Instale as Dependências**  
```bash  
pip install -r requirements.txt  
```  

#### **4. Inicialize o Banco de Dados**  
```bash  
flask db init  
flask db migrate  
flask db upgrade  
```  

#### **5. Execute o Servidor**  
```bash  
python main.py  
```  

#### **6. Acesse o SnapGram**  
Abra o navegador e acesse:  
```  
http://127.0.0.1:5000  
```  
O perfil ainda está sofrendo com a lógica errada do token, então você ainda não vai conseguir acessa-lo, porém o criar conta funciona, então a api consegue registrar você, o script então chama a rota do feed, que é uma rota pública
