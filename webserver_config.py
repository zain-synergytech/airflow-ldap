"""
Production-Ready Airflow LDAP Configuration
Uses standard Flask-AppBuilder AUTH_ROLES_MAPPING with memberOf attributes

This configuration works with the production bootstrap.ldif file that includes
memberOf attributes for all users.
"""
import os
from airflow import configuration as conf
from flask_appbuilder.security.manager import AUTH_LDAP

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
try:
    # Use the new configuration key if available
    SQLALCHEMY_DATABASE_URI = conf.get('database', 'sql_alchemy_conn')
except:
    # Fallback to deprecated key
    SQLALCHEMY_DATABASE_URI = conf.get('core', 'SQL_ALCHEMY_CONN')

# Security settings
CSRF_ENABLED = True
WTF_CSRF_ENABLED = True

# =============================================================================
# LDAP AUTHENTICATION CONFIGURATION
# =============================================================================

# Authentication method
AUTH_TYPE = AUTH_LDAP

# LDAP server configuration
AUTH_LDAP_SERVER = "ldap://openldap:389"

# Base DN for LDAP searches
AUTH_LDAP_SEARCH = "dc=example,dc=org"

# User identifier field in LDAP
AUTH_LDAP_UID_FIELD = "uid"

# Service account for LDAP binding
AUTH_LDAP_BIND_USER = "cn=admin,dc=example,dc=org"
AUTH_LDAP_BIND_PASSWORD = "admin"

# TLS/SSL configuration (adjust for production)
AUTH_LDAP_USE_TLS = False
AUTH_LDAP_ALLOW_SELF_SIGNED = True

# =============================================================================
# USER REGISTRATION AND FIELD MAPPING
# =============================================================================

# Allow automatic user registration on first login
AUTH_USER_REGISTRATION = True

# Default role for new users (fallback if no group mapping found)
AUTH_USER_REGISTRATION_ROLE = "Viewer"

# Map LDAP user attributes to Airflow user fields
AUTH_LDAP_FIRSTNAME_FIELD = "givenName"  # or "cn" if givenName not available
AUTH_LDAP_LASTNAME_FIELD = "sn"          # surname
AUTH_LDAP_EMAIL_FIELD = "mail"           # email address

# =============================================================================
# GROUP-BASED ROLE MAPPING (STANDARD FLASK-APPBUILDER)
# =============================================================================

# LDAP attribute containing group memberships
# This works because our bootstrap.ldif includes memberOf attributes
AUTH_LDAP_GROUP_FIELD = "memberOf"

# Map LDAP groups to Airflow roles
# These group DNs must match exactly what's in the memberOf attributes
AUTH_ROLES_MAPPING = {
    "cn=airflow-admins,ou=groups,dc=example,dc=org": ["Admin"],
    "cn=airflow-users,ou=groups,dc=example,dc=org": ["User"], 
    "cn=airflow-viewers,ou=groups,dc=example,dc=org": ["Viewer"],
}

# Synchronize user roles on every login
AUTH_ROLES_SYNC_AT_LOGIN = True

# =============================================================================
# ADDITIONAL SECURITY CONFIGURATION
# =============================================================================

# Admin role name
AUTH_ROLE_ADMIN = "Admin"

# Optional: Custom user search filter
# AUTH_LDAP_SEARCH_FILTER = "(objectClass=inetOrgPerson)"

# Optional: Bind with user credentials first (more secure)
# AUTH_LDAP_BIND_FIRST = True

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

import logging

# Set up logging for authentication events
logging.getLogger("flask_appbuilder.security").setLevel(logging.INFO)

# Optional: More detailed LDAP debugging (disable in production)
# logging.getLogger("flask_appbuilder.security.ldap").setLevel(logging.DEBUG)

# =============================================================================
# CONFIGURATION SUMMARY
# =============================================================================

print("=== PRODUCTION LDAP CONFIGURATION LOADED ===")
print(f"LDAP Server: {AUTH_LDAP_SERVER}")
print(f"Search Base: {AUTH_LDAP_SEARCH}")
print(f"Group Field: {AUTH_LDAP_GROUP_FIELD}")
print(f"Role Mapping: {AUTH_ROLES_MAPPING}")
print(f"Default Role: {AUTH_USER_REGISTRATION_ROLE}")
print(f"Role Sync: {AUTH_ROLES_SYNC_AT_LOGIN}")
print("============================================")

# =============================================================================
# PRODUCTION DEPLOYMENT NOTES
# =============================================================================
"""
SECURITY CHECKLIST FOR PRODUCTION:

1. PASSWORDS:
   - Change default LDAP admin password
   - Use strong passwords for all LDAP users
   - Consider password policies

2. TLS/SSL:
   - Enable AUTH_LDAP_USE_TLS = True
   - Configure proper SSL certificates
   - Set AUTH_LDAP_ALLOW_SELF_SIGNED = False

3. SERVICE ACCOUNT:
   - Create dedicated service account for Airflow
   - Grant minimum required permissions
   - Use strong password for service account

4. NETWORK SECURITY:
   - Restrict LDAP server access to Airflow servers only
   - Use firewall rules to limit network access
   - Consider VPN for remote access

5. MONITORING:
   - Monitor authentication failures
   - Log role assignments and changes
   - Set up alerts for security events

6. BACKUP:
   - Regular LDAP backups
   - Test restore procedures
   - Document recovery processes

ROLE ASSIGNMENT:
- Admin: johndoe, anna.meier (full system access)
- User: (intermediate permissions - can create/edit DAGs)
- Viewer: peter.schmidt (read-only access)

To add new users:
1. Create user in appropriate OU
2. Add memberOf attribute pointing to desired group
3. User will get appropriate role on first login
"""
