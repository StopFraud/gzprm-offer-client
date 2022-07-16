import urllib.request, json, os,time,pika,re
import requests 
from colorama import Fore, Back, Style

def service_check(pip):
    proxies={'https':'http://'+pip,'http':'http://'+pip}
    #2do: add json hostname to dns
    good_proxy=1
    while good_proxy==1:


        url= urllib.request.urlopen("http://json.stopfraud.cyou:8000")
        data = json.loads(url.read().decode())

        try:
#            d1={'arfield': "field", 'form':"#callbackForm"}
 #           print (d1)
            r1 = requests.get('https://gzprm-offer.com/registration.php', proxies=proxies, timeout=15)
#            print (r1.text)
#            print (r1.status_code)
#            print(r1.headers)
#            sys.exit()
            php=(r1.headers["Set-Cookie"])
#            print(php)
            z=re.match(r'^PHPSESSID=(.*);.*$',php)
            phpsessid=""
            if z:
#                print(z.groups())
                phpsessid=z.groups()[0]

#            time.sleep(1)
#            cookies={'PHPSESSID':phpsessid,'path':'/'}
            cookies={'PHPSESSID':phpsessid}
#            print (cookies)
#            sys.exit()

#emaillenka777@yandex.ru
#nameElena
#passwordGg123456
#phone+794576543234
#surnameKuvshinina

            d1={'name':data['name'],'phone':data['phone_full'],'email':data['email'],'surname':data['surname'],'password':data['password']}

#            d1={'arfield': "code", 'form':"#callbackForm"}
#            print (d1)
            r1 = requests.post('https://gzprm-offer.com/assets/ajax/registration.php',data=d1,proxies=proxies, timeout=15,cookies=cookies)
#            print (r1.text)
#            print (r1.status_code)
#            print(r1.headers)

            d1={'phone':data['phone_full'],'email':data['email'],'textarea':data['phrase']}
#            print (d1)
            r1 = requests.get('https://gzprm-offer.com/help.php', proxies=proxies, cookies=cookies, params=d1, timeout=15)
#            print (r1.text)
#            print (r1.status_code)
#            print(r1.headers)
#            print (d1)

#            sys.exit()
#original
#            print ("{:<23} {:<44} {:<10} {}".format(Fore.WHITE+data["name"]+" "+data["surname"], Fore.YELLOW+data["email"],data["password"],Fore.GREEN+data["phrase"]+Fore.WHITE))


            print ("{:<23} {}".format(Fore.WHITE+data["name"]+" "+data["surname"]))
            print ("{:<25} {}".format(Fore.YELLOW+data["email"],data["password"]))
            print (Fore.GREEN+data["phrase"]+Fore.WHITE)
            print ("")       
#            time.sleep(1)


#arfield

            if ('<h2>Мы всегда рядом</h2>' in r1.text):
#                print ("req ok")
                good_proxy=1
            else:
                good_proxy=0
#            if good_proxy==1:
#                print('trying good proxy again '+ str(pip))
#            else:
#                print('proxy became bad, quit')
        except Exception as e:
            print (e)
            good_proxy=0
            pass

#service_check('170.39.194.16:3128')

#service_check('216.238.81.217:59394')
#sys.exit()
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    service_check(body.decode("utf-8"))


RABBITMQ_SERVER=os.getenv("RABBITMQ_SERVER")
RABBITMQ_USER=os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD=os.getenv("RABBITMQ_PASSWORD")



while True:

    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(RABBITMQ_SERVER,
                                       5672,
                                       '/',
                                       credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
#        channel.basic_qos(prefetch_count=1, global_qos=False)
        channel.queue_declare(queue='gzprm-offer')
        channel.basic_consume(queue='gzprm-offer', on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
#    except pika.exceptions.AMQPConnectionError:
#        print ("retry connecting to rabbit")
#        time.sleep(6)
    except Exception as e1:
        print (e1)
        print ("retry connecting to rabbit")
        time.sleep(6)
