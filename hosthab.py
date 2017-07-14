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

def connect(sock, addr):
    test = {}

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
                            if hostWI['State'] == 'WAIT':
                                print('begin to send to vodomat!')
                                bot.send_message(param['idT'],
                                                 "Спасибо за покупку воды, приятного питья!")

                                j = json.dumps(date)
                                tableSock[int(param["idv"])].send(j.encode("utf-8"))
                            else:
                                print("PRE")
                                bot.send_message(param['idT'], "Приносим вам свои извинения, но водомат в не рабочем состоянии!")

                    elif method == "ToUpBalance":
                            hostWI = hostbd.get_vodomat(param['idv'])
                            if hostWI['State'] == 'WAIT':
                                bot.send_message(param['idT'],
                                                 "Спасибо за пополнения счета!")
                                print('begin to send to vodomat!')
                                j = json.dumps(date)
                                tableSock[int(param['idv'])].send(j.encode("utf-8"))
                            else:
                                bot.send_message(param['idT'], "Приносим вам свои извинения, но водомат в не рабочем состоянии!")
                                ypar = {'method': 'error', 'param': 'prombples with vodomat'}
                                j = json.dumps(ypar)
                                sock.send(j.encode("utf-8"))

                    elif method == "Answer":
                            userbd.update_user(**param)
                            bot.send_message(param['idT'], "У вас на счету " + str(param['score']) + "рублей")

                    elif method == "error":
                            bot.send_message(param['idT'], "В ходе работы произошла ошибка, пожалуйста попробуйте еще разок, ладненько?")

                    elif method == "status":  # for get information about hosts
                            prev=hostbd.get_vodomat(param['idv'])
                            if date == prev:
                                ypar = {'method': 'got','param': 'saved'}
                                j = json.dumps(ypar)
                                sock.send(j.encode("utf-8"))
                            else:
                                hostbd.update_vodomat(**param)
                                workbyfile.write_on_file(date)
                                print("Savedate = %s" % date)
                                ypar = {'method': 'got', 'param': 'saved'}
                                j = json.dumps(ypar)
                                sock.send(j.encode("utf-8"))

                    elif method == "connect":
                            hostbd.add_host(param['idv'])
                            hostbd.update_vodomat(**param)
                            tableSock.update({date['param']['idv']: sock})
                            workbyfile.write_on_file(date)
                            ypar = {'method': 'got','param': 'saved'}
                            j = json.dumps(ypar)
                            sock.send(j.encode("utf-8"))
                    else:
                        ypar = {'method': 'error', 'param': 'error'}
                        j = json.dumps(ypar)
                        sock.send(j.encode("utf-8"))
                except  Exception as e:
                    print(e)
                    ypar = {'method': 'error', 'param': 'error'}
                    j = json.dumps(ypar)
                    sock.send(j.encode("utf-8"))

    except ConnectionResetError:
        # tableSock.pop({date['param']['idv']: sock})
        print("Disconnect: ", addr)



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