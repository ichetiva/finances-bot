def setup():
    from .start import dp

    from .wallets import setup as setup_wallets

    setup_wallets()
