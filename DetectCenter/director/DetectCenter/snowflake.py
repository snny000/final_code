# -*- coding: utf-8 -*-

import time
import threading


sequence = 0L

twepoch = 1288834974657L

worker_id_bits = 5L
datacenter_id_bits = 5L
max_worker_id = -1L ^ (-1L << worker_id_bits)
max_datacenter_id = -1L ^ (-1L << datacenter_id_bits)
sequence_bits = 12L

worker_id_shift = sequence_bits
datacenter_id_shift = sequence_bits + worker_id_bits
timestamp_left_shift = sequence_bits + worker_id_bits + datacenter_id_bits
sequence_mask = -1L ^ (-1L << sequence_bits)

last_timestamp = -1L

lock = threading.Lock()


def til_next_millis(last_time_stamp):
    timestamp = int(time.time() * 1000)
    while timestamp <= last_time_stamp:
        timestamp = int(time.time() * 1000)
    return timestamp


def next_id(datacenter_id, worker_id):
    global sequence, twepoch, worker_id_bits, datacenter_id_bits, max_worker_id, \
           max_datacenter_id, sequence_bits, worker_id_shift, datacenter_id_shift, \
           timestamp_left_shift, sequence_mask, last_timestamp
    lock.acquire()
    try:
        timestamp = int(time.time() * 1000)
        if timestamp < last_timestamp:
            raise ValueError("Clock moved backwards. Refusing to generate id for %d milliseconds" % (last_timestamp - timestamp))
        if last_timestamp == timestamp:
            sequence = (sequence + 1) & sequence_mask
            if sequence == 0:
                timestamp = til_next_millis(last_timestamp)
        else:
            sequence = 0L

        last_timestamp = timestamp

        unique_id = ((timestamp - twepoch) << timestamp_left_shift) | (datacenter_id << datacenter_id_shift) | (worker_id << worker_id_shift) | sequence
        #print unique_id
        return unique_id
    finally:
        lock.release()

if __name__ == '__main__':
    #t1 = threading.Thread(target=next_id, args=(0, 0))
    #t2 = threading.Thread(target=next_id, args=(0, 1))
    #t1.start()
    #t2.start()
    #t1.join()
    #t2.join()
    for i in range(100):
        print next_id(0, 0)
