import machine, ntptime, time

class LocalTime:
    def __init__(self, timezone: int):
        self.timezone = timezone*3600
        self.rtc = machine.RTC()

    def set_time(self):
        ntptime.settime()
        tm = time.localtime(time.mktime(time.localtime()) + self.timezone)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        return self.rtc.datetime(tm)

    def current_time(self, epoch_time=None):
        if epoch_time is None:
            return time.localtime()
        else:
            return time.localtime(self.__to_local_epoch(epoch_time))

    def current_epoch_time(self, epoch_time=None):
        if epoch_time is None:
            return time.mktime(self.current_time())
        else:
            return self.__to_local_epoch(epoch_time)

    def strf_current_date(self):
        time = self.current_time()
        return "{}-{}-{}".format(time[0], time[1], time[2])

    def strf_current_time(self):
        time = self.current_time()
        return "{}:{}:{}".format(time[3], time[4], time[5])
    
    def strf_current_datetime(self):
        time = self.current_time()
        return "{}-{}-{} {}:{}:{}".format(time[0], time[1], time[2], time[3], time[4], time[5])

    def __to_local_epoch(self, epoch_time: int):
        return epoch_time + self.timezone
