figerScanPort = '/dev/ttyUSB1'
comport = '/dev/ttyUSB0'
delaySec = 2
lockerName = 'A'

# mysql config
#dbhost = '27.254.172.53'
#dbuser = 'testapp_locker'
#dbpassword = 'Sinetong9977'
#dbname = 'testapp_locker'

# mysql config local
dbhost = '192.168.1.49'
dbuser = 'locker'
dbpassword = 'Sinetong9977'
dbname = 'testapp_locker'

# no: (slaveID,chanel)
boxMap ={
  1: (1,3),
  2: (1,2),
  3: (1,1),
  4: (1,6),
  5: (1,7),
  6: (1,8),
  7: (2,3),
  8: (2,2),
  9: (2,1),
  10: (2,6),
  11: (2,7),
  12: (2,8),
  13: (3,3),
  14: (3,2),
  15: (3,1),
  16: (3,6),
  17: (3,7),
  18: (3,8),
  19: (4,3),
  20: (4,2),
  21: (4,1),
  22: (4,6),
  23: (4,7),
  24: (4,8),
  25: (5,3),
  26: (5,2),
  27: (5,1),
  28: (5,6),
  29: (5,7),
  30: (5,8),
  31: (6,3),
  32: (6,2),
  33: (6,1),
  34: (6,6),
  35: (6,7),
  36: (6,8),
  37: (7,3),
  38: (7,2),
  39: (7,1),
  40: (7,6),
  41: (7,7),
  42: (7,8),
  43: (8,3),
  44: (8,2),
  45: (8,1),
  46: (8,6),
  47: (8,7),
  48: (8,8)
}