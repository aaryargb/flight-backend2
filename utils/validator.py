
def validate_airport(code):
    if not code:
        return False
    if len(code) != 3:
        return False
    return True