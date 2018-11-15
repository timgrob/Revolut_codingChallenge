DATABASE_USER = 'db_user'
DATABASE_PW = 'db_pw'
DATABASE_NAME = 'db_name'
DATABASE_PORT = 'db_port'
DATABASE_URL = 'postgresql+psycopg2://{}:{}@localhost:{}/{}'.format(DATABASE_USER,DATABASE_PW,DATABASE_PORT,DATABASE_NAME)
