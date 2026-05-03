import psycopg2
import streamlit as st
from psycopg2.extras import RealDictCursor

class DBManager:
    def __init__(self):
        # Intentamos obtener la URL de los Secrets
        try:
            self.db_url = st.secrets["DB_URL"]
        except Exception:
            st.error("Falta la configuración de DB_URL en los Secrets de Streamlit.")
            st.stop()

    @st.cache_resource
    def _obtener_conexion(_self):
        # CRÍTICO: sslmode='require' es obligatorio para Supabase desde la nube
        return psycopg2.connect(_self.db_url, sslmode='require')

    def ejecutar_query(self, query, params=None, es_select=False):
        try:
            conn = self._obtener_conexion()
            
            # Si la conexión se cerró por tiempo de espera, la forzamos a reiniciar
            if conn.closed:
                st.cache_resource.clear()
                conn = self._obtener_conexion()

            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                resultado = cur.fetchall() if es_select else None
                conn.commit()
                return resultado
        except Exception as e:
            # Si hay un error de conexión, limpiamos la caché para que el próximo intento sea desde cero
            st.cache_resource.clear()
            st.error(f"Error de base de datos: {e}")
            return None