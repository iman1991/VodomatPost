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

def send(sock, data):
    if type(data) == str:
        data = data.encode("utf-8")
    elif type(data) == dict:
        data = json.dumps(data).encode("utf-8")
    sock.send(data)

def connect(sock, addr):
    while True:
        data = sock.recv(2048)
        data = data.decode("utf-8")
        print("data '%s' " % data)

        if data is None:
            print("Disconnect. Not Data: ", addr)
            return False

        date = json.loads(data)

        try:
            method = date.get("method")
            param = date.get("param")

            # if method == "GetWater":
            #     hostWI = hostbd.get_vodomat(int(param['idv']))
            #     if hostWI is not None:
            #         if hostWI['State'] == 'WAIT':
            #             bot.send_message(param['idT'],
            #                              "Спасибо за покупку воды, приятного питья!")
            #
            #             j = json.dumps(date)
            #             tableSock[int(param["idv"])].send(j.encode("utf-8"))
            #         else:
            #             bot.send_message(param['idT'],
            #                              "Приносим вам свои извинения, но водомат в не рабочем состоянии!")
            #     else:
            #         bot.send_message(param['idT'],
            #                          "Вы ввели неправильный ID водомата!")

            if method == "Activate":
                hostWI = hostbd.get_vodomat(int(param['idv']))
                if hostWI['State'] == 'WAIT':
                        try:
                            j = json.dumps(date)
                            tableSock[int(param['idv'])].send(j.encode("utf-8"))
                        except:
                            bot.send_message(param['idT'],
                                             "Приносим вам свои извинения,"
                                             "но водомат временно в не рабочем состоянии!")



            elif method == "GetWaterStop":
                        try:
                            j = json.dumps(date)
                            tableSock[int(param['idv'])].send(j.encode("utf-8"))
                        except:
                            bot.send_message(param['idT'],
                                             "Приносим вам свои извинения,"
                                             "но водомат временно в не рабочем состоянии!")



            elif method == "Answer":
                userbd.update_user(**param)
                bot.send_message(param['idT'], "У вас на счету " + str(param['score']) + "₽")
                ScoreVodomat = hostbd.get_vodomat(param['idv'])
                ScoreVodomat = int(ScoreVodomat['score'])
                try:
                    date['method']="GetStatus"
                    j = json.dumps(date)

                    tableSock[int(param['idv'])].send(j.encode("utf-8"))
                except:
                    bot.send_message(param['idT'],
                                     "Приносим вам свои извинения,"
                                     "но водомат временно в не рабочем состоянии!")

                data2 = sock.recv(2048)
                data2 = data2.decode("utf-8")
                date2 = json.loads(data2)

                HowManyWereSpent = int(date2['param']['totalPaid'])
                all = ScoreVodomat + HowManyWereSpent - int(date2['param']['sessionpaid'])
                hostbd.update_vodomatScore(param['idv'], all)

                # getscore = date2['method']['param']['sessionpaid']

                # getBd = userbd.get_user(param['idT'])
                # print("getBd: %s" % getBd)
                # getscore = int(getBd['score']) - int(param['score'])
                # print("getscore: %s" % getscore)






            # elif method == "AnswerUP":
            #     bot.send_message(param['idT'], "У вас на счету " + str(param['score']) + "₽")
            #     userbd.update_user(**param)



            elif method == "error":
                bot.send_message(param['idT'],
                                 "В ходе работы произошла ошибка, пожалуйста попробуйте еще разок, ладненько?")



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
