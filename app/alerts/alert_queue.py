from queue import Queue

alert_queue = Queue()

def push_alert(alert):

    # print("PUSHING ALERT TO QUEUE:", alert)

    alert_queue.put(alert)