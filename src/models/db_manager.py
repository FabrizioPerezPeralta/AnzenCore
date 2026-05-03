import psycopg2
import streamlit as st
from psycopg2.extras import RealDictCursor

class DBManager:
    def __init__(self):
        try:
            self.db_url = st.secrets["DB_URL"]
        except Exception:
            st.error("❌ Error: No se encontró la variable DB_URL en los Secrets.")
            st.stop()

    def ejecutar_query(self, query, params=None, es_select=False):
        resultado = None
        conn = None
        try:
            # Abrimos la conexión limpia
            conn = psycopg2.connect(self.db_url)
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if es_select:
                    resultado = cur.fetchall()
                conn.commit()
            return resultado
        except Exception as e:
            if conn: conn.rollback()
            st.error(f"⚠️ Error de base de datos: {e}")
            return None
        finally:
            # Cerramos la conexión para no saturar el pooler gratuito
            if conn:
                conn.close()