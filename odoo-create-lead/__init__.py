import logging
import os
import json
import xmlrpc.client

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Odoo create new lead.')

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

    # get request body
    try:
        req_body = req.get_json()

        name = req_body.get('name')
        description = req_body.get('description')

        logging.info(f'Name: {name}')
        logging.info(f'Description: {description}')

        # execute query
        if name and description:
            id = models.execute_kw(db, uid, password, 'crm.lead', 'create', [{
                'name': name,
                'description': description
            }])

            return func.HttpResponse(json.dumps({ 'id': id }), mimetype="application/json")
        else:
            raise ValueError("Not Found")
    except ValueError as e:
        return func.HttpResponse(body=str(e), status_code=500)
           
