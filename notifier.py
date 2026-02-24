from twilio.rest import Client
import config, logging

logger = logging.getLogger(__name__)

def send(msg: str):
    """Send a WhatsApp message via Twilio."""
    try:
        prefix = '[PAPER] ' if config.PAPER_TRADING else '[LIVE] '
        client = Client(config.TWILIO_SID, config.TWILIO_TOKEN)
        client.messages.create(
            body=prefix + msg,
            from_=config.TWILIO_FROM,
            to=config.TWILIO_TO
        )
        logger.info(f'WhatsApp sent: {msg}')
    except Exception as e:
        logger.error(f'WhatsApp failed: {e}')
