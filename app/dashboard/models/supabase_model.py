from datetime import datetime, timezone
from hashlib import sha256

from supabase import create_client

from app.dashboard.config.settings import get_supabase_settings


class SupabaseModel:
    def __init__(self):
        settings = get_supabase_settings()
        self.supabase = create_client(settings["url"], settings["key"])

    @staticmethod
    def _hash_password(password: str) -> str:
        """Return the SHA-256 hex digest of the password."""
        return sha256(password.encode()).hexdigest()

    def authenticate(self, username, password):
        hashed = self._hash_password(password)
        return (
            self.supabase.table("usuarios")
            .select("*")
            .eq("username", username)
            .eq("password", hashed)
            .execute()
        )

    def user_exists(self, username):
        return (
            self.supabase.table("usuarios")
            .select("id")
            .eq("username", username)
            .limit(1)
            .execute()
        )

    def register(self, username, password):
        hashed = self._hash_password(password)
        return (
            self.supabase.table("usuarios")
            .insert({"username": username, "password": hashed})
            .execute()
        )

    def update_ping(self, user_id):
        return (
            self.supabase.table("usuarios")
            .update({"last_ping": datetime.now(timezone.utc).isoformat()})
            .eq("id", user_id)
            .execute()
        )

    def get_online_users(self, time_limit):
        return (
            self.supabase.table("usuarios")
            .select("username")
            .gt("last_ping", time_limit)
            .execute()
        )

    def get_vulnerabilities(self):
        return (
            self.supabase.table("vulnerabilidades")
            .select("*")
            .order("fecha", desc=True)
            .execute()
        )

    def get_apk_scans(self):
        return (
            self.supabase.table("apk_scan_summary")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

    def create_apk_scan(self, payload):
        return self.supabase.table("apk_scans").insert(payload).execute()

    def update_apk_scan(self, scan_id, payload):
        return (
            self.supabase.table("apk_scans")
            .update(payload)
            .eq("id", scan_id)
            .execute()
        )

    def get_apk_findings(self, scan_id):
        return (
            self.supabase.table("apk_findings")
            .select("*")
            .eq("scan_id", scan_id)
            .order("severity", desc=True)
            .execute()
        )

    def get_apk_artifacts(self, scan_id):
        return (
            self.supabase.table("apk_artifacts")
            .select("*")
            .eq("scan_id", scan_id)
            .order("artifact_type")
            .execute()
        )

    def create_apk_findings(self, findings):
        if not findings:
            return None
        return self.supabase.table("apk_findings").insert(findings).execute()

    def create_apk_artifacts(self, artifacts):
        if not artifacts:
            return None
        return self.supabase.table("apk_artifacts").insert(artifacts).execute()

    def create_report_export(self, payload):
        return self.supabase.table("report_exports").insert(payload).execute()
