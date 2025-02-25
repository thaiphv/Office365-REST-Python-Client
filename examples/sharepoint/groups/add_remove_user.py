"""
Adds and removes site group

"""
from office365.sharepoint.client_context import ClientContext
from tests import create_unique_name, test_password, test_site_url, test_username

ctx = ClientContext(test_site_url).with_user_credentials(test_username, test_password)
group_name = create_unique_name("Group")
group = ctx.web.site_groups.add(group_name).execute_query()
# clean up temporary resources
group.delete_object().execute_query()
