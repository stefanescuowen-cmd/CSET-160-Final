# Please enter password for the
# following service:
# Service: Mysql@localhost:3306
# User: root

# Password:

# Save password in vault

# OK

# Cancel
class Config:
    SECRET_KEY = "Al1baba64"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Stevens2023!@localhost/exam_platform"
    SQLALCHEMY_TRACK_MODIFICATIONS = False