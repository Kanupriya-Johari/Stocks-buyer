import requests, pyotp, logging, os
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect
import config

logger = logging.getLogger(__name__)


def login() -> KiteConnect:
    session = requests.Session()
    kite = KiteConnect(api_key=config.KITE_API_KEY)

    # Step 1: POST credentials
    r1 = session.post('https://kite.zerodha.com/api/login', data={
        'user_id':  config.KITE_USER_ID,
        'password': config.KITE_PASSWORD
    })
    r1.raise_for_status()
    request_id = r1.json()['data']['request_id']

    # Step 2: TOTP 2FA
    totp_code = pyotp.TOTP(config.KITE_TOTP_SECRET).now()
    r2 = session.post('https://kite.zerodha.com/api/twofa', data={
        'request_id':   request_id,
        'twofa_value':  totp_code,
        'user_id':      config.KITE_USER_ID
    })
    r2.raise_for_status()

    # Step 3: Get request_token
    r3 = session.get(kite.login_url(), allow_redirects=True)
    parsed = urlparse(r3.url)
    params = parse_qs(parsed.query)

    if 'request_token' not in params:
        raise Exception(f'No request_token in redirect: {r3.url}')

    request_token = params['request_token'][0]

    # Step 4: Exchange for access_token
    data = kite.generate_session(request_token, api_secret=config.KITE_API_SECRET)
    kite.set_access_token(data['access_token'])

    # Step 5: Cache token
    with open(config.TOKEN_FILE, 'w') as f:
        f.write(data['access_token'])

    logger.info('Zerodha login successful')
    return kite
def get_kite() -> KiteConnect:
    if os.path.exists(config.TOKEN_FILE):
        kite = KiteConnect(api_key=config.KITE_API_KEY)
        token = open(config.TOKEN_FILE).read().strip()
        kite.set_access_token(token)
        try:
            kite.profile()
            return kite
        except Exception:
            pass

    return login()
