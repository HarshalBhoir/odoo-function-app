import logging
import os
import json
import xmlrpc.client

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Odoo create customer.')

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

    try:
        req_body = req.get_json()

        name = req_body.get('name')
        email = req_body.get('email')
        is_company = req_body.get('is_company')

        logging.info(f'Name: {name}')
        logging.info(f'Email: {email}')
        logging.info(f'Is company: {is_company}')

        if name and email and (is_company is not None):
            # execute query
            id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
                'name': name,
                'email': email,
                'is_company': is_company
            }], {})

            return func.HttpResponse(str(id))
        else:
            raise ValueError("Empty value")
    except ValueError as e:
        return func.HttpResponse(body=str(e), status_code=500)
