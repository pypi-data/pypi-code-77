# Copyright 1999-2020 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..utils import infer_dtype, implement_scipy
from .core import spspecial, TensorSpecialBinOp


class TensorXLogY(TensorSpecialBinOp):
    _func_name = 'xlogy'

    @classmethod
    def _is_sparse(cls, x1, x2):
        if hasattr(x1, 'issparse') and x1.issparse():
            return True
        return False


@implement_scipy(spspecial.xlogy)
@infer_dtype(spspecial.xlogy)
def xlogy(x1, x2, out=None, where=None, **kwargs):
    op = TensorXLogY(**kwargs)
    return op(x1, x2, out=out, where=where)
