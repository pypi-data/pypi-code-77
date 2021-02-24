# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields


class BatchLine(metaclass=PoolMeta):
    __name__ = 'account.batch.line'

    bank_imp_line = fields.Many2One('banking.import.line',
        'Banking Import Line', readonly=True)
