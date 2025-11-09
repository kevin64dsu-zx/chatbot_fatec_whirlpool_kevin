import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

def connect_db():
    """Conecta ao banco de dados MySQL usando variáveis do .env."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=os.getenv("MYSQL_PORT"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        if conn.is_connected():
            print("✅ Conectado ao banco MySQL com sucesso!")
            return conn
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return None


def log_message(role, content):
    """Registra uma mensagem no histórico."""
    conn = connect_db()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # Cria tabela caso ainda não exista (estrutura antiga)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                role VARCHAR(50),
                content TEXT
            )
            """
        )

        # Insere dados nas colunas corretas (role/content)
        cursor.execute(
            "INSERT INTO chat_history (role, content) VALUES (%s, %s)",
            (role, content)
        )
        conn.commit()
        print("💾 Mensagem registrada com sucesso!")
        return True
    except Error as e:
        print(f"Erro ao registrar mensagem: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def get_history():
    """Busca o histórico completo de mensagens."""
    conn = connect_db()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT role, content, timestamp FROM chat_history ORDER BY id ASC")
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Erro ao buscar histórico: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def clear_history():
    """Apaga todas as mensagens do histórico."""
    conn = connect_db()
    if conn is None:
        print("⚠️ Erro: não foi possível conectar ao banco para limpar histórico.")
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM chat_history")
        conn.commit()
        print("🧹 Histórico apagado com sucesso!")
        return True
    except Error as e:
        print(f"Erro ao apagar histórico: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
