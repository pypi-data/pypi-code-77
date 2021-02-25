# Copyright 2021 Sushil Khanchi <sushilkhanchi97@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
import io

from ..errors import (
    not_implemented,
    unknown_error,
)
from ..oid import (
    blob_oid,
)
from ..git import (
    NULL_BLOB_OID,
)
from mercurial import (
    patch,
    pycompat,
    diffutil,
)
from ..stub.diff_pb2 import (
    CommitDiffRequest,
    CommitDiffResponse,
    CommitDeltaRequest,
    CommitDeltaResponse,
    RawDiffRequest,
    RawDiffResponse,
    RawPatchRequest,
    RawPatchResponse,
    DiffStatsRequest,
    DiffStatsResponse,
)
from ..stub.diff_pb2_grpc import DiffServiceServicer

from ..servicer import HGitalyServicer
from ..revision import gitlab_revision_changeset
from ..stream import (
    concat_resplit,
    WRITE_BUFFER_SIZE,
)


logger = logging.getLogger(__name__)
# Copied from mercurial/patch.py
gitmode = {b'l': b'120000', b'x': b'100755', b'': b'100644'}


class DiffServicer(DiffServiceServicer, HGitalyServicer):
    """DiffService implementation.

    The ordering of methods in this source file is the same as in the proto
    file.
    """
    def CommitDiff(self, request: CommitDiffRequest,
                   context) -> CommitDiffResponse:
        return not_implemented(context, CommitDiffResponse,
                               issue=38)  # pragma no cover

    def CommitDelta(self, request: CommitDeltaRequest,
                    context) -> CommitDeltaResponse:
        return not_implemented(context, CommitDeltaResponse,
                               issue=39)  # pragma no cover

    def RawDiff(self, request: RawDiffRequest,
                context) -> RawDiffResponse:
        parsed_request = parse_diff_request(self, request, context)
        _parsed, repo, ctx_from, ctx_to = parsed_request
        if not _parsed:
            return unknown_error(context, RawDiffResponse, "exit status 128")
        opts = {b'git': True}
        overrides = {
            (b'experimental', b'extendedheader.similarity'): True,
        }
        with repo.ui.configoverride(overrides):
            diffopts = diffutil.diffallopts(repo.ui, opts)
            diffchunks = ctx_to.diff(ctx_from, opts=diffopts)

        # generator func to yield hunks
        def in_chunks():
            for chunk in patch.parsepatch(diffchunks):
                header = _insert_blob_index(chunk, ctx_from, ctx_to)
                yield header
                for hunk in chunk.hunks:
                    with io.BytesIO() as extracted:
                        hunk.write(extracted)
                        yield extracted.getvalue()
        for data in concat_resplit(in_chunks(), WRITE_BUFFER_SIZE):
            yield RawDiffResponse(data=data)

    def RawPatch(self, request: RawPatchRequest,
                 context) -> RawPatchResponse:
        return not_implemented(context, RawPatchResponse,
                               issue=41)  # pragma no cover

    def DiffStats(self, request: DiffStatsRequest,
                  context) -> DiffStatsResponse:
        return not_implemented(context, DiffStatsResponse,
                               issue=42)  # pragma no cover


def parse_diff_request(servicer, request, context):
    repo = servicer.load_repo(request.repository, context)
    left_cid = pycompat.sysbytes(request.left_commit_id)
    right_cid = pycompat.sysbytes(request.right_commit_id)
    ctx_from = gitlab_revision_changeset(repo, left_cid)
    ctx_to = gitlab_revision_changeset(repo, right_cid)
    if ctx_from is None:
        logger.warning(
            "RawDiff: left_commit_id %r "
            "could not be found", left_cid)
        return (False, repo, ctx_from, ctx_to)
    if ctx_to is None:
        logger.warning(
            "RawDiff: right_commit_id %r "
            "could not be found", right_cid)
        return (False, repo, ctx_from, ctx_to)
    return (True, repo, ctx_from, ctx_to)


def old_new_blob_oids(header, old_ctx, new_ctx):
    """Return a tuple of (old, new) blob oids."""
    old_path, new_path = old_new_file_path(header)
    old_bid = new_bid = NULL_BLOB_OID
    if old_path in old_ctx:
        cid = pycompat.sysstr(old_ctx.hex())
        old_bid = blob_oid(None, cid, old_path)
    if new_path in new_ctx:
        cid = pycompat.sysstr(new_ctx.hex())
        new_bid = blob_oid(None, cid, new_path)
    return old_bid, new_bid


def old_new_file_mode(header, old_ctx, new_ctx):
    """Return a tuple of (old, new) file mode."""
    old_path, new_path = old_new_file_path(header)
    old_mode, new_mode = b'0', b'0'
    if old_path in old_ctx:
        old_fctx = old_ctx[old_path]
        old_mode = gitmode[old_fctx.flags()]
    if new_path in new_ctx:
        new_fctx = new_ctx[new_path]
        new_mode = gitmode[new_fctx.flags()]
    return old_mode, new_mode


def old_new_file_path(header):
    """Return a tuple of (old, new) file path."""
    fname = header.filename()
    from_path, to_path = fname, fname
    if len(header.files()) > 1:
        # file is renamed
        from_path, to_path = header.files()
    return from_path, to_path


def _insert_blob_index(chunk, ctx_from, ctx_to):
    fname = chunk.filename()
    old_bid, new_bid = old_new_blob_oids(chunk, ctx_from, ctx_to)
    indexline = 'index %s..%s' % (old_bid, new_bid)
    indexline = pycompat.sysbytes(indexline)

    # Note: <mode> is required only when it didn't change between
    # the two changesets, otherwise it has a separate line
    if fname in ctx_from and fname in ctx_to:
        oldmode, mode = old_new_file_mode(chunk, ctx_from, ctx_to)
        if mode == oldmode:
            indexline += b' ' + mode
    indexline += b'\n'
    headerlines = chunk.header

    for index, line in enumerate(headerlines[:]):
        if line.startswith(b'--- '):
            headerlines.insert(index, indexline)
            break
    return b''.join(headerlines)
