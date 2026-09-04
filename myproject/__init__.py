import pymysql

# 1. Install PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()

# 2. Patch version check & feature flag for older MariaDB/XAMPP
from django.db.backends.mysql import base, features

base.DatabaseWrapper.check_database_version_supported = lambda self: None
features.DatabaseFeatures.can_return_columns_from_insert = False