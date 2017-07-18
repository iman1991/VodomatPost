#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql.cursors


def connect():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='7087',
                                 db='vodomat',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection



def add_host(idv): # Add a new Vodomat
  result=get_vodomat(idv)
  if result is None or int(result['idv']) != int(idv):
    param = {"idv": 0, "state": "", "input10Counter": 0, "out10Counter": 0,"milLitlose": 0,
                 "milLitWentOut": 0, "milLitContIn": 0, "waterPrice": 0,
                 "waterContThreshold": 0, "contVolume": 0, "totalPaid": 0, "sessionPaid": 0,
                 "leftFromPaid": 0, "container": "", "currentContainerVolume": "",
                 "consumerPump": 0, "mainPump": 0, "magistralPressure": 0, "mainValve": 0,
                 "filterValve": 0, "washFilValve": 0, "tumperMoney": 0, "tumperDoor": 0,
                 "serviceButton": 0, "freeButton": 0, "Voltage": 0}
    param["idv"]=idv
    connection = connect()
    cursor = connection.cursor()
    first = "INSERT INTO vs (idv, state, input10Counter, out10Counter, milLitlose, milLitWentOut, milLitContIn, waterPrice, waterContThreshold, contVolume, totalPaid, sessionPaid, leftFromPaid, container, currentContainerVolume, consumerPump, mainPump, magistralPressure, mainValve, filterValve, washFilValve, tumperMoney, tumperDoor, serviceButton, freeButton, Voltage) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    second = (param.get('idv'), param.get('state'), param.get('input10Counter'),param.get('out10Counter'),param.get('milLitlose'),param.get('milLitWentOut'),param.get('milLitContIn'),param.get('waterPrice'),param.get('waterContThreshold'),param.get('contVolume'),param.get('totalPaid'),param.get('sessionPaid'),param.get('leftFromPaid'),param.get('container'),param.get('currentContainerVolume'),param.get('consumerPump'),param.get('mainPump'),param.get('magistralPressure'),param.get('mainValve'),param.get('filterValve'),param.get('washFilValve'),param.get('tumperMoney'),param.get('tumperDoor'),param.get('serviceButton'),param.get('freeButton'),param.get('Voltage'))
    cursor.execute(first, second)
    connection.commit()
    cursor.close()
    connection.close()
    return True
  return False


# #Get DATABASE
def get_vodomat(idv): # Get a Vodomat with its idv
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vs WHERE idv = %i" % (idv))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results

#UPDATE DATABASE
def update_vodomat(**param):
    connection = connect()
    cursor = connection.cursor()

    divv = param['idv']
    first = "UPDATE vs SET state = %s, input10Counter = %s, out10Counter = %s, milLitlose = %s, milLitWentOut = %s, milLitContIn = %s, waterPrice = %s, waterContThreshold = %s, contVolume = %s, totalPaid = %s, sessionPaid = %s, leftFromPaid = %s, container = %s, currentContainerVolume = %s, consumerPump = %s, mainPump = %s, magistralPressure = %s, mainValve = %s, filterValve = %s, washFilValve = %s, tumperMoney = %s, tumperDoor = %s, serviceButton = %s, freeButton = %s, Voltage = %s WHERE idv = %s "
    second = (param.get('state'), param.get('input10Counter'),param.get('out10Counter'),param.get('milLitlose'),param.get('milLitWentOut'),param.get('milLitContIn'),param.get('waterPrice'),param.get('waterContThreshold'),param.get('contVolume'),param.get('totalPaid'),param.get('sessionPaid'),param.get('leftFromPaid'),param.get('container'),param.get('currentContainerVolume'),param.get('consumerPump'),param.get('mainPump'),param.get('magistralPressure'),param.get('mainValve'),param.get('filterValve'),param.get('washFilValve'),param.get('tumperMoney'),param.get('tumperDoor'),param.get('serviceButton'),param.get('freeButton'),param.get('Voltage'), divv)
    cursor.execute(first, second)

    connection.commit()
    cursor.close()
    connection.close()
    return True

def update_vodomatScore(idv, score): # Get a Vodomat with its idv
    connection = connect()
    cursor = connection.cursor()
    print("into hostbd where been upvodscore:")
    print("idv:")
    print(idv)
    print("score:")
    print(score)
    first = "UPDATE vs SET score = %s WHERE idv = %s"
    second = (score, idv)
    cursor.execute(first, second)
    connection.commit()
    cursor.close()
    connection.close()


# DELETE VODOMAT
def delete_vodomat(idv):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE from vs where idv = %i" % (idv))
    connection.commit()
    cursor.close()
    connection.close()
    return True