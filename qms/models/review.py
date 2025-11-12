from odoo import fields, models


class Review(models.Model):

    _name = "qms.review"
    _description = "Review"

    name = fields.Char(required=True)

    date = fields.Date()

    conclusion = fields.Html()

    policy_id = fields.Many2one(comodel_name="qms.policy", ondelete="set null")

    document_id = fields.Many2one(comodel_name="qms.document", ondelete="set null")

    goal_id = fields.Many2one(comodel_name="qms.goal", ondelete="set null")

    process_id = fields.Many2one(comodel_name="qms.process", ondelete="set null")

    hazard_id = fields.Many2one(comodel_name="qms.hazard", ondelete="set null")

    indicator_id = fields.Many2one(comodel_name="qms.indicator", ondelete="set null")

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )
