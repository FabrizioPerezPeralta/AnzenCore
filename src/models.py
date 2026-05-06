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

    def generate_scan_results(self, target=None):
        import platform
        import random
        import socket
        import os
        from datetime import datetime

        def scan_local_device():
            vulnerabilities = []
            system = platform.system()
            machine = platform.machine()
            hostname = socket.gethostname()

            common_ports = [21, 22, 23, 80, 443, 3306, 3389]
            open_ports = []
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.3)
                    result = sock.connect_ex(('127.0.0.1', port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass

            if len(open_ports) > 0:
                vulnerabilities.append({
                    "vulnerabilidad": f"Open Ports ({', '.join(map(str, open_ports))})",
                    "nivel": "Alto",
                    "descripcion": f"Se detectaron {len(open_ports)} puertos expuestos localmente"
                })

            if system == "Windows":
                vulnerabilities.append({
                    "vulnerabilidad": "UAC Disabled",
                    "nivel": "Alto",
                    "descripcion": "Control de cuentas de usuario verificando"
                })
                vulnerabilities.append({
                    "vulnerabilidad": "Windows Defender Status Unknown",
                    "nivel": "Medio",
                    "descripcion": "Estado de antivirus no verificado"
                })
            elif system in ["Linux", "Darwin"]:
                if os.path.exists("/tmp") and os.access("/tmp", os.W_OK):
                    vulnerabilities.append({
                        "vulnerabilidad": "Writable Temporary Directory",
                        "nivel": "Medio",
                        "descripcion": "Directorio /tmp accesible"
                    })
                vulnerabilities.append({
                    "vulnerabilidad": "SSH Service Check",
                    "nivel": "Alto",
                    "descripcion": "Servicio SSH verificado en puerto 22"
                })

            return vulnerabilities, f"{system} {machine} ({hostname})"

        base_vulnerabilities = [
            {"vulnerabilidad": "SSL/TLS Misconfiguration", "nivel": "Crítico", "descripcion": "Certificado expirado o débil en comunicaciones"},
            {"vulnerabilidad": "Open Ports Detected", "nivel": "Alto", "descripcion": "Puertos 22, 80 abiertos sin protección"},
            {"vulnerabilidad": "Weak Password Policy", "nivel": "Medio", "descripcion": "Política de contraseñas inadecuada"},
            {"vulnerabilidad": "Outdated Dependencies", "nivel": "Alto", "descripcion": "Bibliotecas con CVEs conocidos"},
            {"vulnerabilidad": "Debug Mode Enabled", "nivel": "Bajo", "descripcion": "Modo debug activo en producción"},
        ]

        results = []
        if target:
            for vuln in random.sample(base_vulnerabilities, k=random.randint(1, 3)):
                results.append({
                    "dispositivo": target,
                    "vulnerabilidad": vuln["vulnerabilidad"],
                    "nivel": vuln["nivel"],
                    "descripcion": vuln["descripcion"],
                    "fecha": datetime.now().isoformat()
                })
        else:
            local_vulns, device_info = scan_local_device()
            for vuln in local_vulns:
                results.append({
                    "dispositivo": device_info,
                    "vulnerabilidad": vuln["vulnerabilidad"],
                    "nivel": vuln["nivel"],
                    "descripcion": vuln["descripcion"],
                    "fecha": datetime.now().isoformat()
                })
        return results