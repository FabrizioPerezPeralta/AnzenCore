from supabase import create_client
import streamlit as st

class AnzenModel:
    def __init__(self):
        self.supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

    def authenticate(self, user, pw):
        return self.supabase.table("usuarios").select("*").eq("username", user).eq("password", pw).execute()

    def register(self, user, pw):
        return self.supabase.table("usuarios").insert({"username": user, "password": pw}).execute()

    def update_ping(self, user_id):
        return self.supabase.table("usuarios").update({"last_ping": "now()"}).eq("id", user_id).execute()

    def get_online_users(self, time_limit):
        return self.supabase.table("usuarios").select("username").gt("last_ping", time_limit).execute()

    def get_vulnerabilities(self):
        return self.supabase.table("vulnerabilidades").select("*").order("fecha", desc=True).execute()