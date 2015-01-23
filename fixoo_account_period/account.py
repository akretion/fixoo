# -*- coding: utf-8 -*-
###############################################################################
#
#   fixoo for Odoo
#   Copyright (C) 2015 Akretion (http://www.akretion.com). All Rights Reserved
#   @author Benoît GUILLOT <benoit.guillot@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp.osv import fields, orm


class account_move_line(orm.Model):
    _inherit = "account.move.line"

    def update_period(self, cr, uid, period_ids, context=None):
        period_obj = self.pool['account.period']
        move_obj = self.pool['account.move']
        if not period_ids:
            period_ids = period_obj.search(cr, uid, [], context=context)
        for period in period_obj.browse(cr, uid, period_ids, context=context):
            if not period.special :
                move_ids = move_obj.search(cr, uid,
                                           [('date', '>=', period.date_start),
                                            ('date', '<=', period.date_stop),
                                            ('period_id', '!=', period.id),
                                            ], context=context)
                if move_ids:
                    cr.execute("""
                        UPDATE account_move
                        SET period_id = %s
                        WHERE id in %s""", (period.id, tuple(move_ids)))

                cr.execute("""
                    UPDATE account_move_line
                    SET period_id = account_move.period_id,
                        date=account_move.date
                    FROM account_move
                    WHERE account_move_line.move_id = account_move.id
                    AND account_move_line.period_id != account_move.period_id
                """)
        return True
