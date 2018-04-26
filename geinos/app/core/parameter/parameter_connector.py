from app.core.parameter.parameter import Parameter
from app.core.parameter.list_parameter import ListParameter
from sqlalchemy.orm import sessionmaker
from app import engine

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
    return param.get_next_value()

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
        for value in val:
            pm = ListParameter(name, value)
            s.add(pm)
    else: # scalar
        dv = Parameter(name,val,type)
        s.add(dv)
    s.commit()
