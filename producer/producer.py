from kafka import KafkaProducer
import time

bootstrap_servers = ['MACHINE_IP:30092', 'MACHINE_IP:30093']
topicName = 'test1'

producer = KafkaProducer(bootstrap_servers = bootstrap_servers)

while True:
    epoch_time = int(time.time())
    ack = producer.send(topicName, bytes('Time is : '+str(epoch_time), 'utf8') )
    metadata = ack.get()
    print(metadata.topic)
    print(metadata.partition)
    time.sleep(0.05) #produces 20 events per second