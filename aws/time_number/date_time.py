import datetime

__all__ = ["get_utctime_one_year_ago"]

def _now():
    """ 获取当前utc时间

    :return:
    """
    return datetime.datetime.utcnow()


# RFC 3339格式日期字符串
RFC_fmt = '%Y-%m-%dT%H:%M:%S.000Z'


class _DataTime:
    """ 语义化date-time

    """
    @property
    def now(self):
        """ 调用当前时间

        :return:
        """
        return _now().strftime(RFC_fmt)

    @property
    def ten_minutes_ago(self):
        """ 调用时10分钟前

        :return:
        """
        return (_now() + datetime.timedelta(minutes=-10)).strftime(RFC_fmt)

    @property
    def one_day_ago(self):
        """ 调用时1天前

        :return:
        """
        return (_now() + datetime.timedelta(days=-1)).strftime(RFC_fmt)

    @property
    def one_week_ago(self):
        """ 调用时1周前

        :return:
        """
        return (_now() + datetime.timedelta(days=-7)).strftime(RFC_fmt)

    @property
    def one_year_ago(self):
        """ 调用时1年前

        :return:
        """
        return (_now() + datetime.timedelta(days=-365)).strftime(RFC_fmt)

    @property
    def ten_minutes_alter(self):
        """ 调用时10分钟后

        :return:
        """
        return (_now() + datetime.timedelta(days=+1)).strftime(RFC_fmt)

    @property
    def one_day_later(self):
        """ 调用时1天后

        :return:
        """
        return (_now() + datetime.timedelta(days=+1)).strftime(RFC_fmt)

    @property
    def one_week_later(self):
        """ 调用时1周后

        :return:
        """
        return (_now() + datetime.timedelta(days=+7)).strftime(RFC_fmt)

UTCDateTime = _DataTime()

def get_utctime_one_year_ago():
    """
    构造一年前的UTC时间
    :return:
    """
    UTCDateTime = _DataTime()
    return UTCDateTime.one_year_ago

if __name__=='__main__':
    print(get_utctime_one_year_ago())