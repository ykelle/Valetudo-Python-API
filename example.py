import time
from valetudo import Valetudo, ValetudoError

# Create an object with the ip of your vacuum robot
robo = Valetudo(ip='192.168.XXX.xxx')

try:
    value = robo.set_volume(100)
    print(value)

    value = robo.get_volume()
    print(value)

    value = robo.start_cleaning()
    print(value)

    time.sleep(5)

    value = robo.stop_cleaning()
    print(value)

except ValetudoError as e:
    print(e)
