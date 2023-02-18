import asyncio

import aiosqlite
import click
from flask import current_app, g


async def get_db():
    if 'db' not in g:
        g.db = await aiosqlite.connect(
            current_app.config['DATABASE']
        )
        g.db.row_factory = aiosqlite.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        asyncio.run(db.close())


async def init_db():
    db = await get_db()

    with current_app.open_resource('schema.sql') as f:
        await db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    asyncio.run(init_db())
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
