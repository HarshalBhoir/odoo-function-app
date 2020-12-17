import logging
import os
import json
import xmlrpc.client

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Odoo API.')

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
        logging.info(req_body)

        # get value from req body
        model_name = req_body.get('model_name')
        method_name = req_body.get('method_name')
        parameters_by_position = req_body.get('parameters_by_position')
        parameters_by_keyword = req_body.get('parameters_by_keyword')

        # execute query
        if model_name and method_name:
            result = models.execute_kw(db, uid, password, model_name, method_name, parameters_by_position, parameters_by_keyword)

            if isinstance(result, int):
                return func.HttpResponse(str(result))
            else:
                return func.HttpResponse(json.dumps(result), mimetype="application/json")
        else:
            raise Exception("Pls provide model_name, method_name")
    except BaseException as e:
        return func.HttpResponse(body=str(e), status_code=500)
