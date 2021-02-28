import click


@click.group()
@click.pass_context
def cli(ctx):
    """ A command line utility for organizing directories of binary content.
    """
    ctx.ensure_object(dict)


@cli.command()
@click.pass_obj
def init(obj):
    """ Create a new fit repository in the current directory.
    """
    if not os.path.exists(obj['fit_path']):
        os.mkdir(obj['fit_path'])
        os.mkdir(os.path.join(obj['fit_path'], 'objects'))
        click.echo(f'Initialized empty fit repository in: {obj["fit_path"]!r}')
    else:
        click.echo(f'fit repository already exists in: {obj["fit_path"]!r}')


@cli.command()
@click.option('--clean', '-c', default=False, is_flag=True,
              help='Remove untracked files.')
@click.option('--force', '-f', default=False, is_flag=True,
              help='Don\'t prompt for confirmation when removing untracked '
              'files.')
@click.pass_obj
def pack(obj, clean, force):
    """ Removes all tracked links and their directories.
    """
    if not in_repo(obj):
        return

    unpacked_files = models.session.query(models.File).filter_by(packed=False)

    # Pack files
    for file in unpacked_files:
        click.echo(f'{file.hash} PACK {format_filename(obj, file.file)!r}')
        os.remove(file.file)
        file.packed = True
    models.session.commit()

    remove_empty_directories(obj['fit_repo_path'], clean=clean, force=force)


@cli.command()
@click.pass_obj
def status(obj):
    """ Show the active directory status.
    """
    if not in_repo(obj):
        return

    file_query = models.session.query(models.File)
    packed_files = file_query.filter_by(packed=True)
    tag_query = models.session.query(models.Tag).group_by(models.Tag.tag)
    click.echo(f'{file_query.count()} tracked files - {packed_files.count()} packed')
    click.echo(f'{tag_query.count()} tags')


@cli.group()
@click.pass_context
def tag(ctx):
    """ Create, manage, and view tags.
    """
    if not in_repo(obj):
        return

    ctx.ensure_object(dict)


@tag.command()
@click.argument('tag')
@click.argument('filenames', type=click.Path(exists=True), nargs=-1,
                required=True)
@click.pass_obj
def add(obj, tag, filenames):
    """ Tag one or more files.
    """
    if not in_repo(obj):
        return

    for filename in filenames:
        file = models.session.query(models.File) \
                .filter_by(file=os.path.abspath(filename)) \
                .first()
        if file:
            hash = file.hash
            tag_query = models.session.query(models.Tag) \
                .filter_by(hash=hash, tag=tag)
            if not tag_query.count():
                models.Tag.add(hash=hash, tag=tag)
                click.echo(f'{hash} TAGGED {tag!r}')
            else:
                click.echo(f'{hash} is already tagged {tag!r}')
        else:
            click.echo(f'Cannot tag untracked file: {format_filename(obj, filename)!r}')


@tag.command()
@click.argument('tag')
@click.argument('filenames', type=click.Path(exists=True), nargs=-1,
                required=True)
@click.pass_obj
def remove(obj, tag, filenames):
    """ Remove tag from one or more files.
    """
    if not in_repo(obj):
        return

    for filename in filenames:
        file = models.session.query(models.File) \
                .filter_by(file=os.path.abspath(filename)) \
                .first()
        if file:
            hash = file.hash
            tag_query = models.session.query(models.Tag) \
                .filter_by(hash=hash, tag=tag)
            if tag_query.count():
                tag_query.delete()
                models.session.commit()
                click.echo(f'{hash} UNTAGGED {tag!r}')
            else:
                click.echo(f'{hash} is not tagged {tag!r}')
        else:
            click.echo(f'Cannot tag untracked file: {format_filename(obj, filename)!r}')


@tag.command()
@click.argument('tag')
@click.pass_obj
def find(obj, tag):
    """ Find all files with a certain tag.
    """
    if not in_repo(obj):
        return

    tag_obj = models.session.query(models.Tag).filter_by(tag=tag).first()
    if tag_obj:
        file_query = models.session.query(models.File) \
            .filter_by(hash=tag_obj.hash) \
            .order_by(models.File.file)
        for file in file_query:
            click.echo(format_filename(obj, file.file))
    else:
        click.echo(f'No such tag: {tag!r}')


@tag.command()
@click.option('--uses', '-u', default=False, is_flag=True,
              help='Sort by and display number of uses.')
