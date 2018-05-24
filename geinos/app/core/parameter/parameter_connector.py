from app.core.parameter.parameter import Parameter
from app.core.parameter.list_parameter import ListParameter
from sqlalchemy.orm import sessionmaker
from app import engine
import ipaddress

def get_all_parameters():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Parameter)
    prms=[]
    for pm in query:
        prms.append([pm.param_name,pm.param_type,pm.start_value])
    return prms

def get_all_parameter_names():
	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(Parameter)
	param_names = []
	for pm in query:
		param_names.append(pm.param_name)
	return param_names

def get_parameter_next_value(name):
    Session = sessionmaker(bind=engine)
    s = Session()
    param = s.query(Parameter).filter(Parameter.param_name == name).first()
    ret_value = ""
    if param.param_type == "RANGE":
        if param.start_value.count('.') == 3: # ipv4 -- TODO better way
            start = int(ipaddress.IPv4Address(param.start_value))
            end = int(ipaddress.IPv4Address(param.end_value))
            start = start + param.current_offset
            if start > end:
                param.current_offset = '1'
                ret_value = param.start_value
            else:
                ret_value = ipaddress.IPv4Address(start + param.current_offset)
                param.current_offset = param.current_offset + 1
        else:
            ret_value = param.start_value + param.current_offset
            param.current_offset = param.current_offset + 1
    elif param.param_type == "LIST":
        lst = s.query(ListParameter).filter(ListParameter.param_name == name)
        if (param.current_offset >= len(lst)):
            param.current_offset = 0
        ret_value = lst[param.current_offset].param_value
        param.current_offset = param.current_offset + 1
    else:
        ret_value = param.start_value
    s.add(param)
    s.commit()
    return ret_value

def add_parameter(name,type,val):
    Session = sessionmaker(bind=engine)
    s = Session()
    if (type == "RANGE"):
        val = val.split("-")
        dv = Parameter(name,val[0],type,val[1])
        s.add(dv)
    elif (type == "LIST"):
        val = val.split(",")
        dv = Parameter(name,"",type)
        dv.current_offset = 0
        s.add(dv)
        for index,value in enumerate(val):
            pm = ListParameter(name, value, index)
            s.add(pm)
    else: # scalar
        dv = Parameter(name,val,type)
        s.add(dv)
    s.commit()

def remove_parameter(param_name):
    Session = sessionmaker(bind=engine)
    s = Session()
    param = s.query(Parameter).filter(Parameter.param_name == param_name).delete()
    if param is 0:
        return False
    s.commit()
    return True