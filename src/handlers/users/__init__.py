def setup():
    from .start import dp
    from .wallets import setup as setup_wallets

    setup_wallets()

    from .transactions import setup as setup_transactions
    
    setup_transactions()
