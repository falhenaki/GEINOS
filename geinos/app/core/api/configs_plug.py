from flask_restful import Resource
from flask import request, jsonify, session
from flask_httpauth import HTTPBasicAuth
from app.core.user import auth
from app.core.device.device_access import *
authen = HTTPBasicAuth()

class Device_Configs(Resource):
    def get(self):
        status=400
        message = "Configs not created"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            print("YEASH")
            #hst = request.form["host"]
            #usr = request.form["username"]
            #passw = request.form["pass"]
            hst = "192.168.1.1"
            usr = "admin"
            passw = "admin"

            print(hst)
            print(usr)
            print(passw)
            '''
            dev = Device(host=hst,username=usr,password=passw)
            print("00000000000000000000000000000000000000000000000")
            dev.open()
            print("111111111111111111111111111111111111111111111111111111")
            with Config(dev) as cm:
                out = cm.get(format='json')
                print(out)
                status=200
            '''
            conf = get_config(hst,usr,passw)
            status=200
            message="ok"
        return jsonify(
            status=status,
            message=message
        )
    def put(self):
        t_config="""
                <config>
                    <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system">
                        <ntp>
                            <use-ntp>true</use-ntp>
                            <ntp-server>
                                <address>1.1.1.1</address>
                            </ntp-server>
                        </ntp>
                    </system>
                </config>
                """
        status = 400
        message = "Not success"
        if (auth.login(request.authorization["username"], request.authorization["password"])):
            print("YEASH")
            #hst = request.form["host"]
            #usr = request.form["username"]
            #passw = request.form["pass"]
            hst = "192.168.1.1"
            usr = "admin"
            passw = "admin"
            '''
            dev = Device(host=hst,username=usr,password=passw)
            print("00000000000000000000000000000000000000000000000")
            dev.open()
            print("111111111111111111111111111111111111111111111111111111")
            with Config(dev) as cm:
                rsp = cm.load(content=t_config)
                print(rsp)
                rsp = cm.validate()
                print(rsp)
                rsp = cm.commit()
                print(rsp)
                status=200
                message="ok"
            '''
            set_config(hst,usr,passw,t_config)
        return jsonify(
            status=status,
            message=message
            )