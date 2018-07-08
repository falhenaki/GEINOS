from app.core.parameter.parameter import Parameter
from app.core.parameter.list_parameter import ListParameter
from app.core.log import log_connector
from sqlalchemy.orm import sessionmaker
from app import engine
from app.core.exceptions.custom_exceptions import Conflict, GeneralError, MissingResource, InvalidInput
import ipaddress
from app.core.device.device import Device
from app.core.device import device_access

def get_all_parameters():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Parameter).with_entities(Parameter.param_name, Parameter.param_type, Parameter.start_value)
    ret = []
    atts_returned = ['param_name', 'param_type', 'start_value']
    for d in query:
        dictionary = {}
        for att in atts_returned:
            dictionary[att] = getattr(d, att)
        ret.append(dictionary)
    return ret


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


def get_parameter_next_value(name, request_ip, sn):
    Session = sessionmaker(bind=engine)
    s = Session()
    param = s.query(Parameter).filter(Parameter.param_name == name).first()
    ret_value = ""
    if param.param_type == "DYNAMIC":
        return '??dynamic??'
    elif param.param_type == "RANGE":
        if param.start_value.count('.') == 3:  # ipv4 -- TODO better way
            start = int(ipaddress.IPv4Address(param.start_value))
            end = int(ipaddress.IPv4Address(param.end_value))
            start = start + param.current_offset
            if start > end:
                # param.current_offset = '1'
                # ret_value = param.start_value
                log_connector.add_log('PARAM OVERFLOW', "Ran out of params in range (param: {}). Starting over.".format(name), None,
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
            log_connector.add_log('PARAM OVERFLOW', "Ran out of params in list (param: {}). Starting over.".format(name), None, None,
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
        if (type.upper() == "RANGE"):
            dv = Parameter(name, str(val[0]), "RANGE", str(val[-1]))
            s.add(dv)
        elif (type.upper() == "LIST"):
            val = val.split(",")
            dv = Parameter(name, "", "LIST")
            dv.current_offset = 0
            s.add(dv)
            for index, value in enumerate(val):
                pm = ListParameter(name, value, index)
                s.add(pm)
        elif (type.upper() == "SCALAR"):
            dv = Parameter(name, val, type)
            s.add(dv)
        else:
            raise InvalidInput("Invalid Parameter Type")
        s.commit()
        log_connector.add_log('ADD PARAM', "Added the {} parameter".format(name), username, user_role, request_ip)
        return True
    else:
        log_connector.add_log('ADD PARAM FAIL', "Failed to add the {} parameter".format(name), username, user_role, request_ip)
        raise GeneralError("Next parameter value for: {} could not be obtained for unknown reasons", name)


def add_dynamic_parameter(name, type, val, username, user_role, request_ip, interface):
    if not parameter_exists(name):
        Session = sessionmaker(bind=engine)
        s = Session()
        param = Parameter(name, val, type, None, interface)
        s.add(param)
        s.commit()
        log_connector.add_log('ADD PARAM', "Added the {} parameter".format(name), username, user_role, request_ip)
        return True
    else:
        log_connector.add_log('ADD PARAM FAIL', "Failed to add the {} parameter".format(name), username, user_role, request_ip)
        raise GeneralError("Next parameter value for: {} could not be obtained for unknown reasons", name)

def get_dynamic_parameter(name, sn):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Device).filter(Device.serial_number == sn).first()
    param = s.query(Parameter).filter(Parameter.param_name == name).first()
    if (query is not None and param is not None):
        ifaddr = device_access.get_interface_address(query.IP, query.username, query.password, param.interface)
        return get_dynamic_ip(param.start_value, ifaddr)
    else:
        raise GeneralError("Dynamic param can't be retrieved: {}", name)

def get_dynamic_ip(subnet, interface):
    if (subnet.split('/')[1] is '8'):
        return subnet.split('/')[0].split('.')[0] + interface.split('.')[1] + interface.split('.')[2] + interface.split('.')[3]
    elif (subnet.split('/')[1] is '16'):
        return subnet.split('/')[0].split('.')[0] + subnet.split('/')[0].split('.')[1] + interface.split('.')[2] + interface.split('.')[3]
    elif (subnet.split('/')[1] is '24'):
        return subnet.split('/')[0].split('.')[0] + subnet.split('/')[0].split('.')[1] + subnet.split('/')[0].split('.')[2] + interface.split('.')[3]
    else:
        return subnet.split('/')[0]

def remove_parameter(param_name, username, user_role, request_ip):
    Session = sessionmaker(bind=engine)
    s = Session()
    param = s.query(Parameter).filter(Parameter.param_name == param_name)
    if param is None:
        raise MissingResource("Parameter to be removed did not exist")
    param.delete()
    if param is 0:
        log_connector.add_log('DELETE PARAM', "Failed to delete parameter: {}".format(param_name), username, user_role, request_ip)
        raise GeneralError("Parameter could not be removed for unknown reasons")
    s.commit()
    log_connector.add_log('DELETE PARAM FAIL', "Deleted parameter: {}".format(param_name), username, user_role, request_ip)
    return True


def number_of_parameter(param_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    param = s.query(Parameter).filter(Parameter.param_name == param_name)
    if param is None:
        raise MissingResource("Parameter to be removed did not exist")
    if (param.param_type is 'SCALAR' or (param.param_type is 'DYNAMIC')):
        return -1
    elif (param.param_type is 'LIST'):
        return s.query(ListParameter).filter(ListParameter.param_name == param_name).count()
    elif (param.param_type is 'RANGE'):
        if (ipaddress.IPv4Address(param.end_value) - ipaddress.IPv4Address(param.start_value) - param.current_offset) > 0:
            return ipaddress.IPv4Address(param.end_value) - ipaddress.IPv4Address(param.start_value) - param.current_offset
        else:
            return 0
    else:
        return 0