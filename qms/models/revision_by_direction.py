# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Revision_by_direction(models.Model):

    _name = "qms.revision_by_direction"

    name = fields.Char(
        required=True
    )

    description = fields.Html()

    date_open = fields.Date()

    date_close = fields.Date()

    _states_ = [
        ('open', 'Open'),
        ('done', 'Closed')
    ]

    resource_ids = fields.Many2many(
        comodel_name='qms.resource'
    )

    non_conformity_ids = fields.One2many(
        comodel_name='qms.non_conformity',
        inverse_name='revision_by_direction_id'
    )

    observation_ids = fields.One2many(
        comodel_name='qms.observation',
        inverse_name='revision_by_direction_id'
    )

    opportunity_ids = fields.One2many(
        comodel_name='qms.opportunity',
        inverse_name='revision_by_direction_id'
    )

    action_ids = fields.One2many(
        comodel_name='qms.action',
        inverse_name='revision_by_direction_id',
        ondelete='cascade'
    )

    responsibles_ids = fields.Many2many(
        comodel_name='qms.interested_party',
        relation='audit_auditor_rel'
        #domain="[('auditor', '=', True)]"
    )

    state = fields.Selection(
        selection=_states_,
        default='open'
    )

    @api.multi
    def button_close(self):
        return self.write(
            {
                'state': 'done',
                'closing_date': fields.Datetime.now()
            }
        )
