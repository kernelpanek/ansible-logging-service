###############################################################################
# LDAP AUTHENTICATION SETTINGS
###############################################################################

import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion
from django_auth_ldap.config import NestedGroupOfNamesType

# LDAP server URI, such as "ldap://ldap.example.com:389" (non-SSL) or
# "ldaps://ldap.example.com:636" (SSL).  LDAP authentication is disabled if this
# parameter is empty.

AUTH_LDAP_SERVER_URI = 'ldaps://apu-svc-ipa01.useast.tni01.com:636'

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER
}

# DN (Distinguished Name) of user to bind for all search queries. Normally in the format
# "CN=Some User,OU=Users,DC=example,DC=com" but may also be specified as
# "DOMAIN\username" for Active Directory. This is the system user account
# we will use to login to query LDAP for other user information.

AUTH_LDAP_BIND_DN = 'uid=atower,cn=users,cn=accounts,dc=tni01,dc=com'

# Password using to bind above user account.

AUTH_LDAP_BIND_PASSWORD = '8675309AT!#'

# Whether to enable TLS when the LDAP connection is not using SSL.

AUTH_LDAP_START_TLS = False

# LDAP search query to find users.  Any user that matches the pattern
# below will be able to login to AWX.  The user should also be mapped
# into an AWX organization (as defined later on in this file).  If multiple
# search queries need to be supported use of "LDAPUnion" is possible. See
# python-ldap documentation as linked at the top of this section.

AUTH_LDAP_USER_SEARCH = LDAPSearch(
    'cn=users,cn=accounts,dc=tni01,dc=com',  # Base DN
    ldap.SCOPE_SUBTREE,  # SCOPE_BASE, SCOPE_ONELEVEL, SCOPE_SUBTREE
    '(uid=%(user)s)',  # Query
)

# Alternative to user search, if user DNs are all of the same format. This will be
# more efficient for lookups than the above system if it is usable in your organizational
# environment. If this setting has a value it will be used instead of AUTH_LDAP_USER_SEARCH
# above.

AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,cn=users,cn=accounts,dc=tni01,dc=com'

# Mapping of LDAP user schema to AWX API user atrributes (key is user attribute name, value is LDAP
# attribute name).  The default setting in this configuration file is valid for ActiveDirectory but
# users with other LDAP configurations may need to change the values (not the keys) of the dictionary/hash-table
# below.

AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}

# Users in AWX are mapped to organizations based on their membership in LDAP groups.  The following setting defines
# the LDAP search query to find groups. Note that this, unlike the user search above, does not support LDAPSearchUnion.

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    'cn=groups,cn=accounts,dc=tni01,dc=com',  # Base DN
    ldap.SCOPE_SUBTREE,  # SCOPE_BASE, SCOPE_ONELEVEL, SCOPE_SUBTREE
    '(objectClass=ipausergroup)',  # Query
)

# The group type import may need to be changed based on the type of the LDAP server.
# Values are listed at: http://pythonhosted.org/django-auth-ldap/groups.html#types-of-groups

AUTH_LDAP_GROUP_TYPE = NestedGroupOfNamesType()

# Group DN required to login. If specified, user must be a member of this
# group to login via LDAP.  If not set, everyone in LDAP that matches the
# user search defined above will be able to login via AWX.  Only one
# require group is supported.

AUTH_LDAP_REQUIRE_GROUP = 'cn=ansible-tower-users,cn=groups,cn=accounts,dc=tni01,dc=com'

# Group DN denied from login. If specified, user will not be allowed to login
# if a member of this group.  Only one deny group is supported.

# AUTH_LDAP_DENY_GROUP = ''

# User profile flags updated from group membership (key is user attribute name,
# value is group DN).  These are boolean fields that are matched based on
# whether the user is a member of the given group.  So far only is_superuser
# is settable via this method.  This flag is set both true and false at login
# time based on current LDAP settings.

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'is_superuser': 'cn=ansible-tower-admin,cn=groups,cn=accounts,dc=tni01,dc=com',
}

# Mapping between organization admins/users and LDAP groups. This controls what
# users are placed into what AWX organizations relative to their LDAP group
# memberships. Keys are organization names.  Organizations will be created if not present.
# Values are dictionaries defining the options for each organization's membership.  For each organization
# it is possible to specify what groups are automatically users of the organization and also what
# groups can administer the organization.
#
# - admins: None, True/False, string or list/tuple of strings.
#   If None, organization admins will not be updated based on LDAP values.
#   If True, all users in LDAP will automatically be added as admins of the organization.
#   If False, no LDAP users will be automatically added as admins of the organiation.
#   If a string or list of strings, specifies the group DN(s) that will be added of the organization if they match
#   any of the specified groups.
# - remove_admins: True/False. Defaults to False.
#   If True, a user who is not an member of the given groups will be removed from the organization's administrative list.
# - users: None, True/False, string or list/tuple of strings. Same rules apply
#   as for admins.
# - remove_users: True/False. Defaults to False. Same rules as apply for remove_admins

AUTH_LDAP_ORGANIZATION_MAP = {
    # 'Test Org': {
    #    'admins': 'CN=Domain Admins,CN=Users,DC=example,DC=com',
    #    'users': ['CN=Domain Users,CN=Users,DC=example,DC=com'],
    #    'remove_users' : False,
    #    'remove_admins' : False,
    # },
    # 'Test Org 2': {
    #    'admins': ['CN=Administrators,CN=Builtin,DC=example,DC=com'],
    #    'users': True,
    #    'remove_users' : False,
    #    'remove_admins' : False,
    # },
    'Tendril': {
        'admins': 'cn=ansible-tower-tendril-org-admins,cn=groups,cn=accounts,dc=tni01,dc=com',
        'users': ['cn=ansible-tower-users,cn=groups,cn=accounts,dc=tni01,dc=com'],
        'remove_users': False,
        'remove_admins': True,
    }
}

# Mapping between team members (users) and LDAP groups. Keys are team names
# (will be created if not present). Values are dictionaries of options for
# each team's membership, where each can contain the following parameters:
# - organization: string. The name of the organization to which the team
#   belongs.  The team will be created if the combination of organization and
#   team name does not exist.  The organization will first be created if it
#   does not exist.
# - users: None, True/False, string or list/tuple of strings.
#   If None, team members will not be updated.
#   If True/False, all LDAP users will be added/removed as team members.
#   If a string or list of strings, specifies the group DN(s). User will be
#   added as a team member if the user is a member of ANY of these groups.
# - remove: True/False. Defaults to False. If True, a user who is not a member
#   of the given groups will be removed from the team.

AUTH_LDAP_TEAM_MAP = {
    # 'My Team': {
    #    'organization': 'Test Org',
    #    'users': ['CN=Domain Users,CN=Users,DC=example,DC=com'],
    #    'remove': True,
    # },
    # 'Other Team': {
    #    'organization': 'Test Org 2',
    #    'users': 'CN=Other Users,CN=Users,DC=example,DC=com',
    #    'remove': False,
    # },
    'Dev': {
        'organization': 'Tendril',
        'users': ['cn=ansible-tower-users,cn=groups,cn=accounts,dc=tni01,dc=com'],
        'remove': True,
    }
}