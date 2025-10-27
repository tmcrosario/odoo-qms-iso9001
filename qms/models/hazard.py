from odoo import api, fields, models


class Hazard(models.Model):

    _name = "qms.hazard"
    _description = "Hazard"

    number = fields.Integer()

    description = fields.Html()

    causes = fields.Html()

    consequences = fields.Html()

    type_risk = fields.Selection(
        selection=[
            ("strategic", "Strategic"),
            ("image", "Image"),
            ("operative", "Operative"),
            ("financial", "Financial"),
            ("compliance", "Compliance"),
            ("technological", "Technological"),
            ("corruption", "Corruption"),
            ("information", "Information"),
        ],
        required=False,
    )

    factor = fields.Selection(
        selection=[
            ("e_economic", "Economics (external)"),
            ("e_politicians", "Politicians (external)"),
            ("e_social", "Social (external)"),
            ("e_technological", "Technological (external)"),
            ("e_enviroment", "Enviroment (external)"),
            ("e_communication", "Communication (external)"),
            ("i_financial", "Financial (internal)"),
            ("i_personal", "Personal (internal)"),
            ("i_technological", "Technological (internal)"),
            ("i_strategic", "Srategic (internal)"),
            ("i_communication", "Communication (internal)"),
            ("i_factors", "Factors (internal)"),
        ],
        required=False,
    )

    @api.depends("probability", "impact")
    def _compute_result_and_evaluation(self):
        if self.impact and self.probability:
            self.result = self.impact * self.probability
        else:
            self.result = 0
        if self.result >= 1 and self.result <= 3:
            self.evaluation = "low"
        elif self.result >= 4 and self.result <= 8:
            self.evaluation = "medium"
        elif self.result >= 9 and self.result <= 14:
            self.evaluation = "high"
        elif self.result >= 15 and self.result <= 25:
            self.evaluation = "very_high"
        else:
            self.evaluation = False

    name = fields.Char(required=True)

    date = fields.Date()

    probability = fields.Selection(
        selection=[
            ("1", "Very Low (Rare)"),
            ("2", "Low (Improbable)"),
            ("3", "Medium (Possible)"),
            ("4", "High Medium (Probable)"),
            ("5", "Very High (Almost Sure)"),
        ],
        required=False,
    )

    impact = fields.Selection(
        selection=[
            ("1", "Very Low (Insignificant)"),
            ("2", "Low (Less)"),
            ("3", "Medium (Moderate)"),
            ("4", "High Medium (Higher)"),
            ("5", "Very High (Catastrophic)"),
        ],
        required=False,
    )

    strategy = fields.Selection(
        selection=[
            ("accept", "Accept"),
            ("watch", "Watch"),
            ("evitar", "Avoid"),
            ("transfer", "Transfer"),
            ("reduce", "Reduce"),
            ("share", "Share"),
        ],
        required=False,
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("open", "Open"),
            ("closed", "Closed"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=False,
    )

    evaluation = fields.Selection(
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("very_high", "Very High"),
        ],
        compute=_compute_result_and_evaluation,
        readonly=True,
        store=True,
        compute_sudo=True,
    )

    result = fields.Integer(
        compute=_compute_result_and_evaluation,
        readonly=True,
        store=True,
        compute_sudo=True,
    )

    process_ids = fields.Many2many(comodel_name="qms.process", required=False)

    policy_component_ids = fields.Many2many(
        comodel_name="qms.policy_component", required=False
    )

    action_ids = fields.One2many(
        comodel_name="qms.action", inverse_name="hazard_id"
    )

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="hazard_id"
    )

    last_review_date = fields.Date(compute="_compute_last_review_date")

    @api.depends("review_ids")
    def _compute_last_review_date(self):
        for hazard in self:
            domain = [
                ("hazard_id", "=", hazard.id),
                # ('modify_concession', '=', True)
            ]
            related_reviews = hazard.env["qms.review"].search(domain)
            if related_reviews:
                last_review = related_reviews.sorted(
                    key=lambda r: r.date, reverse=True
                )
                hazard.last_review_date = last_review[0].date
            else:
                hazard.last_review_date = None

    _sql_constraints = [
        models.Constraint("unique(number)", "Number must be unique")
    ]
