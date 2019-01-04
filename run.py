import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

import sys
import os
from PySide import QtGui
from grow.view.lungmodelwidget import LungModelWidget
from grow.model.lungmodel import LungModel

from aether.diagnostics import set_diagnostics_on
from aether.indices import define_problem_type
from aether.geometry import define_node_geometry_2d, define_elem_geometry_2d, make_data_grid, evaluate_ordering, \
    define_data_geometry, define_node_geometry, define_1d_elements, group_elem_parent_term
from aether.exports import export_node_geometry_2d, export_elem_geometry_2d, export_data_geometry, export_node_geometry, \
    export_1d_elem_geometry
from aether.growtree import grow_tree

app = QtGui.QApplication(sys.argv)
model = LungModel()
airwayModel = model.getMeshModel('airway')
surfaceModel = model.getMeshModel('surface')

set_diagnostics_on(False)
define_problem_type('grow_tree')

def loadAirway(ipnode, ipelem):
    exnode = os.path.splitext(ipnode)[0] + '.exnode'
    exelem = os.path.splitext(ipelem)[0] + '.exelem'

    define_node_geometry(ipnode)
    define_1d_elements(ipelem)
    export_node_geometry(exnode, 'airway')
    export_1d_elem_geometry(exelem, 'airway')
    
    airwayModel.load(exnode, exelem)

def loadSurface(ipnode, ipelem):
    node = os.path.splitext(ipnode)[0]
    elem = os.path.splitext(ipelem)[0]

    define_node_geometry_2d(ipnode)
    define_elem_geometry_2d(ipelem, 'unit')
    export_node_geometry_2d(node, 'surface', 0)
    export_elem_geometry_2d(elem, 'surface', 0, 0)

    surfaceModel.load(node+'.exnode', elem+'.exelem')

def generate(options, exnode, exelem):
    make_data_grid(0, options["gridSize"], False, 'test', 'test')
    evaluate_ordering()
    group_elem_parent_term(options["startNode"])
    grow_tree(options["startNode"], 1, options["angleMax"], options["angleMin"], options["branchFraction"], options["lengthLimit"], options["shortestLength"], options["rotationLimit"])

    export_node_geometry(exnode, 'out')
    export_1d_elem_geometry(exelem, 'out')
    
    airwayModel.load(exnode, exelem)

view = LungModelWidget(model)
view.airwayCallback(loadAirway)
view.surfaceCallback(loadSurface)
view.generateCallback(generate)
view.setAirways('airway_tree_FRC.ipnode', 'airway_tree_FRC.ipelem')
view.setOutputs('out.exnode', 'out.exelem')
view.show()
sys.exit(app.exec_())

# Print errors
num = model._logger.getNumberOfMessages()
for i in range(0, num):
    print model._logger.getMessageTextAtIndex(i)
