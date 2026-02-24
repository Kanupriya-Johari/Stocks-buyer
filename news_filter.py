from google import genai
from google.genai import types
import logging
import config

logger = logging.getLogger(__name__)

client = genai.Client(api_key=config.GEMINI_API_KEY)

MODEL = "gemini-2.0-flash-lite"

PROMPT_TEMPLATE = """
You are a risk filter for an algorithmic stock trading bot focused on Indian markets (NSE).

Analyze the stock: {symbol} (NSE India)

Search for and evaluate:
1. Any fraud, scam, or regulatory (SEBI/RBI/ED) action in the last 7 days
2. Sudden CEO/CFO resignation or major management change in the last 7 days
3. Earnings announcement scheduled in the next 3 days
4. Any trading halt, circuit breaker, or ban on this stock
5. Major negative news that could cause a sharp drop (>5%) in the next week

Respond with EXACTLY this format and nothing else:
VERDICT: SAFE|CAUTION|AVOID
REASON: One sentence explaining why (max 20 words)

Rules:
- AVOID if: fraud/scam, SEBI ban, earnings in <3 days, trading halt
- CAUTION if: mixed news, management uncertainty, sector headwinds
- SAFE if: no major negative news found
"""


def check_news(symbol: str) -> dict:
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=PROMPT_TEMPLATE.format(symbol=symbol),
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        text    = response.text.strip()
        verdict = 'SAFE'
        reason  = 'No issues found'

        for line in text.split('\n'):
            if line.startswith('VERDICT:'):
                v = line.replace('VERDICT:', '').strip().upper()
                if v in ('SAFE', 'CAUTION', 'AVOID'):
                    verdict = v
            elif line.startswith('REASON:'):
                reason = line.replace('REASON:', '').strip()

        qty_multiplier = {'SAFE': 1.0, 'CAUTION': 0.5, 'AVOID': 0.0}[verdict]
        logger.info(f'Gemini [{symbol}]: {verdict} — {reason}')
        return {'verdict': verdict, 'reason': reason, 'qty_multiplier': qty_multiplier}

    except Exception as e:
        logger.error(f'Gemini check failed for {symbol}: {e}')
        return {'verdict': 'CAUTION', 'reason': f'News check failed: {e}', 'qty_multiplier': 0.5}


def filter_qty(original_qty: int, symbol: str) -> tuple:
    result  = check_news(symbol)
    verdict = result['verdict']
    reason  = result['reason']

    if verdict == 'AVOID':
        logger.warning(f'AVOID {symbol}: {reason}')
        return 0, verdict, reason
    elif verdict == 'CAUTION':
        adjusted = max(1, int(original_qty * 0.5))
        logger.info(f'CAUTION {symbol}: qty {original_qty}→{adjusted}')
        return adjusted, verdict, reason
    else:
        logger.info(f'SAFE {symbol}: qty {original_qty} unchanged')
        return original_qty, verdict, reason
