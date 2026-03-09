FREE_PROVIDERS=[
    'gmail.com',
    'yahoo.com',
    'outlook.com',
    'hotmail.com',
    'icloud.com',
    'mail.com',
]

def detect_domain_type(domain):
    """
    Check wheather domain is free or corporate.
    """

    if domain in FREE_PROVIDERS:
        return 'Free Provider'
    else:
        return 'Corporate'