import psycopg2
import streamlit as st
from psycopg2.extras import RealDictCursor

class DBManager:
    def __init__(self):
        try:
            self.db_url = st.secrets["DB_URL"]
        except Exception:
            st.error("❌ Error: No se encontró DB_URL en los Secrets.")
            st.stop()

    def ejecutar_query(self, query, params=None, es_select=False):
        resultado = None
        conn = None
        try:
            # Abrimos la conexión justo antes de usarla
            conn = psycopg2.connect(self.db_url)
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if es_select:
                    resultado = cur.fetchall()
                conn.commit()
        except Exception as e:
            if conn: conn.rollback()
            st.error(f"Error técnico: {e}")
        finally:
            # CERRAMOS SIEMPRE (Obligatorio para el Pooler puerto 6543)
            if conn:
                conn.close()
        return resultado