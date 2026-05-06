from datetime import datetime, timedelta

class AnzenController:
    def __init__(self, model):
        self.model = model

    def login(self, username, password):
        res = self.model.authenticate(username, password)
        return res.data[0] if res.data else None

    def signup(self, username, password):
        try:
            self.model.register(username, password)
            return True
        except:
            return False

    def fetch_online_list(self):
        # Umbral de 30 segundos para considerar online
        umbral = (datetime.now() - timedelta(seconds=30)).isoformat()
        res = self.model.get_online_users(umbral)
        return res.data

    def fetch_all_reports(self):
        res = self.model.get_vulnerabilities()
        return res.data

    def scan_vulnerabilities(self, target=None):
        return self.model.generate_scan_results(target)