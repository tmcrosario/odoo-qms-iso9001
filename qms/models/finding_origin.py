from odoo import _, api, exceptions, fields, models


class FindingOrigin(models.Model):

    _name = "qms.finding.origin"
    _description = "Finding Origin"
    _order = "parent_id, sequence"
    _parent_store = True
    _inherit = ["qms.finding.milestone"]

    parent_id = fields.Many2one(
        comodel_name="qms.finding.origin", string="Group", ondelete="restrict"
    )

    child_ids = fields.One2many(
        comodel_name="qms.finding.origin",
        inverse_name="parent_id",
        string="Child Origins",
    )

    @api.constrains("parent_id")
    def _check_parent_recursion(self):
        # MIG(19.0): _check_recursion() (returned True when VALID) was removed in
        # 18.0 and replaced by _has_cycle() (returns True when a cycle EXISTS).
        if self._has_cycle():
            raise exceptions.ValidationError(
                _("Error! Cannot create recursive cycle.")
            )
