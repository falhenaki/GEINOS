from flask_restful import Resource, reqparse
from flask import request, jsonify
from app.core.template import xml_templates, template_connector
from app.core.api import request_parser
parser = reqparse.RequestParser()


# parser.add_argument('template_name')

class Templates(Resource):
    """
    API to get template files. If no filename is specified will return all files currently saved, if a filename is
    specified it will return the contents of that file
    """
    """
    HTTP Method: GET
    Authorization: Required
    Authorization type: (auth token) OR (username and password)
    Parameters (json): template_name = Name of Template
    Description : API to get template files. If no filename is specified will return all files currently saved, if a filename is
    specified it will return the contents of that file
    :return:
    Success: status= 200, message= "Sent Templates", data= templates(json)
    Failure: status= 400, message= "Could not send templates"
    """
    def get(self, template_name=None):
        status = 400
        message="error"
        data = []
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            if (template_name is None):
                 nms = xml_templates.get_templates()
            else:
                nms = xml_templates.get_template(template_name)
            status=200
            message="Sent Templates"
            data=nms

        else:
            status=401
            message="Unauthorized"
        return jsonify(
            auth_token=auth_token,
            status=status,
            message=message,
            data=data
        )

    def post(self):
        """
        HTTP Method: PUT
        Authorization: Required
        Authorization type: (auth token) OR (username and password)
        Parameters (file): file (file)
        Description : upload a new template file
        :return:
        Success: status= 200, message = 'Template Added'
        Failure:
            status: 400, message = 'Template not added'
        """
        status = 400
        message = "Template not added"
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            if 'file' in request.files:
                file = request.files['file']
                '''
                get_templates = template_connector.get_template_names()
                templates = []
                for t in get_templates:
                    templates.append(t[0])
                if file.filename in templates:
                    return jsonify(
                        status=402,
                        message= "Cannot create template. Template already exists"
                    )
                '''
                if xml_templates.save_with_jinja(file, file.filename, logged_user.username, logged_user.role_type, request.remote_addr):
                   status = 200
                   message = "Template Added"
        else:
            status=401
            message = "Unauthorized"
        return jsonify(
            auth_token=auth_token,
            status=status,
            message=message
        )

    def delete(self):
        print("Attempting to delete a template")
        status = 401
        message = "Unauthorized"
        logged_user = request_parser.validateCreds(request)
        auth_token = ""
        if (logged_user):
            auth_token = logged_user.generate_auth_token().decode('ascii') + ":unused"
            content = request.get_json()
            template_names = content['names']
            deleted, not_deleted = template_connector.delete_templates(template_names, logged_user.username, logged_user.role_type, request.remote_addr)
            if len(not_deleted) == 0:
                print("Deleted template: " + str(template_names))
                status=200
                message="Templates deleted: {}".format(','.join(deleted))
            else:
                print("Failed to delete template: " + str(template_names))
                status = 412,
                message = "Templates not deleted : {}\nTemplates deleted : {}".format(','.join(not_deleted), ','.join(deleted))
        return jsonify(
            auth_token=auth_token,
            status=status,
            message=message
        )