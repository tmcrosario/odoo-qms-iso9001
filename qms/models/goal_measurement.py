# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class GoalMeasurement(models.Model):

    _name = "qms.goal.measurement"
    _description = "Goal Measurement"

    name = fields.Char(string="Measurement", required=True)

    goal = fields.Char()

    goal_id = fields.Many2one(
        comodel_name="qms.goal", ondelete="cascade", string="Goals"
    )

    expected_date = fields.Date()

    measurement_date = fields.Date()

    comments = fields.Text()

    result = fields.Selection(
        selection=[
            ("goal_ok", "Goal achieved"),
            ("goal_with_obs", "Goal achieved with comments"),
            ("goal_no_ok", "Goal not achieved"),
        ],
        required=False,
    )

    result_detail = fields.Char()
