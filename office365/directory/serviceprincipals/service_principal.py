from typing import Optional

from office365.delta_collection import DeltaCollection
from office365.directory.applications.roles.assignment_collection import (
    AppRoleAssignmentCollection,
)
from office365.directory.applications.roles.role import AppRole
from office365.directory.certificates.self_signed import SelfSignedCertificate
from office365.directory.key_credential import KeyCredential
from office365.directory.object import DirectoryObject
from office365.directory.object_collection import DirectoryObjectCollection
from office365.directory.password_credential import PasswordCredential
from office365.directory.permissions.grants.oauth2 import OAuth2PermissionGrant
from office365.directory.permissions.scope import PermissionScope
from office365.directory.synchronization.synchronization import Synchronization
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection


class ServicePrincipal(DirectoryObject):
    """Represents an instance of an application in a directory."""

    def add_key(self, key_credential, password_credential, proof):
        """
        Adds a key credential to a servicePrincipal. This method along with removeKey can be used by a servicePrincipal
        to automate rolling its expiring keys.

        :param KeyCredential key_credential: The new application key credential to add.
            The type, usage and key are required properties for this usage. Supported key types are:
                AsymmetricX509Cert: The usage must be Verify.
                X509CertAndPassword: The usage must be Sign
        :param PasswordCredential password_credential: Only secretText is required to be set which should contain the password
             for the key. This property is required only for keys of type X509CertAndPassword. Set it to null otherwise.
        :param str proof: A self-signed JWT token used as a proof of possession of the existing keys
        """
        payload = {
            "keyCredential": key_credential,
            "passwordCredential": password_credential,
            "proof": proof,
        }
        return_type = ClientResult(self.context, KeyCredential())
        qry = ServiceOperationQuery(self, "addKey", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def add_password(self, display_name=None):
        """Adds a strong password to an application.

        :param str display_name: App display name
        """
        params = PasswordCredential(display_name=display_name)
        return_type = ClientResult(self.context, params)
        qry = ServiceOperationQuery(
            self, "addPassword", None, params, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def add_token_signing_certificate(self, display_name, end_datetime=None):
        """
        Create a self-signed signing certificate and return a selfSignedCertificate object, which is the public part
        of the generated certificate.

        The self-signed signing certificate is composed of the following objects,
        which are added to the servicePrincipal:

          The keyCredentials object with the following objects:
              A private key object with usage set to Sign.
              A public key object with usage set to Verify.
              The passwordCredentials object.
        All the objects have the same value of customKeyIdentifier.

        The passwordCredential is used to open the PFX file (private key). It and the associated private key object
        have the same value of keyId. When set during creation through the displayName property, the subject of the
        certificate cannot be updated. The startDateTime is set to the same time the certificate is created using
        the action. The endDateTime can be up to three years after the certificate is created.

        :param str display_name: Friendly name for the key. It must start with CN=.
        :param str end_datetime: The date and time when the credential expires. It can be up to 3 years from the date
            the certificate is created. If not supplied, the default is three years from the time of creation.
            The timestamp type represents date and time information using ISO 8601 format and is always in UTC time.
            For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z.
        """
        payload = {"displayName": display_name, "endDateTime": end_datetime}
        return_type = ClientResult(self.context, SelfSignedCertificate())
        qry = ServiceOperationQuery(
            self, "addTokenSigningCertificate", None, payload, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def remove_password(self, key_id):
        """
        Remove a password from a servicePrincipal object.
        :param str key_id: The unique identifier for the password.
        """
        qry = ServiceOperationQuery(self, "removePassword", None, {"keyId": key_id})
        self.context.add_query(qry)
        return self

    @property
    def account_enabled(self):
        # type: () -> Optional[bool]
        """
        true if the service principal account is enabled; otherwise, false. If set to false, then no users will be
        able to sign in to this app, even if they are assigned to it. Supports $filter (eq, ne, not, in).
        """
        return self.properties.get("accountEnabled", None)

    @property
    def alternative_names(self):
        """
        Used to retrieve service principals by subscription, identify resource group and full resource ids for
        managed identities. Supports $filter (eq, not, ge, le, startsWith).
        """
        return self.properties.get("alternativeNames", StringCollection())

    @property
    def app_description(self):
        # type: () -> Optional[str]
        """
        The description exposed by the associated application.
        """
        return self.properties.get("appDescription", None)

    @property
    def app_display_name(self):
        # type: () -> Optional[str]
        """
        The display name exposed by the associated application.
        """
        return self.properties.get("appDisplayName", None)

    @property
    def app_role_assigned_to(self):
        """
        App role assignments for this app or service, granted to users, groups, and other service principals.
        Supports $expand."""
        return self.properties.get(
            "appRoleAssignedTo",
            AppRoleAssignmentCollection(
                self.context, ResourcePath("appRoleAssignedTo", self.resource_path)
            ),
        )

    @property
    def app_roles(self):
        """
        The roles exposed by the application which this service principal represents.
        """
        return self.properties.get("appRoles", ClientValueCollection(AppRole))

    @property
    def homepage(self):
        # type: () -> Optional[str]
        """
        Home page or landing page of the application.
        """
        return self.properties.get("homepage", None)

    @property
    def key_credentials(self):
        """
        The collection of key credentials associated with the service principal. Not nullable.
        Supports $filter (eq, not, ge, le).
        """
        return self.properties.setdefault(
            "keyCredentials", ClientValueCollection(KeyCredential)
        )

    @property
    def login_url(self):
        # type: () -> Optional[str]
        """
        Specifies the URL where the service provider redirects the user to Azure AD to authenticate.
        Azure AD uses the URL to launch the application from Microsoft 365 or the Azure AD My Apps. When blank,
        Azure AD performs IdP-initiated sign-on for applications configured with SAML-based single sign-on.
        The user launches the application from Microsoft 365, the Azure AD My Apps, or the Azure AD SSO URL.
        """
        return self.properties.get("loginUrl", None)

    @property
    def logout_url(self):
        """
        Specifies the URL that will be used by Microsoft's authorization service to logout an user using
        OpenId Connect front-channel, back-channel or SAML logout protocols.
        :rtype: str
        """
        return self.properties.get("logoutUrl", None)

    @property
    def notification_email_addresses(self):
        """
        Specifies the list of email addresses where Azure AD sends a notification when the active certificate is near
        the expiration date. This is only for the certificates used to sign the SAML token issued for Azure
        AD Gallery applications.
        """
        return self.properties.get("notificationEmailAddresses", StringCollection())

    @property
    def service_principal_type(self):
        """
        Identifies whether the service principal represents an application, a managed identity, or a legacy application.
        This is set by Azure AD internally. The servicePrincipalType property can be set to three different values:
            Application - A service principal that represents an application or service.
            The appId property identifies the associated app registration, and matches the appId of an application,
            possibly from a different tenant. If the associated app registration is missing, tokens are not issued
            for the service principal.

            ManagedIdentity - A service principal that represents a managed identity. Service principals
            representing managed identities can be granted access and permissions, but cannot be updated
            or modified directly.

            Legacy - A service principal that represents an app created before app registrations,
            or through legacy experiences. Legacy service principal can have credentials, service principal names,
            reply URLs, and other properties which are editable by an authorized user,
            but does not have an associated app registration. The appId value does not associate
            the service principal with an app registration.
            The service principal can only be used in the tenant where it was created.

        :rtype: str or None
        """
        return self.properties.get("servicePrincipalType", None)

    @property
    def owners(self):
        """Directory objects that are owners of this servicePrincipal.
        The owners are a set of non-admin users or servicePrincipals who are allowed to modify this object.
        """
        return self.properties.get(
            "owners",
            DirectoryObjectCollection(
                self.context, ResourcePath("owners", self.resource_path)
            ),
        )

    @property
    def oauth2_permission_scopes(self):
        """
        The delegated permissions exposed by the application. For more information see the oauth2PermissionScopes
        property on the application entity's api property.
        """
        return self.properties.get(
            "oauth2PermissionScopes", ClientValueCollection(PermissionScope)
        )

    @property
    def oauth2_permission_grants(self):
        """"""
        return self.properties.get(
            "oauth2PermissionGrants",
            DeltaCollection(
                self.context,
                OAuth2PermissionGrant,
                ResourcePath("oauth2PermissionGrants", self.resource_path),
            ),
        )

    @property
    def created_objects(self):
        """Directory objects created by this service principal."""
        return self.properties.get(
            "createdObjects",
            DirectoryObjectCollection(
                self.context, ResourcePath("createdObjects", self.resource_path)
            ),
        )

    @property
    def owned_objects(self):
        """Directory objects that are owned by this service principal."""
        return self.properties.get(
            "ownedObjects",
            DirectoryObjectCollection(
                self.context, ResourcePath("ownedObjects", self.resource_path)
            ),
        )

    @property
    def synchronization(self):
        """
        Represents the capability for Azure Active Directory (Azure AD) identity synchronization through
        the Microsoft Graph API.
        """
        return self.properties.get(
            "synchronization",
            Synchronization(
                self.context, ResourcePath("synchronization", self.resource_path)
            ),
        )

    @property
    def token_encryption_key_id(self):
        """
        Specifies the keyId of a public key from the keyCredentials collection. When configured, Azure AD issues tokens
        for this application encrypted using the key specified by this property. The application code that receives
        the encrypted token must use the matching private key to decrypt the token before it can be used
        for the signed-in user.
        """
        return self.properties.get("tokenEncryptionKeyId", None)

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "appRoles": self.app_roles,
                "appRoleAssignedTo": self.app_role_assigned_to,
                "created_objects": self.created_objects,
                "keyCredentials": self.key_credentials,
                "oauth2PermissionScopes": self.oauth2_permission_scopes,
                "ownedObjects": self.owned_objects,
                "oauth2PermissionGrants": self.oauth2_permission_grants,
            }
            default_value = property_mapping.get(name, None)
        return super(ServicePrincipal, self).get_property(name, default_value)