@click.pass_obj
def show(obj, uses):
    """ Show all existing tags.
    """
    if not in_repo(obj):
        return

    tag_query = models.session.query(
        models.Tag,
        func.count(models.Tag.tag).label('count')
    ) \
        .group_by(models.Tag.tag) \
        .order_by(desc('count') if uses else models.Tag.tag)
    for tag, count in tag_query:
        if uses:
            click.echo(f'{tag.tag} ({count} uses)')
        else:
            click.echo(tag.tag)


@tag.command()
@click.argument('filenames', type=click.Path(exists=True), nargs=-1,
                required=True)
@click.pass_obj
def view(obj, filenames):
    """ View all the tags for one or more files.
    """
    if not in_repo(obj):
        return

    for filename in filenames:
        file = models.session.query(models.File) \
                .filter_by(file=os.path.abspath(filename)) \
                .first()
        if file:
            hash = file.hash
            tag_query = models.session.query(models.Tag) \
                .filter_by(hash=hash) \
                .order_by(models.Tag.tag)
            if tag_query.count():
                tags = [tag.tag.__repr__() for tag in tag_query]
                click.echo(f'{hash} {", ".join(tags)}')
        else:
            click.echo(f'Cannot tag untracked file: {format_filename(obj, filename)!r}')


@cli.command()
@click.option('--soft/--hard', '-s/-h', default=False,
              help='The type of links to create.')
@click.pass_obj
def unpack(obj, soft):
    """ Restores all tracked links and their directories.
    """
    if not in_repo(obj):
        return

    object_dir_path = os.path.join(obj['fit_path'], 'objects')
    packed_files = models.session.query(models.File).filter_by(packed=True)
    for file in packed_files:
        object_path = os.path.join(object_dir_path, file.hash)
        file_path = os.path.relpath(file.file, obj['fit_repo_path'])
        for dir_part in [os.path.sep.join(file_path.split(os.path.sep)[:i+1])
                         for i in range(len(file_path.split(os.path.sep)) - 1)]:
            dir_part = os.path.join(obj['fit_repo_path'], dir_part)
            if not os.path.exists(dir_part):
                os.mkdir(dir_part)

        # Create links
        click.echo(f'{file.hash} LINK ({"soft" if soft else "hard"}) {format_filename(obj, file.file)!r}')
        if soft:
            os.symlink(object_path, file.file)
        else:
            os.link(object_path, file.file)

        file.packed = False
    models.session.commit()


@cli.command()
@click.option('--soft/--hard', '-s/-h', default=False,
              help='The type of links to create.')
@click.option('--pack', '-p', default=False, is_flag=True,
              help='Automatically pack new files.')
@click.pass_obj
def update(obj, soft, pack):
    """ Tracks changes to the active directory and replaces literal files with
        their respective links.
    """
    if not in_repo(obj):
        return

    # Make list of tracked files that are expected to be found
    expected_file_query = models.session.query(models.File.file) \
            .filter_by(packed=False)
    expected_files = [row.file for row in expected_file_query]

    # Traverse active directory looking for changes
    for root, dirs, files in os.walk(obj['fit_repo_path'], topdown=True):
        # Filter excluded paths
        dirs[:] = [d for d in dirs if not exclude(d)]
        # Process files
        for file in files:
            file_path = os.path.join(root, file)
            if file_path in expected_files:
                expected_files.remove(file_path)
            if not exclude(file):
                process_file(obj, file_path, soft=soft)

    remove_empty_directories(obj['fit_repo_path'])

    # Remove unpacked file rows that were not found in active directory
    for file_path in expected_files:
        click.echo(f'{format_filename(obj, file_path)!r} REMOVE (outdated file reference)')
        file = models.session.query(models.File) \
                .filter_by(file=file_path).delete()
        models.session.commit()

    # Remove newly orphaned objects
    for hash in os.listdir(os.path.join(obj['fit_path'], 'objects')):
        file_query = models.session.query(models.File).filter_by(hash=hash)
        if not file_query.count():
            click.echo(f'{hash} REMOVE (orphaned object)')
            object = os.path.join(obj['fit_path'], 'objects', hash)
            os.remove(object)


if __name__ == '__main__':
    obj = dict()
    obj['fit_path'] = os.path.abspath(find_path_up('.fit', start='.') or './.fit')
    obj['db_path'] = os.path.join(obj['fit_path'], 'data')
    obj['fit_repo_path'] = os.path.abspath(os.path.join(obj['fit_path'], '..'))
    if os.path.exists(obj['fit_path']):
        obj['db'] = create_engine(f'sqlite:///{obj["db_path"]}')
    else:
        obj['db'] = create_engine(f'sqlite:///:memory:')
    models.bind(obj['db'])
    obj['in_repo'] = os.path.exists(obj['fit_path'])
    cli(obj=obj)
