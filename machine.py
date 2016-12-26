"""
Drop-in replacement for Python's standard 'datetime' package and/or class.

See README.txt for usage and discussion.
"""
import datetime as _datetime  # python's standard datetime module
import time as _time  # python's standard time module, needed for frozen time

# Attributes we just pass along from the standard datetime module:
MAXYEAR = _datetime.MAXYEAR
MINYEAR = _datetime.MINYEAR
# Not sure what this does, but let's pass it along anyway:
datetime_CAPI = _datetime.datetime_CAPI
# Classes that are passed-thru as-is:
time = _datetime.time
timedelta = _datetime.timedelta
tzinfo = _datetime.tzinfo

# Time machine control constants and variables:
_PRESENT_MODE = 0
_FROZEN_MODE = 1
_SHIFTED_MODE = 2
_mode = _PRESENT_MODE
# Frozen time variables:
_frozen_datetime = None
_frozen_utc_delta = None
# Shifted time variables:
_shifted_delta = None


def _is_present():
    global _mode
    return (_mode == _PRESENT_MODE)


def _is_frozen():
    global _mode
    return (_mode == _FROZEN_MODE)


def _is_shifted():
    global _mode
    return (_mode == _SHIFTED_MODE)


def return_to_present():
    """ Resets all time modes and resumes standard datetime operation. """
    global _mode
    global _frozen_datetime
    global _frozen_utc_delta
    global _shifted_delta
    _mode = _PRESENT_MODE
    _frozen_datetime = None
    _shifted_delta = None


def start_freeze_at_datetime(frozen):
    """
    Set the machine to a specific frozen time.
    The 'frozen' parameter should be expressed as a local system time, NOT a
    UTC time, unless the system clock is set to the UTC timezone.
    If frozen includes a tzinfo, that tzinfo will be ignored;
    in other words, the machine is time-zone ignorant, just like all the
    classmethods in the standard datetime package.
    """
    global _mode
    global _frozen_datetime
    global _frozen_utc_delta
    return_to_present()
    _mode = _FROZEN_MODE
    # VERY IMPORTANT: _frozen_datetime must be a standard python datetime!
    # Otherwise, you get recursion errors later.
    _frozen_datetime = _datetime.datetime(
        frozen.year, frozen.month, frozen.day,
        frozen.hour, frozen.minute, frozen.second,
        frozen.microsecond)
    # Base UTC offset on the current system offset; it's not as accurate as
    # it could be, esp. for some frozen dates, but we're kinda stuck.
    # We could use pytz to implement a more elegant solution, but let's see
    # what happens for now.
    if _time.daylight == 1:
        _frozen_utc_delta = timedelta(seconds=_time.altzone)
    else:
        _frozen_utc_delta = timedelta(seconds=_time.timezone)


def start_freeze_by_delta(delta):
    """ Enter frozen time mode based on delta from current system time. """
    calculated = _datetime.datetime.now() + delta
    start_freeze_at_datetime(calculated)


def start_freeze_now():
    """ Enter frozen time mode at current system time. """
    start_freeze_at_datetime(_datetime.datetime.now())


def move_freeze_by_delta(delta):
    """ Add delta to the frozen datetime. """
    global _mode
    global _frozen_datetime
    assert (_mode == _FROZEN_MODE), 'Cannot increment unless in frozen mode!'
    _frozen_datetime = _frozen_datetime + delta


def start_shift_by_delta(delta):
    """ Enter shifted time mode based on delta from current system time. """
    global _mode
    global _shifted_delta
    _mode = _SHIFTED_MODE
    _shifted_delta = delta


def start_shift_at_datetime(shifted_datetime):
    """
    Set the machine to shifted time mode, starting at shifted_datetime.
    The 'shifted_datetime' parameter should be expressed as a local system
    time, NOT a UTC time, unless the system clock is set to the UTC timezone.
    """
    calcdelta = shifted_datetime - _datetime.datetime.now()
    start_shift_by_delta(calcdelta)


# Our own classes that override the standard datetime module:
# NOTE: I hope this doesn't mess up the object signatures, if anyone is checking.
class datetime(_datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        if _is_frozen():
            return _frozen_datetime  # Accomodate tz?
        elif _is_shifted():
            return _datetime.datetime.now(tz) + _shifted_delta
        else:
            return _datetime.datetime.now(tz)

    @classmethod
    def today(cls):
        if _is_frozen():
            return _frozen_datetime
        elif _is_shifted():
            return _datetime.datetime.today() + _shifted_delta
        else:
            return _datetime.datetime.today()

    @classmethod
    def utcnow(cls):
        if _is_frozen():
            return _frozen_datetime + _frozen_utc_delta
        elif _is_shifted():
            return _datetime.datetime.utcnow() + _shifted_delta
        else:
            return _datetime.datetime.utcnow()


class date(_datetime.date):
    @classmethod
    def today(cls):
        rpt = datetime.today()
        # Return report_date as a date:
        report_date = date(rpt.year, rpt.month, rpt.day)
        return report_date


def _proof(when):
    print("@ %s:") % when
    print("date.today()      :", date.today())
    print("datetime.today()  :", datetime.today())
    print("datetime.now()    :", datetime.now())
    print("datetime.utcnow() :", datetime.utcnow())


def _sanity_check():
    # This is some proof-of-concept code.
    _proof('Present')
    start_freeze_at_datetime(datetime(2010, 12, 25, 23, 45, 56))
    _proof('Frozen')
    start_shift_by_delta(timedelta(days=-5))
    _proof('Shifted')


if __name__ == "__main__":
    _sanity_check()
