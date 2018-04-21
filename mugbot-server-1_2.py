#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import time
import os
import commands
import tornado.ioloop
import tornado.web
import tornado.websocket
import sys
import socket

SERIALPORT = ["ACM0", "USB0"]

cl=[]

# 読み上げ
def speak(msg):
    print "speaking ... " + msg
    os.system('/home/pi/mugbot-talk-1.1.sh ' + msg )
    print "speak end"

def ip_speak():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    speak("IPアドレスは、" + s.getsockname()[0] + "です。")
    s.close()

#クライアントからメッセージを受けるとopen → on_message → on_closeが起動する
class WebSocketHandler(tornado.websocket.WebSocketHandler):

    #websocketチェックオリジン
    def check_origin(self, origin):
        print "origin"
        return True 

    #websocketオープン
    def open(self):
        print "open"
        speak("ネットワークに接続しました")
        ip_speak()
        if self not in cl:
            cl.append(self)
 
    #処理
    def on_message(self, message):
        print "on_message"
        msg = message.encode('utf-8')
        for client in cl:
            print msg
            if( msg[0:2] == "@x" ):
              ans = msg[2:len(msg)]
              sp.write(ans + 'x')
              time.sleep(0.01)
              #目の上下のアクション
              #最初の2文字が@xであればその2文字を取り除いてxの値をArduinoに送信
            elif( msg[0:2] == "@y" ):
              ans = msg[2:len(msg)]
              sp.write(ans + 'y')
              time.sleep(0.01)
              #首の左右のアクション
              #最初の2文字が@yであればその2文字を取り除いてyの値をArduinoに送信
            elif( msg[0:2] == "@z" ):
              ans = msg[2:len(msg)]
              sp.write(ans + 'z')
              time.sleep(0.01)
              #目の明るさ変調のアクション
              #最初の2文字が@zであればその2文字を取り除いてzの値をArduinoに送信
            elif( msg[0:1]=="@" ):
              ans = msg[1]
              sp.write(ans)
              time.sleep(0.01)
              #最初の1文字が@であれば@を取り除いてアクションを指示するアルファベット1文字をArduinoに送信
            else:
              if msg == "そのとおりです":
	        speak("リブートします")
                os.system('sudo reboot')
              elif msg == "さようなら":
	        speak("シャットダウンします")
                os.system('sudo halt')
              sp.write("t")
	      speak(msg)
              sp.write("k")
              # tをArduinoに送って口の点滅開始、発話させ、kを送って点滅終了

    #websockeクローズ
    def on_close(self):
        print "close"
        speak("ネットワークが切断されました")
        if self in cl:
            cl.remove(self)

app = tornado.web.Application([
    (r"/", WebSocketHandler)
])

if __name__ == "__main__":
  speak("マグボットを起動します")
  head = '/dev/tty'
#  str = head + 'ttyACM0'
#  sp = serial.Serial(str, 9600)
#  str = head + 'ttyUSB0'
#  sp = serial.Serial(str, 9600)
  pot = 0
  while 1:
    try:
      portstr = SERIALPORT[pot]
      str = head + portstr
      sp = serial.Serial(str, 9600)
      break;
    except:
      pot = pot + 1
      if pot == 2:
        break;
  speak("ＵＳＢは" + portstr + "で接続しました")
  app.listen(51234)
  ip_speak()
  tornado.ioloop.IOLoop.instance().start()



