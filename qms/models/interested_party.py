from datetime import date

from odoo import api, fields, models


class InterestedParty(models.Model):
    _name = "qms.interested_party"
    _description = "Interested Party"

    power = fields.Selection(
        selection=[
            ("1", "Low"),
            ("2", "Medium"),
            ("3", "High"),
            ("4", "Very High"),
        ],
        required=False,
    )

    interest = fields.Selection(
        selection=[
            ("1", "Low"),
            ("2", "Medium"),
            ("3", "High"),
            ("4", "Very High"),
        ],
        required=False,
    )

    cooperation = fields.Selection(
        selection=[
            ("1", "Low"),
            ("2", "Medium"),
            ("3", "High"),
            ("4", "Very High"),
        ],
        required=False,
    )

    impact = fields.Selection(
        selection=[
            ("1", "Low"),
            ("2", "Medium"),
            ("3", "High"),
            ("4", "Very High"),
        ],
        required=False,
    )

    name = fields.Char(required=True)

    interested_party_type = fields.Selection(
        selection=[
            ("internal", "Internal"),
            ("external", "External"),
        ]
    )

    is_organization = fields.Boolean()

    organization_id = fields.Many2one(
        comodel_name="qms.interested_party",
        domain=[("is_organization", "=", True)],
        ondelete="set null",
    )

    requeriments_interested_party = fields.Html()

    interest_tmc = fields.Html()

    area = fields.Char()

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="responsible_id"
    )

    last_review_date = fields.Date(compute="_compute_last_review_date")

    @api.depends("review_ids.date")
    def _compute_last_review_date(self):
        for interested_party in self:
            if interested_party.review_ids:
                # Fallback date: an undated review must not break the sort
                last_review = interested_party.review_ids.sorted(
                    key=lambda r: r.date or date.min, reverse=True
                )
                interested_party.last_review_date = last_review[0].date
            else:
                interested_party.last_review_date = False
