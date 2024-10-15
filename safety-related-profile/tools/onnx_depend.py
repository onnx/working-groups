"""
 *******************************************************************************
 * ACETONE: Predictable programming framework for ML applications in safety-critical systems
 * Copyright (c) 2024. ONERA
 * Copyright (c) 2024. AIRBUS
 * This file is part of ACETONE
 *
 * ACETONE is free software ;
 * you can redistribute it and/or modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation ;
 * either version 3 of  the License, or (at your option) any later version.
 *
 * ACETONE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY ;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License along with this program ;
 * if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
 ******************************************************************************
"""
import onnx
import argparse
from onnx import (
    defs,
    IR_VERSION,
    __version__
)
from onnx.defs import onnx_opset_version

if __name__ == "__main__":
    print(f"onnx.__version__={__version__!r}, opset={onnx_opset_version()}, IR_VERSION={IR_VERSION}")    
    parser = argparse.ArgumentParser(description='print/modify onnx model strings')
    parser.add_argument('--model_path', required=True,help='onnx model path')
    args = parser.parse_args()

    onnx_model = onnx.load(args.model_path)
    onnx.checker.check_model(onnx_model)
    print('\nOperator dependencies:')
    local_func = [f.name for f in onnx_model.functions]
    op = {}
    for typ in onnx_model.graph.node:
        if typ.op_type not in local_func:
            #collect the onnx operator used in the model nodes except local function names
            op[typ.op_type] = defs.get_schema(typ.op_type,'').since_version
    for f in onnx_model.functions:
        for typ in f.node:
            if typ.op_type not in local_func:
                #collect the onnx operator used in the local functions except other local function names
                op[typ.op_type] = defs.get_schema(typ.op_type,'').since_version

    sops = [f'{x}\t\tv{op[x]}' for x in sorted(list(op.keys()))]
    print ('\n'.join(sops))
