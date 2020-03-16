#! /usr/bin/env python
"""Performs (incremental) backups of activities for a given Garmin Connect
account.
The activities are stored in a local directory on the user's computer.
The backups are incremental, meaning that only activities that aren't already
stored in the backup directory will be downloaded.
"""

from datetime import timedelta

from garminexport.chinagarminclient import ChinaGarminClient
from garminexport.garminclient import GarminClient
import garminexport.backup

from garminexport.retryer import (
    Retryer, ExponentialBackoffDelayStrategy, MaxRetriesStopStrategy)
import logging
import os


logging.basicConfig(
    level=logging.INFO, format="%(asctime)-15s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR
}
"""Command-line (string-based) log-level mapping to logging module levels."""

DEFAULT_MAX_RETRIES = 7
"""The default maximum number of retries to make when fetching a single activity."""

format_suffix = {
    "json_summary": "_summary.json",
    "json_details": "_details.json",
    "gpx": ".gpx",
    "tcx": ".tcx",
    "fit": ".fit"
}

USER_NAME = "email"
PASSWORD = "password"
PATH = "file_path"
#加载个人的账号密码信息,这里国际版和国内版需要保持一致
from user_info import USER_NAME, PASSWORD,PATH


def export_filename(activity, export_format):
    """Returns a destination file name to use for a given activity that is
    to be exported to a given format. Exported files follow this pattern:
      ``<timestamp>_<activity_id>_<suffix>``.
    For example: ``2015-02-17T05:45:00+00:00_123456789.tcx``

    :param activity: An activity tuple `(id, starttime)`
    :type activity: tuple of `(int, datetime)`
    :param export_format: The export format (see :attr:`export_formats`)
    :type export_format: str

    :return: The file name to use for the exported activity.
    :rtype: str
    """
    fn = "{time}_{id}{suffix}".format(
        id=activity[0],
        time=activity[1].isoformat(),
        suffix=format_suffix[export_format])
    return fn.replace(':', '_') if os.name == 'nt' else fn


def sync():
    retryer = Retryer(
        delay_strategy=ExponentialBackoffDelayStrategy(
            initial_delay=timedelta(seconds=1)),
        stop_strategy=MaxRetriesStopStrategy(3))

    with ChinaGarminClient(USER_NAME, PASSWORD) as china_client:
        # get all activity ids and timestamps from Garmin account
        log.info("scanning activities for %s ...", USER_NAME)
        activities = set(retryer.call(china_client.list_activities))
        log.info("account has a total of %d activities", len(activities))

        missing_activities = garminexport.backup.need_backup(
            activities, PATH, ["fit"])
        backed_up = activities - missing_activities
        log.info("%s contains %d backed up activities",
                 PATH, len(backed_up))

        log.info("activities that aren't backed up: %d",
                 len(missing_activities))

        for index, activity in enumerate(missing_activities):
            id, start = activity
            log.info("backing up activity %d from %s (%d out of %d) ..." % (
                id, start, index + 1, len(missing_activities)))
            try:
                garminexport.backup.download(
                    china_client, activity, retryer, PATH,
                    ["fit"])
            except Exception as e:
                log.error(u"failed with exception: %s", e)
                if not True:
                    raise
        with GarminClient(USER_NAME, PASSWORD) as client:
            for index, activity in enumerate(missing_activities):
                dest = os.path.join(
                    PATH, export_filename(activity, 'fit'))
                log.info("uploading activity file {}".format(dest))
                try:
                    id = client.upload_activity(dest, name=None, description=None,
                                                private=True, activity_type="fit")
                except Exception as e:
                    log.error("upload failed: {!r}".format(e))
                else:
                    log.info("upload successful: https://connect.garmin.com/modern/activity/{}".format(id))


sync()