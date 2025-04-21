def register_commands(app):
    from .seed_db import seed_db
    from .check_db import db_cli
    
    app.cli.add_command(seed_db)
    app.cli.add_command(db_cli)