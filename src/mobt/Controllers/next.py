import click

from mobt import echo


@click.command()
def next():
    """
    Pass the mob to the next team member. You must call this command even if you didn't make any changes in the code.
    It's important to call this command every time, so the mob tool can manage who's turn is next.

    It will push all the changes to the remote in a WIP commit.
    """
    from mobt.di import di
    from mobt.MobApp.MobNext import MobNext
    next_driver = di.get(MobNext).next()

    echo(f'Done! Next driver is: {next_driver}', fg='bright_green')
