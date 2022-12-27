from kafka import KafkaConsumer
from kafka.errors import KafkaError
import sys, time

bootstrap_servers = ['MACHINE_IP:30092', 'MACHINE_IP:30093']
topicName = 'test1'
consumer = KafkaConsumer (topicName, group_id='my-group-1',bootstrap_servers = bootstrap_servers, auto_offset_reset = 'earliest')
try:
    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
        time.sleep(0.1) #consumes 10 events per second 
except KeyboardInterrupt:
    sys.exit()