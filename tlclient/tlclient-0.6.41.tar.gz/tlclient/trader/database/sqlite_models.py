# auto generated by update_py.py
from peewee import CharField, DoubleField, IntegerField
from peewee import CompositeKey, Model, SqliteDatabase

rtn_order_db = SqliteDatabase(None)
rtn_trade_db = SqliteDatabase(None)
position_db = SqliteDatabase(None)
capital_db = SqliteDatabase(None)


class RtnOrder(Model):
    """
        message_pb.RtnOrder
    """
    class Meta:
        database = rtn_order_db
        table_name = 'rtn_order'

    account_id     = CharField(null=True)
    sub_account    = CharField(null=True)
    sender         = CharField(null=True)
    order_id       = IntegerField(primary_key=True)
    order_ref      = CharField(null=True)
    parent_id      = IntegerField(null=True)
    front_id       = IntegerField(null=True)
    session_id     = IntegerField(null=True)
    exchange       = IntegerField(null=True)
    offset_flag    = IntegerField(null=True)
    order_status   = IntegerField(null=True)
    order_type     = IntegerField(null=True)
    security_type  = IntegerField(null=True)
    side           = IntegerField(null=True)
    symbol         = CharField(null=True)
    traded_vol     = DoubleField(null=True)
    traded_price   = DoubleField(null=True)
    traded_amt     = DoubleField(null=True)
    create_time    = CharField(null=True)
    recv_time      = CharField(null=True)
    update_time    = CharField(null=True)
    entrust_vol    = DoubleField(null=True)
    entrust_price  = DoubleField(null=True)
    entrust_amt    = DoubleField(null=True)
    frz_amt        = DoubleField(null=True)
    frz_fee        = DoubleField(null=True)
    extra_info     = CharField(null=True)
    margin_mode    = IntegerField(null=True)
    source_type    = IntegerField(null=True)
    lever_rate     = IntegerField(null=True)
    err_id         = IntegerField(null=True)
    err_msg        = CharField(null=True)
    cancel_err_id  = IntegerField(null=True)
    cancel_err_msg = CharField(null=True)


class RtnTrade(Model):
    """
        message_pb.RtnTrade
    """
    class Meta:
        database = rtn_trade_db
        table_name = 'rtn_trade'
        primary_key = CompositeKey('trade_ref', 'order_id')

    account_id    = CharField(null=True)
    sub_account   = CharField(null=True)
    sender        = CharField(null=True)
    trade_ref     = CharField()
    order_id      = IntegerField()
    order_ref     = CharField(null=True)
    exchange      = IntegerField(null=True)
    exec_role     = IntegerField(null=True)
    offset_flag   = IntegerField(null=True)
    order_type    = IntegerField(null=True)
    security_type = IntegerField(null=True)
    side          = IntegerField(null=True)
    symbol        = CharField(null=True)
    traded_vol    = DoubleField(null=True)
    traded_price  = DoubleField(null=True)
    traded_amt    = DoubleField(null=True)
    commission    = DoubleField(null=True)
    trading_day   = CharField(null=True)
    recv_time     = CharField(null=True)
    trade_time    = CharField(null=True)
    entrust_vol   = DoubleField(null=True)
    entrust_price = DoubleField(null=True)
    entrust_amt   = DoubleField(null=True)
    currency      = IntegerField(null=True)
    source_type   = IntegerField(null=True)


class Position(Model):
    """
        message_pb.GatewayPosition
    """
    class Meta:
        database = position_db
        table_name = 'position'
        primary_key = CompositeKey('pos_id', 'account_id', 'sub_account', 'direction', 'security_type', 'symbol')

    pos_id         = IntegerField()
    account_id     = CharField(null=True)
    sub_account    = CharField(null=True)
    direction      = IntegerField(null=True)
    exchange       = IntegerField(null=True)
    margin_mode    = IntegerField(null=True)
    security_type  = IntegerField(null=True)
    symbol         = CharField(null=True)
    position       = DoubleField(null=True)
    yd_pos         = DoubleField(null=True)
    avail_pos      = DoubleField(null=True)
    frz_pos        = DoubleField(null=True)
    pos_cost       = DoubleField(null=True)
    borrowed       = DoubleField(null=True)
    interest       = DoubleField(null=True)
    liq_price      = DoubleField(null=True)
    margin         = DoubleField(null=True)
    mkt_value      = DoubleField(null=True)
    risk_rate      = DoubleField(null=True)
    pnl            = DoubleField(null=True)
    realized_pnl   = DoubleField(null=True)
    unrealized_pnl = DoubleField(null=True)
    recv_time      = CharField(null=True)
    source_time    = CharField(null=True)
    source_type    = IntegerField(null=True)
    currency       = IntegerField(null=True)


class Capital(Model):
    """
        message_pb.RspAccount
    """
    class Meta:
        database = capital_db
        table_name = 'capital'
        primary_key = CompositeKey('req_id', 'account_id', 'sub_account')

    req_id         = IntegerField()
    account_id     = CharField(null=True)
    sub_account    = CharField(null=True)
    avail_amt      = DoubleField(null=True)
    balance        = DoubleField(null=True)
    equity         = DoubleField(null=True)
    frz_amt        = DoubleField(null=True)
    frz_margin     = DoubleField(null=True)
    mkt_value      = DoubleField(null=True)
    pnl            = DoubleField(null=True)
    realized_pnl   = DoubleField(null=True)
    unrealized_pnl = DoubleField(null=True)
    recv_time      = CharField(null=True)
    source_time    = CharField(null=True)
    source_type    = IntegerField(null=True)
    currency       = IntegerField(null=True)
    err_id         = IntegerField(null=True)
    err_msg        = CharField(null=True)
