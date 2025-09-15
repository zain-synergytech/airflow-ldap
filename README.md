# Apache Airflow with LDAP Authentication

A simple Docker setup for Apache Airflow with OpenLDAP authentication and web-based user management.

## Prerequisites

- Docker and Docker Compose
- Ports 8080, 8081, 389 available

## Quick Setup

### 1. Clone and Setup

```bash
git clone https://github.com/zain-synergytech/airflow-ldap.git
cd airflow-ldap

# Create directories and set permissions
mkdir -p dags logs plugins config
chmod 755 dags logs plugins config

# Create environment file
echo "AIRFLOW_UID=$(id -u)" > .env
```

### 2. Start Services

```bash
docker compose up -d
```

## Access

| Service | URL | Credentials |
|---------|-----|-------------|
| **Airflow** | http://localhost:8080 | See test users below |
| **LDAP Admin** | http://localhost:8081 | Login DN: `cn=admin,dc=example,dc=org`<br>Password: `admin` |

## Test Users

| Username | Password | Role |
|----------|----------|------|
| `johndoe` | `password123` | Admin |
| `anna.meier` | `password456` | Admin |
| `peter.schmidt` | `password789` | Viewer |

## Adding New Users

### 1. Create User in LDAP Admin

1. Go to http://localhost:8081
2. Login with admin credentials
3. Navigate to `ou=IT` (for Admin users) or `ou=Marketing` (for Viewers)
4. Create new user with basic fields:
   - **cn**: Full Name
   - **sn**: Last Name
   - **uid**: username
   - **mail**: email@example.org
   - **userPassword**: password

### 2. Add Group Membership

Since `memberOf` may not be in dropdown, use this LDIF method:

Create file `add-user.ldif`:
```ldif
dn: uid=newuser,ou=IT,dc=example,dc=org
changetype: modify
add: memberOf
memberOf: cn=airflow-admins,ou=groups,dc=example,dc=org
```

Apply:
```bash
docker cp add-user.ldif openldap:/tmp/add-user.ldif
docker compose exec openldap ldapmodify -x -H ldap://localhost:389 -D "cn=admin,dc=example,dc=org" -w admin -f /tmp/add-user.ldif
```

### 3. Group Roles

- **Admin**: `cn=airflow-admins,ou=groups,dc=example,dc=org`
- **Viewer**: `cn=airflow-viewers,ou=groups,dc=example,dc=org`

## Troubleshooting

### Check if services are running:
```bash
docker compose ps
```

### Test LDAP connection:
```bash
docker compose exec openldap ldapsearch -x -H ldap://localhost:389 -D "cn=admin,dc=example,dc=org" -w admin -b "dc=example,dc=org" "(uid=johndoe)"
```

### Check user roles in Airflow:
```bash
docker compose exec airflow-webserver airflow users list
```

### View logs:
```bash
docker compose logs airflow-webserver
docker compose logs openldap
```

## File Structure

```
airflow-ldap/
├── docker-compose.yml
├── webserver_config.py
├── ldap/bootstrap.ldif
├── dags/
├── logs/
├── plugins/
└── config/
```

That's it! Your Airflow with LDAP authentication is ready to use.
