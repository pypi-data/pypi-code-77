#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import click
from dxi._lib.util import boolean_based_system_exit
from dxi.database.dxi_dboperations import DXIDBOperations
from dxi.database.dxi_dboperations import DXIDBOperationsConstants
from dxi.database.dxi_delete import DeleteConstants
from dxi.database.dxi_delete import DXIDelete
from dxi.database.dxi_refresh import DXIRefresh
from dxi.database.dxi_refresh import VDBRefreshConstants
from dxi.database.dxi_rewind import DXIRewind
from dxi.database.dxi_rewind import VDBRewindConstants
from dxi.database.dxi_provisionvdb import DXIProvisionVDB
from dxi.database.dxi_provisiondsource import DXIProvisionDsource
from dxi.database.dxi_provisionvdb import ProvisionVDBConstants
from dxi.database.dxi_provisiondsource import ProvisionDsourceConstants


@click.group()
def database():
    """
    database is a group command perform dsource or vdb operations
    """
    pass


# Refresh command
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to refresh",
    default=None,
)
@click.option(
    "--time_stamp",
    default="LATEST",
    help='''
        The Delphix semantic for the point in time on the source
         from which you want to refresh your VDB.
         Formats: latest point in time or snapshot: LATEST
        point in time: "YYYY-MM-DD HH24:MI:SS"
        snapshot name: "@YYYY-MM-DDTHH24:MI:SS.ZZZ"
        snapshot time from GUI: "YYYY-MM-DD HH24:MI"''',
)
@click.option(
    "--time_stamp_type",
    help="The type of timestamp you are specifying",
    default="SNAPSHOT",
    type=click.Choice(["TIME", "SNAPSHOT"]),
)
@click.option(
    "--time_flow", help="Name of the timeflow to refresh a VDB", default=None
)
@click.option("--engine", default=VDBRefreshConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=VDBRefreshConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=VDBRefreshConstants.POLL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=VDBRefreshConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=VDBRefreshConstants.LOG_FILE_PATH,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=VDBRefreshConstants.PARALLEL,
)
def refresh(
    name,
    time_stamp_type,
    time_stamp,
    engine,
    single_thread,
    time_flow,
    poll,
    config,
    log_file_path,
    parallel,
):
    """
Refresh a Delphix VDB\n

dxi database refresh --name testdb --time_stamp 2021-02-04T04:43:58.000Z
    """

    obj = DXIRefresh(
        name=name,
        engine=engine,
        time_stamp_type=time_stamp_type,
        time_stamp=time_stamp,
        single_thread=single_thread,
        time_flow=time_flow,
        poll=poll,
        config=config,
        log_file_path=log_file_path,
        parallel=parallel,
    )

    boolean_based_system_exit(obj.refresh())


# Rewind Command
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to rewind",
    default=None,
)
@click.option(
    "--time_stamp",
    default="LATEST",
    help='''
        The Delphix semantic for the point in time on the source
        from which you want to refresh your VDB.
         Formats: latest point in time or snapshot: LATEST
        point in time: "YYYY-MM-DD HH24:MI:SS"
        snapshot name: "@YYYY-MM-DDTHH24:MI:SS.ZZZ"
        snapshot time from GUI: "YYYY-MM-DD HH24:MI"''',
)
@click.option(
    "--time_stamp_type",
    help="The type of timestamp you are specifying",
    default="SNAPSHOT",
    type=click.Choice(["TIME", "SNAPSHOT"]),
)
@click.option(
    "--database_type",
    help="Type of database: oracle, mssql, ase, vfiles",
    default=None,
)
@click.option("--engine", default=VDBRewindConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=VDBRewindConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=VDBRewindConstants.POLL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=VDBRewindConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=VDBRewindConstants.LOG_FILE_PATH,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=VDBRefreshConstants.PARALLEL,
)
def rewind(
    name,
    time_stamp_type,
    time_stamp,
    engine,
    single_thread,
    database_type,
    poll,
    config,
    log_file_path,
    parallel,
):
    """
Rewinds a VDB

dxi database rewind --name testdb --time_stamp 2021-02-04T04:43:58.000Z

    """

    obj = DXIRewind(
        name=name,
        engine=engine,
        time_stamp_type=time_stamp_type,
        time_stamp=time_stamp,
        single_thread=single_thread,
        database_type=database_type,
        poll=poll,
        config=config,
        log_file_path=log_file_path,
        parallel=parallel,
    )

    boolean_based_system_exit(obj.rewind())


