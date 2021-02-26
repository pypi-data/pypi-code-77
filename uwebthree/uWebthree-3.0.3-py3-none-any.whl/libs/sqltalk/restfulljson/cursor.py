#!/usr/bin/python3
"""SQLTalk Json API Cursor class."""
__author__ = 'Jan Klopper <jan@underdark.nl>'
__version__ = '0.1'


# Custom modules
from .. import sqlresult


class Cursor:
  def __init__(self, connection):
    self.connection = connection

  def Execute(self, query, args=()):
    try:
      result = self.connection.get('%s%s%s', self.connection.url, query, args)
    except Exception:
      self.connection.logger.exception('Exception during query execution')
      raise
    resultjson = result.json
    fieldnames = resultjson[0].keys()
    return sqlresult.ResultSet(
        affected=len(resultjeson),
        charset='utf-8',
        fields=fieldnames,
        insertid=None,
        query=(query, tuple(args)),
        result=resultjson,
    )

  def Insert(self, table, values):
    pass

  def Select(self, table, fields=None, conditions=None, order=None, group=None,
             limit=None, offset=0):
    """Select fields from table that match the conditions, ordered and limited.

    Arguments:
      table:      string/list/tuple. Table(s) to select fields out of.
      fields:     string/list/tuple (optional). Fields to select. Default '*'.
                  As string, single field name. (autoquoted)
                  As list/tuple, one field name per element. (autoquoted)
      conditions: string/list/tuple (optional). SQL 'where' statement.
                  Literal as string. AND'd if list/tuple.
                  THESE WILL NOT BE ESCAPED FOR YOU, EVER.
      order:      (nested) list/tuple (optional).
                  Defines sorting of table before updating, elements can be:
                    string: a field to order by (in default database order).
                    list/tuple of two elements:
                      1) string, field name to order by
                      2) bool, revserse; set this to True to reverse the order
      group:      str (optional). Field name or function to group result by.
      limit:      integer (optional). Defines output size in rows.
      offset:     integer (optional). Number of rows to skip, requires limit.

    Returns:
      sqlresult.ResultSet object.
    """
    if isinstance(table, str):
      table = self.connection.EscapeField(table)
    else:
      table = ', '.join(map(self.connection.EscapeField, table))

    if fields is None:
      fields = '*'
    elif isinstance(fields, str):
      fields = self.connection.EscapeField(fields)
    else:
      fields = ', '.join(map(self.connection.EscapeField, fields))

    if isinstance(conditions, (list, tuple)):
      conditions = ' AND '.join(conditions)
    elif not conditions:
      conditions = 1

    if order is not None:
      orders = []
      for rule in order:
        if isinstance(rule, str):
          orders.append(self.connection.EscapeField(rule))
        else:
          orders.append('%s %s' %
                        (self.connection.EscapeField(rule[0]),
                        ('ASC', 'DESC')[rule[1]]))
      order = 'ORDER BY ' + ', '.join(orders)
    else:
      order = ''

    if group is not None:
      group = 'GROUP BY ' + self.connection.EscapeField(group)
    else:
      group = ''

    if limit is not None:
      if offset:
        limit = 'LIMIT %d OFFSET %d' % (limit, offset)
      else:
        limit = 'LIMIT %d' % limit
    else:
      limit = ''

    query = ('/%s/%s' %
             (table, conditions))
    return self.Execute(query)
