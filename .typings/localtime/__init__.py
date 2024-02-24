class LocalTime:
    """
    LocalTime class is a class to manage time in MicroPython.

    This class is used to set time with NTP, get time from RTC, get epoch time from RTC,
    and get localized time from epoch time.
    """
    def __init__(self, timezone: int):
        """
        Initialize LocalTime class with timezone.

        Example:
        ```
        localtime = LocalTime(7)
        ```
        """
        ...

    def set_time(self):
        """
        GET UTC time from NTP. Then, set it to RTC with timezone.
        """
        ...

    def current_time(self, epoch_time=None|int):
        """
        Get current time from RTC.

        If epoch_time defined, then get localized time from epoch_time.
        Ensure that epoch_time is in UTC and not in UNIX epoch time.

        Example:
        ```
        localtime.current_time() # (2021, 1, 7, 4, 0, 0, 3, 7)
        localtime.current_time(1610000000) # (2021, 1, 7, 11, 0, 0, 3, 7)
        ```
        """
        ...

    def current_epoch_time(self, epoch_time=None|int):
        """
        Get epoch time from RTC.

        If epoch_time defined, then localized epoch_time.
        Ensure that epoch_time is in UTC and not in UNIX epoch time.

        Example:
        ```
        localtime.current_epoch_time() # 1610000000
        localtime.current_epoch_time(1610000000)
        ```
        """
        ...

    def strf_current_date(self) -> str:
        """
        Get current date in string format.

        Example:
        ```
        localtime.strf_current_date() # "2021-1-7"
        ```
        """
        ...

    def strf_current_time(self) -> str:
        """
        Get current time in string format.

        Example:
        ```
        localtime.strf_current_time() # "11:0:0"
        ```
        """
        ...
    
    def strf_current_datetime(self) -> str:
        """
        Get current datetime in string format.

        Example:
        ```
        localtime.strf_current_datetime() # "2021-1-7 11:0:0"
        ```
        """
        ...
