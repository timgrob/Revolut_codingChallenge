DATABASE_USER = 'timgrob'
DATABASE_PW = ''
DATABASE_NAME = 'revolut_db'
DATABASE_PORT = '5432'
DATABASE_URL = 'postgresql+psycopg2://{}:{}@localhost:{}/{}'.format(DATABASE_USER,DATABASE_PW,DATABASE_PORT,DATABASE_NAME)
