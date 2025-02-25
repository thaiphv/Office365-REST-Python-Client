from office365.entity import Entity


class LinkedResource(Entity):
    """Represents an item in a partner application related to a todoTask. An example is an email from where the task
    was created. A linkedResource object stores information about that source application, and lets you link back to
    the related item. You can see the linkedResource in the task details view, as shown.
    """

    @property
    def application_name(self):
        """Field indicating the app name of the source that is sending the linkedResource.
        :rtype: str
        """
        return self.properties.get("applicationName", None)

    @property
    def display_name(self):
        """The title of the linkedResource..
        :rtype: str
        """
        return self.properties.get("displayName", None)