# Delete command
@database.command()
@click.option(
    "--name",
    default=DeleteConstants.NAME,
    help="Name of dataset(s) in Delphix to execute against",
)
@click.option(
    "--type",
    default=DeleteConstants.TYPE,
    help="Type of the dataset to delete. vdb | dsource",
)
@click.option(
    "--force",
    is_flag=True,
    default=DeleteConstants.FORCE,
    help="Force delete the dataset",
)
@click.option("--engine", default=DeleteConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DeleteConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DeleteConstants.PARALLEL,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DeleteConstants.POLL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DeleteConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DeleteConstants.LOG_FILE_PATH,
)
def delete(
    name,
    type,
    engine,
    single_thread,
    parallel,
    poll,
    config,
    log_file_path,
    force,
):
    """
    Delete a Delphix dSource or VDB
    """
    delete_obj = DXIDelete(
        engine=engine,
        name=name,
        type=type,
        parallel=parallel,
        poll=poll,
        config=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
        force=force,
    )
    boolean_based_system_exit(delete_obj.delete_db())


#############################################
# DB Operations

# db-list
@database.command()
@click.option(
    "--engine",
    default=DXIDBOperationsConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIDBOperationsConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIDBOperationsConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIDBOperationsConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIDBOperationsConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIDBOperationsConstants.LOG_FILE_PATH,
)
def list(engine, single_thread, parallel, poll, config, log_file_path):
    """
    List all datasets on an engine
    """
    ops_obj = DXIDBOperations(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(ops_obj.list())


# db-start
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to start",
    default=None,
)
@click.option("--group", help="Group where the dataset resides", default=None)
@click.option(
    "--engine",
    default=DXIDBOperationsConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIDBOperationsConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIDBOperationsConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIDBOperationsConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIDBOperationsConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIDBOperationsConstants.LOG_FILE_PATH,
)
def start(
    name, group, engine, single_thread, parallel, poll, config, log_file_path
):
    """
    Starts a virtual dataset by name and group
    """
    ops_obj = DXIDBOperations(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(ops_obj.start(name=name, group=group))


# db-stop
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to start",
    default=None,
)
@click.option("--group", help="Group where the dataset resides", default=None)
@click.option(
    "--engine",
    default=DXIDBOperationsConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIDBOperationsConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIDBOperationsConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIDBOperationsConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIDBOperationsConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIDBOperationsConstants.LOG_FILE_PATH,
)
def stop(
    name, group, engine, single_thread, parallel, poll, config, log_file_path
):
    """
    Stop a virtual dataset by name and group (optional)
    """
    ops_obj = DXIDBOperations(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(ops_obj.stop(name=name, group=group))


# db-enable
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to start",
    default=None,
)
@click.option("--group", help="Group where the dataset resides", default=None)
@click.option(
    "--engine",
    default=DXIDBOperationsConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIDBOperationsConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIDBOperationsConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIDBOperationsConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIDBOperationsConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIDBOperationsConstants.LOG_FILE_PATH,
)
def enable(
    name, group, engine, single_thread, parallel, poll, config, log_file_path
):
    """
    Enable a virtual dataset by name and group(optional)
    """
    ops_obj = DXIDBOperations(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(ops_obj.enable(name=name, group=group))


# db-disable
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to start",
    default=None,
)
@click.option("--group", help="Group where the dataset resides", default=None)
@click.option(
    "--force",
    is_flag=True,
    help="Force disable a virtual dataset",
    default=None,
)
@click.option(
    "--engine",
    default=DXIDBOperationsConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIDBOperationsConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIDBOperationsConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIDBOperationsConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIDBOperationsConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIDBOperationsConstants.LOG_FILE_PATH,
)
def disable(
    name,
    group,
    force,
    engine,
    single_thread,
    parallel,
    poll,
    config,
    log_file_path,
):
    """
    Disable a virtual dataset by name and group(optional)
    """
    ops_obj = DXIDBOperations(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(
        ops_obj.disable(name=name, group=group, force=force)
    )


#############
# Provision VDB
@database.command()
@click.option(
    "--target_grp",
    required=True,
    help="The group into which Delphix will place the VDB",
)
@click.option(
    "--source_db",
    required=True,
    help="The source database",
)
@click.option(
    "--db",
    required=True,
    help="The name you want to give the database",
)
@click.option(
    "--env_name",
    required=True,
    help="The name of the Target environment in Delphix",
)
@click.option(
    "--single_thread",
    help="Run as a single thread. False if running multiple threads.",
    default=False,
    type=click.BOOL,
)
@click.option(
    "--db_type",
    required=True,
    help="The type of VDB. oracle, oramt, mssql, ase or vfiles"
)
@click.option(
    "--prerefresh",
    help='Pre-Hook commands before a refresh',
    default=False,
)
@click.option(
    "--postrefresh",
    help='Post-Hook commands after a refresh',
    default=False,
)
@click.option(
    "--prerollback",
    help='Pre-Hook commands before a rollback',
    default=False,
)
@click.option(
    "--postrollback",
    help='Post-Hook commands after a rollback',
    default=False,
)
@click.option(
    "--configure_clone",
    help='Configure Clone commands',
    default=False,
)
@click.option(
    "--envinst",
    help="The identifier of the instance in Delphix.",
    default=None
)
@click.option(
    "--timestamp_type",
    help="The type of timestamp you are specifying. TIME or SNAPSHOT",
    default="SNAPSHOT"
)
@click.option(
    "--timestamp",
    help="The Delphix semantic for the point in time from which you want to provision your VDB.",
    default="LATEST"
)
@click.option(
    "--mntpoint",
    help="The identifier of the instance in Delphix.",
    default="/mnt/provision"
)
@click.option(
    "--parallel", help="Limit number of jobs to maxjob.",
    type=click.INT,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=10,
    type=click.INT,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=ProvisionVDBConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=ProvisionVDBConstants.LOG_FILE_PATH,
)
@click.option(
    "--version", help="Show version.",
    type=click.BOOL,
    is_flag=True,
    default=True
)
@click.option("--engine", default=ProvisionVDBConstants.ENGINE_ID)
def provision_oracle(
    engine,
    source_db,
    db,
    db_type,
    target_grp,
    env_name,
    mntpoint,
    timestamp,
    timestamp_type,
    prerefresh,
    postrefresh,
    prerollback,
    postrollback,
    configure_clone,
    envinst,
    single_thread,
    parallel,
    poll,
    config,
    log_file_path,
    version
):
    """
    Provision an Oracle Delphix VDB
    """
    obj = DXIProvisionVDB(
        engine=engine,
        source_db=source_db,
        db=db,
        db_type=db_type,
        target_grp=target_grp,
        env_name=env_name,
        mntpoint=mntpoint,
        timestamp=timestamp,
        timestamp_type=timestamp_type,
        prerefresh=prerefresh,
        postrefresh=postrefresh,
        prerollback=prerollback,
        postrollback=postrollback,
        configure_clone=configure_clone,
        envinst=envinst,
        single_thread=single_thread,
        parallel=parallel,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
        version=version
    )
    obj.execute()


# Provision AppData VDB
@database.command()
@click.option(
    "--target_grp",
    required=True,
    help="The group into which Delphix will place the VDB",
)
@click.option(
    "--source_db",
    required=True,
    help="The source database",
)
@click.option(
    "--db",
    required=True,
    help="The name you want to give the database",
)
@click.option(
    "--env_name",
    required=True,
    help="The name of the Target environment in Delphix",
)
@click.option(
    "--single_thread",
    help="Run as a single thread. False if running multiple threads.",
    default=False,
    type=click.BOOL,
)
@click.option(
    "--db_type",
    required=True,
    help="The type of VDB. oracle, oramt, mssql, ase or vfiles"
)
@click.option(
    "--prerefresh",
    help='Pre-Hook commands before a refresh',
    default=False,
)
@click.option(
    "--postrefresh",
    help='Post-Hook commands after a refresh',
    default=False,
)
@click.option(
    "--prerollback",
    help='Pre-Hook commands before a rollback',
    default=False,
)
@click.option(
    "--postrollback",
    help='Post-Hook commands after a rollback',
    default=False,
)
@click.option(
    "--configure_clone",
    help='Configure Clone commands',
    default=False,
)
@click.option(
    "--timestamp_type",
    help="The type of timestamp you are specifying. TIME or SNAPSHOT",
    default="SNAPSHOT"
)
@click.option(
    "--timestamp",
    help="The Delphix semantic for the point in time from which you want to provision your VDB.",
    default="LATEST"
)
@click.option(
    "--mntpoint",
    help="The identifier of the instance in Delphix.",
    default="/mnt/provision"
)
@click.option(
    "--parallel", help="Limit number of jobs to maxjob.",
    type=click.INT,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=10,
    type=click.INT,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=ProvisionVDBConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=ProvisionVDBConstants.LOG_FILE_PATH,
)
@click.option(
    "--version", help="Show version.",
    type=click.BOOL,
    is_flag=True,
    default=True
)
@click.option("--engine", default=ProvisionVDBConstants.ENGINE_ID)
def provision_appdata(
    engine,
    source_db,
    db,
    db_type,
    target_grp,
    env_name,
    mntpoint,
    timestamp,
    timestamp_type,
    prerefresh,
    postrefresh,
    prerollback,
    postrollback,
    configure_clone,
    single_thread,
    parallel,
    poll,
    config,
    log_file_path,
    version
):
    """
    Provision an Appdata (vFiles) Delphix VDB
    """
    obj = DXIProvisionVDB(
        engine=engine,
        source_db=source_db,
        db=db,
        db_type=db_type,
        target_grp=target_grp,
        env_name=env_name,
        mntpoint=mntpoint,
        timestamp=timestamp,
        timestamp_type=timestamp_type,
        prerefresh=prerefresh,
        postrefresh=postrefresh,
        prerollback=prerollback,
        postrollback=postrollback,
        configure_clone=configure_clone,
        single_thread=single_thread,
        parallel=parallel,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
        version=version
    )
    obj.execute()


# Provision a Dephix MSSQL VDB
@database.command()
@click.option(
    "--target_grp",
    required=True,
    help="The group into which Delphix will place the VDB",
)
@click.option(
    "--source_db",
    required=True,
    help="The source database",
)
@click.option(
    "--db",
    required=True,
    help="The name you want to give the database",
)
@click.option(
    "--env_name",
    required=True,
    help="The name of the Target environment in Delphix",
)
@click.option(
    "--single_thread",
    help="Run as a single thread. False if running multiple threads.",
    default=False,
    type=click.BOOL,
)
@click.option(
    "--db_type",
    required=True,
    help="The type of VDB. oracle, oramt, mssql, ase or vfiles"
)
@click.option(
    "--prerefresh",
    help='Pre-Hook commands before a refresh',
    default=False,
)
@click.option(
    "--postrefresh",
    help='Post-Hook commands after a refresh',
    default=False,
)
@click.option(
    "--prerollback",
    help='Pre-Hook commands before a rollback',
    default=False,
)
@click.option(
    "--postrollback",
    help='Post-Hook commands after a rollback',
    default=False,
)
@click.option(
    "--configure_clone",
    help='Configure Clone commands',
    default=False,
)
@click.option(
    "--envinst",
    help="The identifier of the instance in Delphix.",
    default=None
)
@click.option(
    "--timestamp_type",
    help="The type of timestamp you are specifying. TIME or SNAPSHOT",
    default="SNAPSHOT"
)
@click.option(
    "--timestamp",
    help="The Delphix semantic for the point in time from which you want to provision your VDB.",
    default="LATEST"
)
@click.option(
    "--parallel", help="Limit number of jobs to maxjob.",
    type=click.INT,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=10,
    type=click.INT,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=ProvisionVDBConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=ProvisionVDBConstants.LOG_FILE_PATH,
)
@click.option(
    "--version", help="Show version.",
    type=click.BOOL,
    is_flag=True,
    default=True
)
@click.option("--engine", default=ProvisionVDBConstants.ENGINE_ID)
def provision_mssql(
    engine,
    source_db,
    db,
    db_type,
    target_grp,
    env_name,
    timestamp,
    timestamp_type,
    prerefresh,
    postrefresh,
    prerollback,
    postrollback,
    configure_clone,
    envinst,
    single_thread,
    parallel,
    poll,
    config,
    log_file_path,
    version
):
    """
    Provision a Delphix MSSQL VDB
    """
    obj = DXIProvisionVDB(
        engine=engine,
        source_db=source_db,
        db=db,
        db_type=db_type,
        target_grp=target_grp,
        env_name=env_name,
        timestamp=timestamp,
        timestamp_type=timestamp_type,
        prerefresh=prerefresh,
        postrefresh=postrefresh,
        prerollback=prerollback,
        postrollback=postrollback,
        configure_clone=configure_clone,
        envinst=envinst,
        single_thread=single_thread,
        parallel=parallel,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
        version=version
    )
    obj.execute()


# Provision a Dephix Sybase ASE VDB
@database.command()
@click.option(
    "--target_grp",
    required=True,
    help="The group into which Delphix will place the VDB",
)
@click.option(
    "--source_db",
    required=True,
    help="The source database",
)
@click.option(
    "--db",
    required=True,
    help="The name you want to give the database",
)
@click.option(
    "--single_thread",
    help="Run as a single thread. False if running multiple threads.",
    default=False,
    type=click.BOOL,
)
@click.option(
    "--db_type",
    required=True,
    help="The type of VDB. oracle, oramt, mssql, ase or vfiles"
)
@click.option(
    "--prerefresh",
    help='Pre-Hook commands before a refresh',
    default=False,
)
@click.option(
    "--postrefresh",
    help='Post-Hook commands after a refresh',
    default=False,
)
@click.option(
    "--prerollback",
    help='Pre-Hook commands before a rollback',
    default=False,
)
@click.option(
    "--postrollback",
    help='Post-Hook commands after a rollback',
    default=False,
)
@click.option(
    "--configure_clone",
    help='Configure Clone commands',
    default=False,
)
@click.option(
    "--envinst",
    help="The identifier of the instance in Delphix.",
    default=None
)
@click.option(
    "--timestamp_type",
    help="The type of timestamp you are specifying. TIME or SNAPSHOT",
    default="SNAPSHOT"
)
@click.option(
    "--timestamp",
    help="The Delphix semantic for the point in time from which you want to provision your VDB.",
    default="LATEST"
)
@click.option(
    "--parallel", help="Limit number of jobs to maxjob.",
    type=click.INT,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=10,
    type=click.INT,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=ProvisionVDBConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=ProvisionVDBConstants.LOG_FILE_PATH,
)
@click.option(
    "--version", help="Show version.",
    type=click.BOOL,
    is_flag=True,
    default=True
)
@click.option("--engine", default=ProvisionVDBConstants.ENGINE_ID)
def provision_ase(
    engine,
    source_db,
    db,
    db_type,
    target_grp,
    timestamp,
    timestamp_type,
    prerefresh,
    postrefresh,
    prerollback,
    postrollback,
    configure_clone,
    envinst,
    single_thread,
    parallel,
    poll,
    config,
    log_file_path,
    version
):
    """
    Provision a Delphix Sybase ASE VDB
    """
    obj = DXIProvisionVDB(
        engine=engine,
        source_db=source_db,
        db=db,
        db_type=db_type,
        target_grp=target_grp,
        timestamp=timestamp,
        timestamp_type=timestamp_type,
        prerefresh=prerefresh,
        postrefresh=postrefresh,
        prerollback=prerollback,
        postrollback=postrollback,
        configure_clone=configure_clone,
        envinst=envinst,
        single_thread=single_thread,
        parallel=parallel,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
        version=version
    )
    obj.execute()


# Provision dSource
#
@database.command()
@click.option(
    "--dsource_name",
    required=True,
    help="Name of the dSource to create",
)
@click.option(
    "--single_thread",
    help="Run as a single thread. False if running multiple threads.",
    default=False,
    type=click.BOOL,
)
@click.option(
    "--db_type",
    help="The type of VDB. oracle, oramt, mssql, ase or vfiles"
)
@click.option(
    "--db_passwd",
    help='Password for db_user',
    required=True,
    default=False,
)
@click.option(
    "--db_user",
    help='Username of the dSource DB',
    required=True,
    default=False,
)
@click.option(
    "--dx_group",
    help='Group name for this dSource',
    required=True,
    default=False,
)
@click.option(
    "--env_name",
    help='Name of the Delphix environment',
    required=True,
    default=False,
)
@click.option(
    "--ip_addr",
    help='IP Address of the dSource',
    required=True,
    default=False,
)
@click.option(
    "--db_type",
    help="dSource type. mssql, sybase, oracle or oramt",
    required=True,
    default=None
)
@click.option(
    "--logsync",
    help="Enable or disable logsync",
    default=True
)
@click.option(
    "--db_install_path",
    help="Location of the installation path of the DB",
    required=True,
    default=None
)
@click.option(
    "--source_user",
    help="Environment username",
    default='delphix'
)
@click.option(
    "--sync_mode",
    help="sync mode",
    default='UNDEFINED'
)
@click.option(
    "--rman_channels",
    help="Configures the number of Oracle RMAN Channels",
    default=2
)
@click.option(
    "--files_per_set",
    help="Configures how many files per set for Oracle RMAN",
    default=5
)
@click.option(
    "--num_connections",
    help="Number of connections for Oracle RMAN",
    default=5
)
@click.option(
    "--port_num",
    help="Port number for the Oracle Listener",
    default=5
)
@click.option(
    "--parallel", help="Limit number of jobs to maxjob.",
    type=click.INT,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=10,
    type=click.INT,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=ProvisionDsourceConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=ProvisionDsourceConstants.LOG_FILE_PATH,
)
@click.option(
    "--version", help="Show version.",
    type=click.BOOL,
    is_flag=True,
    default=True
)
@click.option("--engine", default=ProvisionDsourceConstants.ENGINE_ID)
def link_oracle(
    engine,
    ip_addr,
    env_name,
    dx_group,
    dsource_name,
    db_user,
    db_passwd,
    db_install_path,
    db_type,
    num_connections,
    log_file_path,
    logsync,
    single_thread,
    files_per_set,
    rman_channels,
    port_num,
    sync_mode,
    source_user,
    parallel,
    poll,
    config,
    version

):
    """
    Provision a Delphix dSource
    """
    obj = DXIProvisionDsource(
        engine=engine,
        ip_addr=ip_addr,
        env_name=env_name,
        dx_group=dx_group,
        dsource_name=dsource_name,
        db_user=db_user,
        db_passwd=db_passwd,
        db_install_path=db_install_path,
        db_type=db_type,
        num_connections=num_connections,
        logsync=logsync,
        single_thread=single_thread,
        files_per_set=files_per_set,
        rman_channels=rman_channels,
        port_num=port_num,
        sync_mode=sync_mode,
        source_user=source_user,
        log_file_path=log_file_path,
        parallel=parallel,
        poll=poll,
        config=config,
        version=version
    )
    obj.execute()


# MSSQL dSource
@database.command()
@click.option(
    "--dsource_name",
    help="Name of the dSource to create",
)
@click.option(
    "--single_thread",
    help="Run as a single thread. False if running multiple threads.",
    default=False,
    type=click.BOOL,
)
@click.option(
    "--db_type",
    help="The type of VDB. oracle, oramt, mssql, ase or vfiles"
)
@click.option(
    "--db_passwd",
    help='Password for db_user',
    default=False,
)
@click.option(
    "--db_user",
    help='Username of the dSource DB',
    default=False,
)
@click.option(
    "--dx_group",
    help='Delphix group name of where the dSource will be linked',
    default=False,
)
@click.option(
    "--env_name",
    help='Name of the Delphix environment',
    default=False,
)
@click.option(
    "--envinst",
    help='The identifier of the instance in Delphix. ex. LINUXTARGET',
    default=False,
)
@click.option(
    "--db_type",
    help="dSource type. mssql, sybase, oracle or oramt",
    default=None
)
@click.option(
    "--logsync",
    help="Enable or disable logsync",
    default=True
)
@click.option(
    "--backup_path",
    help="Path to the ASE/MSSQL backups",
    default=None
)
@click.option(
    "--sync_mode",
    help="MSSQL validated sync mode TRANSACTION_LOG|FULL_OR_DIFFERENTIAL|FULL|NONE",
    default='FULL'
)
@click.option(
    "--source_user",
    help="Environment username",
    default='delphix'
)
@click.option(
    "--stage_user",
    help="Stage username",
    default='delphix'
)
@click.option(
    "--stage_repo",
    help="Stage repository",
    default='delphix'
)
@click.option(
    "--stage_instance",
    help="Name of the PPT instance",
    default=None
)
@click.option(
    "--stage_env",
    help="Name of the PPT server",
    default=None
)
@click.option(
    "--backup_loc_passwd",
    help="Password of the shared backup path",
    default=None
)
@click.option(
    "--backup_loc_user",
    help="User of the shared backup path",
    default=None
)
@click.option(
    "--load_from_backup",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default=True
)
@click.option(
    "--validated_sync_mode",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default="TRANSACTION_LOG"
)
@click.option(
    "--delphix_managed",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default=True
)
@click.option(
    "--initial_load_type",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default=None
)
@click.option(
    "--logsync_mode",
    help="logsync mode",
    default=None
)
@click.option(
    "--parallel", help="Limit number of jobs to maxjob.",
    type=click.INT,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=10,
    type=click.INT,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=ProvisionDsourceConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=ProvisionDsourceConstants.LOG_FILE_PATH,
)
@click.option(
    "--version", help="Show version.",
    type=click.BOOL,
    is_flag=True,
    default=True
)
@click.option(
    "--initial_load_type",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default=None
)
@click.option(
    "--version", help="Show version.",
    type=click.BOOL,
    is_flag=True,
    default=True
)
@click.option("--engine", default=ProvisionDsourceConstants.ENGINE_ID)
def link_mssql(
    engine,
    env_name,
    dx_group,
    dsource_name,
    db_user,
    db_passwd,
    db_type,
    logsync,
    single_thread,
    backup_path,
    sync_mode,
    source_user,
    stage_user,
    stage_repo,
    stage_instance,
    logsync_mode,
    stage_env,
    backup_loc_passwd,
    backup_loc_user,
    delphix_managed,
    load_from_backup,
    initial_load_type,
    envinst,
    parallel,
    poll,
    config,
    validated_sync_mode,
    version

):
    """
    Provision a Delphix MSSQL dSource
    """
    obj = DXIProvisionDsource(
        engine=engine,
        env_name=env_name,
        dx_group=dx_group,
        dsource_name=dsource_name,
        db_user=db_user,
        db_passwd=db_passwd,
        db_type=db_type,
        logsync=logsync,
        single_thread=single_thread,
        backup_path=backup_path,
        sync_mode=sync_mode,
        source_user=source_user,
        stage_user=stage_user,
        stage_repo=stage_repo,
        stage_instance=stage_instance,
        stage_env=stage_env,
        logsync_mode=logsync_mode,
        backup_loc_passwd=backup_loc_passwd,
        backup_loc_user=backup_loc_user,
        load_from_backup=load_from_backup,
        validated_sync_mode=validated_sync_mode,
        delphix_managed=delphix_managed,
        initial_load_type=initial_load_type,
        envinst=envinst,
        parallel=parallel,
        poll=poll,
        config=config,
        version=version
    )
    obj.execute()


if __name__ == "__main__":
    provision_mssql()
