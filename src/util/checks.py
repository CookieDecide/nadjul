"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

def is_dev(ctx):
    """Check if the user is an admin.

    Args:
        ctx: Context of command invocation.

    Returns:
        True if user is an admin, False otherwise.
    """
    devs = [132557567585943553, 132545399184424960]
    return ctx.author.id in devs