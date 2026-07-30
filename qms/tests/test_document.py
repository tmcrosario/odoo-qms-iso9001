from datetime import date

from odoo.tests import common


class TestDocument(common.TransactionCase):
    def _document_with_party(self):
        party = self.env["qms.interested_party"].create({"name": "Party"})
        component = self.env["qms.policy_component"].create({"name": "Component"})
        process = self.env["qms.process"].create(
            {
                "name": "Process",
                "responsible_id": party.id,
                "policy_component_ids": [(6, 0, component.ids)],
            }
        )
        document = self.env["qms.document"].create(
            {
                "identification": "DOC-1",
                "name": "Test Document",
                "responsible_id": party.id,
                "process_ids": [(6, 0, process.ids)],
            }
        )
        return document, party

    def test_last_review_date_ignores_undated_review(self):
        # An undated review must not crash the sorted() in the compute
        document, party = self._document_with_party()
        self.env["qms.review"].create(
            [
                {
                    "name": "Dated",
                    "responsible_id": party.id,
                    "document_id": document.id,
                    "date": "2020-06-01",
                },
                {
                    "name": "Undated",
                    "responsible_id": party.id,
                    "document_id": document.id,
                },
            ]
        )
        self.assertEqual(document.last_review_date, date(2020, 6, 1))
