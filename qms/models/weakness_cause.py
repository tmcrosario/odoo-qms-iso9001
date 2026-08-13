from odoo import api, exceptions, fields, models


class WeaknessCause(models.Model):
    _name = "qms.weakness.cause"
    _description = "Weakness Cause"
    _order = "parent_id, sequence"
    _parent_store = True
    _inherit = ["qms.finding.milestone"]

    parent_id = fields.Many2one(
        comodel_name="qms.weakness.cause", string="Group", ondelete="restrict"
    )

    child_ids = fields.One2many(
        comodel_name="qms.weakness.cause",
        inverse_name="parent_id",
        string="Child Causes",
    )

    @api.constrains("parent_id")
    def _check_parent_recursion(self):
        # MIG(19.0): _check_recursion() (returned True when VALID) was removed in
        # 18.0 and replaced by _has_cycle() (returns True when a cycle EXISTS).
        if self._has_cycle():
            raise exceptions.ValidationError(
                self.env._("Error! Cannot create recursive cycle.")
            )
