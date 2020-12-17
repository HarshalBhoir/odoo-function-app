import logging
import os
import json
import xmlrpc.client

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Odoo test request.')

    # define connection var
    url = os.getenv('ODOO_SERVER_URL')
    db = os.getenv('ODOO_DB_NAME')
    username = os.getenv('ODOO_DB_ID')
    password = os.getenv('ODOO_DB_PASSWORD')

    # login to db
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})

    # define model
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # execute query
    result = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [
            [
                ['is_company', '=', True],
                ['active','=',True]
            ]
        ],
        {'fields': ['id', 'name']})

    return func.HttpResponse(json.dumps(result), mimetype="application/json")
