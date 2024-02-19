import logging

import click

from . import gmail as g

'''
This is the main entry point

Usage:
    poetry run main

Options:
    -h, --help  Show this message and exit

Commands:
    list - list the messages in the mailbox
    read - read a specific message based on the ID
'''

# This is the main entry point for the application

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@click.group()
@click.pass_context
def main(ctx):
    gmail = g.Gmail()
    gmail.authenticate()
    ctx.obj = gmail


@main.command()
@click.pass_obj
def list(ctx):
    messages = ctx.get_messages("INBOX")


@main.command()
@click.argument("message_id", type=str, required=True)
@click.pass_obj
def read(ctx, message_id):
    message = ctx.read_message(message_id)
    logger.info(message["subject"])
    pass
