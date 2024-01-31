__package__ = "src"

import os
import pytest
import time

from dotenv import load_dotenv

from health_ping import HealthPing
from _datetime_utils import get_timezone_offset
from _exceptions import CronScheduleException
from _exceptions import EmptyUrlException
from _exceptions import InvalidTimezoneException

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

TEST_URL = os.getenv("TEST_URL")
EXECUTION_TEST_STRING = "HealthPing job executed at"
PRE_FIRE_FUNCTION_TEST_STRING = "Pre-fire called!"
POST_FIRE_FUNCTION_TEST_STRING = "Post-fire called!"
UTC_TIMEZONE_PLUS_8 = "UTC+08:00"
UTC_TIMEZONE_MINUS_5 = "UTC-05:00"
EVERY_HOUR_SCHEDULE = "0 * * * *"
EVERY_SECOND_SCHEDULE = "* * * * * * *"


def pre_fire_function():
    """
    Simple pre-fire function that prints a message for assertion in tests.
    """
    print(PRE_FIRE_FUNCTION_TEST_STRING)


def post_fire_function():
    """
    Simple post-fire function that prints a message for assertion in tests.
    """
    print(POST_FIRE_FUNCTION_TEST_STRING)


def test_health_ping_fire(caplog):
    """
    Checks if a health ping is fired immediately.
    """
    health_ping = HealthPing(url=TEST_URL, debug=True)
    health_ping.fire()
    assert EXECUTION_TEST_STRING in caplog.text


def test_health_ping_schedule(caplog):
    """
    Checks if a health ping is fired on schedule.
    """
    health_ping = HealthPing(url=TEST_URL,
                             schedule=EVERY_SECOND_SCHEDULE,
                             debug=True)
    health_ping.start()
    time.sleep(2)
    health_ping.stop()
    assert EXECUTION_TEST_STRING in caplog.text


def test_fail_should_not_stop_schedule(caplog):
    """
    Checks if a health ping schedule continues even after failure.
    """
    health_ping = HealthPing(url=TEST_URL + "FAIL",
                             schedule=EVERY_SECOND_SCHEDULE,
                             debug=True)
    health_ping.start()
    time.sleep(3)
    health_ping.stop()
    assert caplog.text.count(EXECUTION_TEST_STRING) > 1


def test_health_ping_stop(caplog):
    """
    Checks if a health ping is stopped timely.
    """
    health_ping = HealthPing(url=TEST_URL,
                             schedule=EVERY_SECOND_SCHEDULE,
                             debug=True)
    health_ping.start()
    health_ping.stop()
    assert EXECUTION_TEST_STRING not in caplog.text


def test_health_ping_retries(caplog):
    """
    Checks if a health ping retries on fail.
    """
    health_ping = HealthPing(url=TEST_URL + "FAIL",
                             schedule=EVERY_SECOND_SCHEDULE,
                             retries=[0.1, 0.2, 0.4],
                             debug=True)
    health_ping.start()
    time.sleep(3)
    health_ping.stop()
    assert caplog.text.count(EXECUTION_TEST_STRING) >= 4


def test_health_ping_pre_fire(capfd):
    """
    Checks if pre fire function is called after an execution.
    """
    health_ping = HealthPing(url=TEST_URL,
                             schedule=EVERY_SECOND_SCHEDULE,
                             pre_fire=pre_fire_function,
                             debug=True)
    health_ping.start()
    health_ping.stop()
    captured = capfd.readouterr()
    assert PRE_FIRE_FUNCTION_TEST_STRING not in captured.out


def test_health_ping_post_fire(capfd):
    """
    Checks if post fire is called after an execution.
    """
    health_ping = HealthPing(url=TEST_URL,
                             schedule=EVERY_SECOND_SCHEDULE,
                             post_fire=post_fire_function,
                             debug=True)
    health_ping.start()
    health_ping.stop()
    captured = capfd.readouterr()
    assert POST_FIRE_FUNCTION_TEST_STRING not in captured.out


def test_health_ping_result_success():
    """
    Checks if a health ping result succeeded.
    """
    health_ping = HealthPing(url=TEST_URL,
                             schedule=EVERY_SECOND_SCHEDULE)
    health_ping.start()
    time.sleep(2)
    health_ping.stop()
    assert health_ping.result.success is True


def test_health_ping_result_fail():
    """
    Checks if a health ping result failed.
    """
    health_ping = HealthPing(url=TEST_URL + "FAIL",
                             schedule=EVERY_SECOND_SCHEDULE)
    health_ping.start()
    time.sleep(2)
    health_ping.stop()
    assert health_ping.result.success is False


def test_can_do_logging():
    """
    Checks if logging can be done.
    """
    log_file = "./tests/test.log"
    health_ping = HealthPing(url=TEST_URL + "FAIL",
                             schedule=EVERY_SECOND_SCHEDULE,
                             log_file=log_file)
    health_ping.start()
    time.sleep(2)
    health_ping.stop()
    assert os.path.exists(log_file)
    assert os.path.getsize(log_file) > 0


def test_timezone_offset_correctness():
    """
    Checks if timezone offset is calculated correctly.
    """
    log_file = "./tests/test.log"
    health_ping_1 = HealthPing(url=TEST_URL + "FAIL",
                               timezone=UTC_TIMEZONE_PLUS_8,
                               schedule=EVERY_HOUR_SCHEDULE,
                               log_file=log_file)
    health_ping_2 = HealthPing(url=TEST_URL + "FAIL",
                               timezone=UTC_TIMEZONE_MINUS_5,
                               schedule=EVERY_HOUR_SCHEDULE,
                               log_file=log_file)
    health_ping_1.start()
    health_ping_2.start()
    time_difference = health_ping_1.next_time() - health_ping_2.next_time()
    # accounts for +-1 second difference
    assert time_difference.seconds >= 46799


def test_empty_url_not_allowed():
    """
    Throws exception if url is empty.
    """
    with pytest.raises(EmptyUrlException):
        HealthPing(url="",
                   schedule=EVERY_SECOND_SCHEDULE,
                   post_fire=post_fire_function,
                   debug=True).start()


def test_invalid_schedule():
    """
    Throws exception if invalid cron schedule is passed in.
    """
    with pytest.raises(CronScheduleException):
        HealthPing(url=TEST_URL,
                   schedule="SCHEDULE").start()


def test_invalid_timezone():
    """
    Throws exception if invalid timezone is passed in.
    """
    with pytest.raises(InvalidTimezoneException):
        HealthPing(url=TEST_URL,
                   timezone="TIMEZONE")


def test_get_timezone_offset():
    """
    Checks if correct timezone offsets are given.
    """
    assert get_timezone_offset(UTC_TIMEZONE_PLUS_8) == 28800
    assert get_timezone_offset(UTC_TIMEZONE_MINUS_5) == -18000
