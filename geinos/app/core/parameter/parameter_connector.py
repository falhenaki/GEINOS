from app.core.parameter.parameter import Parameter
from app.core.parameter.list_parameter import ListParameter
from app.core.log import log_connector
from sqlalchemy.orm import sessionmaker
from app import engine
from app.core.exceptions.custom_exceptions import Conflict, GeneralError, MissingResource
import ipaddress


def get_all_parameters():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Parameter)
    prms = []
    for pm in query:
        prms.append(pm.as_dict())
    return prms


def parameter_exists(parameter_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Parameter).filter(Parameter.param_name == parameter_name).first()
    if query is not None:
        raise Conflict("Parameter %s to be added already exists", parameter_name)
    return (query is not None)


def get_all_parameter_names():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Parameter)
    param_names = []
    for pm in query:
        param_names.append(pm.param_name)
    return param_names


def get_parameter_next_value(name, request_ip):
    Session = sessionmaker(bind=engine)
    s = Session()
    param = s.query(Parameter).filter(Parameter.param_name == name).first()
    ret_value = ""
    if param.param_type == "RANGE":
        if param.start_value.count('.') == 3:  # ipv4 -- TODO better way
            start = int(ipaddress.IPv4Address(param.start_value))
            end = int(ipaddress.IPv4Address(param.end_value))
            start = start + param.current_offset
            if start > end:
                # param.current_offset = '1'
                # ret_value = param.start_value
                log_connector.add_log(1, "Ran out of params in range (param: {}). Starting over.".format(name), None,
                                      None, request_ip)
                raise Conflict("Ran out of parameters to assign")
            else:
                ret_value = ipaddress.IPv4Address(start + param.current_offset)
                param.current_offset = param.current_offset + 1
        else:
            ret_value = param.start_value + param.current_offset
            param.current_offset = param.current_offset + 1
    elif param.param_type == "LIST":
        lst = s.query(ListParameter).filter(ListParameter.param_name == name)
        if (param.current_offset >= len(lst)):
            # param.current_offset = 0
            log_connector.add_log(1, "Ran out of params in list (param: {}). Starting over.".format(name), None, None,
                                  request_ip)
            raise Conflict("Ran out of parameters to assign")
        ret_value = lst[param.current_offset].param_value
        param.current_offset = param.current_offset + 1
    else:
        ret_value = param.start_value
    s.add(param)
    s.commit()
    return ret_value


def add_parameter(name, type, val, username, user_role, request_ip):
    if not parameter_exists(name):
        Session = sessionmaker(bind=engine)
        s = Session()
        if (type == "RANGE"):
            val = val.split("-")
            dv = Parameter(name, val[0], type, val[1])
            s.add(dv)
        elif (type == "LIST"):
            val = val.split(",")
            dv = Parameter(name, "", type)
            dv.current_offset = 0
            s.add(dv)
            for index, value in enumerate(val):
                pm = ListParameter(name, value, index)
                s.add(pm)
        else:  # scalar
            dv = Parameter(name, val, type)
            s.add(dv)
        s.commit()
        log_connector.add_log(1, "Added the {} parameter".format(name), username, user_role, request_ip)
        return True
    else:
        log_connector.add_log(1, "Failed to add the {} parameter".format(name), username, user_role, request_ip)
        raise GeneralError("Next parameter value for: {} could not be obtained for unknown reasons", name)


def remove_parameter(param_name, username, user_role, request_ip):
    Session = sessionmaker(bind=engine)
    s = Session()
    param = s.query(Parameter).filter(Parameter.param_name == param_name)
    if param is None:
        raise MissingResource("Parameter to be removed did not exist")
    param.delete()
    if param is 0:
        log_connector.add_log(1, "Failed to delete parameter: {}".format(param_name), username, user_role, request_ip)
        raise GeneralError("Parameter could not be removed for unknown reasons")
    s.commit()
    log_connector.add_log(1, "Deleted parameter: {}".format(param_name), username, user_role, request_ip)
    return True
