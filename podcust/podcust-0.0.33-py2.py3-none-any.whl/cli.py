"""Console script for podcust.

Useful documentation at:
https://click.palletsprojects.com/en/7.x/quickstart/#nesting-commands
https://click.palletsprojects.com/en/7.x/complex/
"""

import click
from podcust.demo.custodian import DemoCust
from podcust.transmission.custodian import TransmissionCust


@click.group()
def main(args=None):
    """Podcust commands provide a wrapper around lower level utilities
    from podman, the Operating System and the container you are managing."""
    click.echo("Welcome to Podman Custodian!")


@click.group()
@click.pass_context
def demo(ctx):
    """Podcust tools for demo container image."""
    # We can only use ctx.obj to create and share between commands.
    ctx.obj = DemoCust()
    click.echo("Initializing Podman Custodian Demo class.")


@click.command()
@click.pass_obj
def rmi(obj):
    """Remove a demo image."""
    click.echo("Removing Demo image.")
    obj.remove_stored_image()
    click.echo("Image removed!")


@click.command()
@click.pass_obj
def rmec(obj):
    """Remove an exited demo container."""
    click.echo("Removing Demo containers.")
    obj.removed_exited_containers()
    click.echo("Containers removed!")


@click.command()
@click.pass_obj
def build(obj):
    """Build a demo image."""
    click.echo("building Demo image.")
    obj.build_demo_image()
    click.echo("Image built!")


@click.command()
@click.pass_obj
def dstart(obj):
    """Start a demo container."""
    click.echo("Starting Demo container.")
    obj.run_container()
    click.echo("Demo container started!")


@click.command()
@click.pass_obj
def dstop(obj):
    """Stop a demo container."""
    click.echo("Stopping Demo container.")
    obj.stop_container()
    click.echo("Demo container stopped!")


@click.command()
@click.pass_obj
def activate(obj):
    """Activate a demo container's service."""
    click.echo("Activating Demo container.")
    obj.activate_container()
    click.echo("Demo container service activated!")


@click.command()
@click.pass_obj
def deactivate(obj):
    """Deactivate a demo container's service."""
    click.echo("Deactivating Demo container.")
    obj.deactivate_container()
    click.echo("Demo container service deactivated!")


@click.command()
@click.pass_obj
def health(obj):
    """Health check of a demo container's service."""
    click.echo("Checking Demo container.")
    obj.health_check()


main.add_command(demo)
demo.add_command(rmi)
demo.add_command(rmec)
demo.add_command(build)
demo.add_command(dstart)
demo.add_command(dstop)
demo.add_command(activate)
demo.add_command(deactivate)
demo.add_command(health)


@click.group()
@click.pass_context
def transmission(ctx):
    """Podcust tools for demo container image."""
    # We can only use ctx.obj to create and share between commands.
    ctx.obj = TransmissionCust()
    click.echo("Initializing Podman Custodian Transmission class.")


@click.command()
@click.pass_obj
def deploy(obj):
    """Deploy transmission container within a pod."""
    click.echo("Deploying transmission container within a pod")
    obj.deploy()
    click.echo("Transmission container deployed!")


@click.command()
@click.pass_obj
def stop(obj):
    """Stop transmission pod."""
    click.echo("Stopping transmission pod.")
    obj.stop()
    click.echo("Transmission pod stopped!")


@click.command()
@click.pass_obj
def start(obj):
    """Start transmission pod."""
    click.echo("Starting transmission pod.")
    obj.stop()
    click.echo("Transmission pod started!")


@click.command()
@click.pass_obj
def rm(obj):
    """Delete transmission pod."""
    click.echo("Delete transmission pod.")
    obj.stop()
    click.echo("Transmission pod deleted!")


@click.command()
@click.pass_obj
def update(obj):
    """Update transmission pod."""
    click.echo("Updating transmission pod.")
    obj.update_running_image()
    click.echo("Transmission pod updated!")


main.add_command(transmission)
transmission.add_command(deploy)
transmission.add_command(stop)
transmission.add_command(start)
transmission.add_command(rm)
transmission.add_command(update)
