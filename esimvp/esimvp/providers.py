import csv
from esi.clients import EsiClientProvider


class EVEClient(EsiClientProvider):
    """
        Our custom ESI provider
    """
    
    def get_status(self):
        return self.client.Status.get_status().results()

esi = EVEClient()
