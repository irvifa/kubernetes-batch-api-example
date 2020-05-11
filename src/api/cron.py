from crontab import CronSlices
from api.exceptions import CronNotationDoesNotValidExceptions


class Cron:
    def __init__(self, environment):
        """
            Example format: 0 */6 * * *
            At minute 0 past every 6th hour.
        """
        self.cron_notation = '0 {execution_time}{execution_period} * * *'

    def generate_cron_notation_from_datetime(
        self,
        execution_time=0,
        execution_period=24):
        """
        When we are creating a cronjob we can set the schedule this way.
        :param execution_time:
        :param execution_period:
        :return:
        """
        cron_notation = self.cron_notation
        if execution_time == 0 and execution_period != 24:
            cron_notation = cron_notation.format(
                execution_time='*/',
                execution_period=execution_period)
        if execution_period == 24:
            cron_notation = cron_notation.format(
                execution_time=execution_time,
                execution_period='')
        if CronSlices.is_valid(cron_notation):
            return cron_notation
        raise CronNotationDoesNotValidExceptions(e)
