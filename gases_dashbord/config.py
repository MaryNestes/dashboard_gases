from dotenv import dotenv_values

config = dotenv_values(".env")

TOKEN = config.get('TOKEN_MAP')
STYLE = config.get('STYLE_MAP')
PATH = config.get('PATH_GASES')

