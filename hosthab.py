import threading
import socket
import json
import telebot

token = "321273335:AAGC0-DP7Rwxu99_sN3sSVdYDOcPgu3869g"

bot = telebot.TeleBot(token=token)


from Archive import workbyfile
from Archive import hostbd
from Archive import userbd

tableSock = {}

def send(sock, data):
    if type(data) == str:
        data = data.encode("utf-8")
    elif type(data) == dict:
        data = json.dumps(data).encode("utf-8")
    sock.send(data)



def connect(sock, addr):
    test = {}
    date={}
    try:
        while True:
            data = sock.recv(2048)
            data = data.decode("utf-8")
            print("data '%s' " % data)
            date = json.loads(data)

            if not data:
                print("Disconnect. Not Data: ", addr)
                break

            if test == date:
                ypar = {'method': 'error', 'param': 'Error not dat'}
                j = json.dumps(ypar)
                sock.send(j.encode("utf-8"))
            else:
                try:
                    method = date.get("method")
                    param = date.get("param")

                    if method == "GetWater":
                        print("PR")
                        hostWI = hostbd.get_vodomat(int(param['idv']))
                        if hostWI is not None:
                            if hostWI['State'] == 'WAIT':
                                print('begin to send to vodomat!')
                                bot.send_message(param['idT'],
                                                 "Спасибо за покупку воды, приятного питья!")

                                j = json.dumps(date)
                                tableSock[int(param["idv"])].send(j.encode("utf-8"))
                            else:
                                print("PRE")
                                bot.send_message(param['idT'], "Приносим вам свои извинения, но водомат в не рабочем состоянии!")
                        else:
                            bot.send_message(param['idT'],
                                             "Вы ввели неправильный ID водомата!")


                    elif method == "ToUpBalance":
                            hostWI = hostbd.get_vodomat(param['idv'])
                            if hostWI is not None:
                                if hostWI['State'] == 'WAIT':
                                    bot.send_message(param['idT'],
                                                     "Спасибо за пополнения счета!")
                                    print('begin to send to vodomat!')
                                    j = json.dumps(date)
                                    try :
                                            tableSock[int(param['idv'])].send(j.encode("utf-8"))
                                    except:
                                            bot.send_message(param['idT'],
                                                         "Приносим вам свои извинения,"
                                                         "но водомат временно в не рабочем состоянии!")
                                else:
                                    bot.send_message(param['idT'], "Водома уже занят, попробуйте позже")
                                    ypar = {"method": "error", "param": {"type": "vodomat",
                                                                         "args": hostWI['State']}}
                                    send(sock, ypar)
                            else:
                                bot.send_message(param['idT'], "Вы ввели неправильный ID водомата!")

                    elif method == "AnswerPay":
                            getBd=userbd.get_user(param['idT'])
                            print("getBd: %s" % getBd)
                            getscore = int(getBd['score']) - int(param['score'])
                            print("getscore: %s" % getscore)
                            hostbd.update_vodomatScore(param['idv'],getscore)
                            userbd.update_user(**param)
                            bot.send_message(param['idT'], "У вас на счету " + str(param['score']) + "₽")

                    elif method == "AnswerUP":
                            bot.send_message(param['idT'], "У вас на счету " + str(param['score']) + "₽")
                            userbd.update_user(**param)

                    elif method == "error":
                            bot.send_message(param['idT'], "В ходе работы произошла ошибка, пожалуйста попробуйте еще разок, ладненько?")

                    elif method == "status":  # for get information about hosts
                            prev = hostbd.get_vodomat(param['idv'])
                            ypar = {'method': 'got', 'param': 'saved'}
                            send(sock, ypar)
                            if date != prev:
                                hostbd.update_vodomat(**param)
                                workbyfile.write_on_file(date)
                                print("Savedate = %s" % date)

                    elif method == "connect":
                            hostbd.add_host(param['idv'])
                            hostbd.update_vodomat(**param)
                            tableSock.update({date['param']['idv']: sock})
                            workbyfile.write_on_file(date)
                            ypar = {'method': 'got', 'param': 'saved'}
                            send(sock, ypar)
                    else:
                        ypar = {"method": "error", "param": {"type": "not method", "args": method}}
                        send(sock, ypar)

                except Exception as e:
                    print(e)
                    ypar = {"method": "error", "param": {"type": "fatal error", "args": e.args}}
                    send(sock, ypar)

    except ConnectionResetError:
        tableSock.pop({date['param']['idv']: sock})
        print("Disconnect: ", addr)
    except json.JSONDecodeError:
        pass

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