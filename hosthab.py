import threading
import socket
import json
import telebot

token = ""

bot = telebot.TeleBot(token=token)


from Archive import workbyfile
from Archive import hostbd
from Archive import userbd

tableSock = {}

def send(data, idv):
    if type(data) == str:
        data = data.encode("utf-8")
    elif type(data) == dict:
        data = json.dumps(data).encode("utf-8")
    while True:
        if tableSock[int(idv)]["locked"]:
            break
    tableSock[int(idv)]["locked"] = True
    tableSock[int(idv)]["socked"].send(data)
    tableSock[int(idv)]["locked"] = False


def connect(sock, addr):
    while True:
        data = sock.recv(2048)
        data = data.decode("utf-8")

        if data is None:
            print("Disconnect. Not Data: ", addr)
            return False

        date = json.loads(data)

        try:
            method = date.get("method")
            param = date.get("param")


            if method == "Activate":
                print("Activate:")
                print(date)

                hostWI = hostbd.get_vodomat(int(param['idv']))
                if hostWI['State'] == 'WAIT':
                        try:
                            idv = param['idv']
                            send(date, idv)
                        except:
                            bot.send_message(param['idT'],
                                             "Приносим вам свои извинения,"
                                             "но водомат временно в не рабочем состоянии!")



            elif method == "Stop":
                        print("Stop:")
                        print(date)

                        try:
                            idv = param['idv']

                            send(date, idv)

                        except:
                            bot.send_message(param['idT'],
                                             "Приносим вам свои извинения,"
                                             "но водомат временно в не рабочем состоянии!")



            elif method == "Answer":
                print("Answer:")
                print(date)
                HowManyWere = userbd.get_user(param['idT'])
                HowManyWere = int(HowManyWere['score'])
                
                userbd.update_user(**param)
                bot.send_message(param['idT'], "У вас на счету " + str(param['score']) + "₽")

                ScoreVodomat = hostbd.get_vodomat(param['idv'])
                ScoreVodomat = int(ScoreVodomat['score'])





            elif method == "error":
                bot.send_message(param['idT'], "В ходе работы произошла ошибка, "
                                               "пожалуйста попробуйте еще разок, ладненько?")



            elif method == "status":  # for get information about hosts
                prev = hostbd.get_vodomat(param['idv'])
                idv = param['idv']
                ypar = {'method': 'got', 'param': 'saved'}
                send(ypar, idv)
                if date != prev:
                    hostbd.update_vodomat(**param)
                    workbyfile.write_on_file(date)
                    # print("Savedate = %s" % date)


            elif method == "connect":
                hostbd.add_host(param['idv'])
                idv = param['idv']
                hostbd.update_vodomat(**param)
                tableSock.update({date['param']['idv']: {"socket": sock, "locked": False}})
                workbyfile.write_on_file(date)
                ypar = {'method': 'got', 'param': 'saved'}
                send(ypar, idv)
            else:
                ypar = {"method": "error", "param": {"type": "not method", "args": method}}
                idv = param['idv']
                send(ypar, idv)



        except ConnectionResetError:
            tableSock.pop({date['param']['idv']: sock})
            print("Disconnect: ", addr)
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(e)

def habStart():
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1000)

    while True:
        print("hosthab")
        conn, addr = sock.accept()
        print("Connect: ", addr)
        t = threading.Thread(target=connect, args=(conn, addr))
        t.start()
habStart()
