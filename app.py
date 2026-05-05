import streamlit as st
from streamlit_autorefresh import st_autorefresh
from src.models import AnzenModel
from src.controllers import AnzenController
from src.views import AnzenView

st.set_page_config(page_title="AnzenCore", page_icon="🛡️", layout="wide")

if 'model' not in st.session_state:
    st.session_state.model = AnzenModel()
    st.session_state.controller = AnzenController(st.session_state.model)
    st.session_state.view = AnzenView()

m = st.session_state.model
c = st.session_state.controller
v = st.session_state.view

def main():
    if 'user' not in st.session_state:
        u, p, b, ru, rp, rb = v.render_login()
        if b:
            user = c.login(u, p)
            if user:
                st.session_state.user = user
                st.rerun()
            else: st.error("Credenciales incorrectas.")
        if rb:
            if ru and rp:
                if c.signup(ru, rp): st.success("✅ Registrado. Ingrese ahora.")
                else: st.error("❌ El usuario ya existe.")
    else:
        st_autorefresh(interval=5000, key="refresh_dashboard")
        m.update_ping(st.session_state.user['id'])
        
        # OBTENCIÓN DE DATOS (Nombres sincronizados con controllers.py)
        online_users = c.fetch_online_list()
        reports = c.fetch_all_reports()
        
        # SIDEBAR
        st.sidebar.title(f"👤 {st.session_state.user['username']}")
        st.sidebar.info(f"🔑 **ID:** `{st.session_state.user['id']}`")
        if st.sidebar.button("Cerrar Sesión"):
            del st.session_state.user
            st.rerun()
            
        v.render_dashboard(st.session_state.user, online_users, reports)

if __name__ == "__main__":
    main()