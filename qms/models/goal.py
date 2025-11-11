from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Goal(models.Model):

    _name = "qms.goal"
    _description = "Goal"

    name = fields.Char(required=True)

    description = fields.Html()

    cancel_date = fields.Date(readonly=True)

    date_open = fields.Date()

    date_close = fields.Date()

    approved = fields.Boolean()

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True
    )

    process_ids = fields.Many2many(comodel_name="qms.process", required=True)

    resource_ids = fields.Many2many(comodel_name="qms.resource")

    measurement_ids = fields.One2many(
        comodel_name="qms.goal.measurement", inverse_name="goal_id"
    )

    action_ids = fields.One2many(
        comodel_name="qms.action", inverse_name="goal_id"
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("open", "Open"),
            ("closed", "Closed"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=True,
    )

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="goal_id"
    )

    last_measurement_date = fields.Date(
        compute="_compute_last_measurement_date", store=True
    )

    last_measurement_result = fields.Char(
        compute="_compute_last_measurement_result", store=True
    )

    last_review_date = fields.Date(compute="_compute_last_review_date", store=True)

    @api.depends("measurement_ids.measurement_date")
    def _compute_last_measurement_date(self):
        for goal in self:
            if goal.measurement_ids:
                last_measurement = goal.measurement_ids.sorted(
                    key=lambda r: r.measurement_date, reverse=True
                )
                goal.last_measurement_date = last_measurement[0].measurement_date
            else:
                goal.last_measurement_date = False

    @api.depends("measurement_ids.measurement_date", "measurement_ids.result")
    def _compute_last_measurement_result(self):
        for goal in self:
            if goal.measurement_ids:
                last_measurement = goal.measurement_ids.sorted(
                    key=lambda r: r.measurement_date, reverse=True
                )
                goal.last_measurement_result = last_measurement[0].result
            else:
                goal.last_measurement_result = False

    @api.depends("review_ids.date")
    def _compute_last_review_date(self):
        for goal in self:
            if goal.review_ids:
                last_review = goal.review_ids.sorted(
                    key=lambda r: r.date, reverse=True
                )
                goal.last_review_date = last_review[0].date
            else:
                goal.last_review_date = False
                
    def action_toggle_approved(self):
        self.approved = not self.approved

    def action_draft(self):
        self.state = "draft"

    def action_open(self):
        self.state = "open"
        if not self.date_open:
            self.date_open = fields.Date.today()

    def action_close(self):
        self.state = "closed"
        if not self.date_close:
            self.date_close = fields.Date.today()

    def action_cancel(self):
        self.state = "cancelled"
        if not self.cancel_date:
            self.cancel_date = fields.Date.today()

    @api.constrains("date_open", "date_close")
    def _check_dates(self):
        for goal in self:
            if goal.date_close and goal.date_open:
                if goal.date_close < goal.date_open:
                    raise ValidationError(
                        _("Close date must be after open date")
                    )
