from docusign_esign import EnvelopesApi
from example_base import ExampleBase

import os


class Envelope(ExampleBase):
    def get_document(self, document_id, envelope_id):
        self.check_token()

        envelope_api = EnvelopesApi(Envelope.api_client)
        document = envelope_api.get_document(Envelope.accountID, document_id, envelope_id, certificate=False)
        os.rename(document, '/home/phamvantoanb/Workspaces/sun/python/nicigas/' + Envelope.accountID + "-" + envelope_id
                  + "-" + document_id + '.pdf')
