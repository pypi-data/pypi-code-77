# Copyright 2021 Sushil Khanchi <sushilkhanchi97@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import grpc
import pytest
from hgitaly.tests.common import (
    make_empty_repo,
)
from hgitaly.stub.diff_pb2 import (
    RawDiffRequest,
)
from mercurial import (
    node,
)
from hgitaly.stub.diff_pb2_grpc import DiffServiceStub
from .. import diff


def test_concat_resplit():
    in_data = iter([b'AAB', b'BCCDD'])
    max_size = 2
    data = diff.concat_resplit(in_data, max_size)
    data = list(data)
    assert data == [b'AA', b'BB', b'CC', b'DD']


def test_raw_diff(grpc_channel, server_repos_root):
    grpc_stub = DiffServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    ctx0 = wrapper.commit_file('foo', content="I am oof\n",
                               message=b'added foo')
    ctx1 = wrapper.commit_file('foo', content="I am foo\n",
                               message=b'changes foo')
    wrapper.command(b'mv', wrapper.repo.root + b'/foo',
                    wrapper.repo.root + b'/zoo')
    wrapper.command(b'ci', message=b"rename foo to zoo")
    ctx2 = wrapper.repo[b'.']
    sha0, sha1, sha2 = ctx0.hex(), ctx1.hex(), ctx2.hex()

    def do_rpc(left_sha, right_sha):
        request = RawDiffRequest(
                    repository=grpc_repo,
                    left_commit_id=left_sha,
                    right_commit_id=right_sha,
                  )
        response = grpc_stub.RawDiff(request)
        return b''.join(resp.data for resp in response)

    # case 1: actual test
    resp = do_rpc(sha0, sha1)
    respheader = (
        b'diff --git a/foo b/foo\n'
    )
    resphunk = (
        b'--- a/foo\n'
        b'+++ b/foo\n'
        b'@@ -1,1 +1,1 @@\n'
        b'-I am oof\n'
        b'+I am foo\n'
    )
    assert resp.startswith(respheader) and resp.endswith(resphunk)

    # case 2: with null node
    resp = do_rpc(node.nullhex, sha0)
    respheader = (
        b'diff --git a/foo b/foo\n'
    )
    resphunk = (
        b'--- /dev/null\n'
        b'+++ b/foo\n'
        b'@@ -0,0 +1,1 @@\n'
        b'+I am oof\n'
    )
    assert resp.startswith(respheader) and resp.endswith(resphunk)

    # case 3: with file renaming
    resp = do_rpc(sha1, sha2)
    assert resp == (
        b'diff --git a/foo b/zoo\n'
        b'similarity index 100%\n'
        b'rename from foo\n'
        b'rename to zoo\n'
    )

    # case 4: when commit_id does not correspond to a commit
    sha_not_exists = b'deadnode' * 5
    # varient 1
    with pytest.raises(grpc.RpcError) as exc_info:
        do_rpc(sha0, sha_not_exists)
    assert exc_info.value.code() == grpc.StatusCode.UNKNOWN
    assert 'exit status 128' in exc_info.value.details()
    # varient 2
    with pytest.raises(grpc.RpcError) as exc_info:
        do_rpc(sha_not_exists, sha0)
    assert exc_info.value.code() == grpc.StatusCode.UNKNOWN
    assert 'exit status 128' in exc_info.value.details()
