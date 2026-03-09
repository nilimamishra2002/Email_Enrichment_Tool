def extract_domain(email):
    """
    Extract domain from email.
    Example: hr@gravity.com-> gravity.com
    """
    try:
        return email.split('@')[1].lower()
    except:
        return None

def extract_name(email):
    """
    Extract a likely person name from the email prefix.
    """

    name = email.split("@")[0]

    # replace separators
    name = name.replace(".", " ").replace("_", " ").replace("-", " ")

    name = name.strip()

    # handle short prefixes like rsriram
    if len(name) > 1 and name[0].isalpha() and name[1].islower() == False:
        name = name[0] + " " + name[1:]

    return name.title()