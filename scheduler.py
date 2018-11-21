import schedule
import time
import threading
import multiprocessing as mp
from REWE_split import download, delete

if __name__=='__main__':
    jobqueue = mp.Queue()


    def worker_main():
        while 1:
            job_func = jobqueue.get()
            job_func()

    schedule.every().monday.at('10:20').do(jobqueue.put, download)
    schedule.every().monday.at('10:20').do(jobqueue.put, delete)

    worker_thread = threading.Thread(target=worker_main)
    worker_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)
