from office365.runtime.client_value import ClientValue


class RecurrenceRange(ClientValue):
    """
    Describes a date range over which a recurring event. This shared object is used to define the recurrence
    of access reviews, calendar events, and access package assignments in Azure AD.
    """

    def __init__(
        self,
        start_date=None,
        end_date=None,
        number_of_occurrences=None,
        recurrence_timezone=None,
        range_type=None,
    ):
        """
        :param datetime.date start_date: The date to start applying the recurrence pattern. The first occurrence of
            the meeting may be this date or later, depending on the recurrence pattern of the event. Must be the
            same value as the start property of the recurring event. Required.
        :param datetime.date end_date: The date to stop applying the recurrence pattern. Depending on the recurrence pattern of
            the event, the last occurrence of the meeting may not be this date. Required if type is endDate.
        :param int number_of_occurrences: The number of times to repeat the event. Required and must be positive
            if type is numbered.
        :param str recurrence_timezone: Time zone for the startDate and endDate properties. Optional. If not specified,
            the time zone of the event is used.
        :param str range_type: The recurrence range. The possible values are: endDate, noEnd, numbered. Required.
        """
        self.endDate = end_date
        self.numberOfOccurrences = number_of_occurrences
        self.recurrenceTimeZone = recurrence_timezone
        self.startDate = start_date
        self.type = range_type
