import sys
import os
from PySide import QtGui
from src.view import View
from src.scene import Scene

from aether.diagnostics import set_diagnostics_on
from aether.indices import define_problem_type
from aether.geometry import *
from aether.exports import *
from aether.growtree import grow_tree


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

def generate(airwayIpnode, airwayIpelem, surfaceIpnode, surfaceIpelem, options):
    #define_node_geometry(airwayIpnode)
    #define_1d_elements(airwayIpelem)

    #define_node_geometry_2d(surfaceIpnode)
    #define_elem_geometry_2d(surfaceIpelem, 'unit')

    make_data_grid(0, options["gridSize"], False, 'test', 'test')
    evaluate_ordering()
    group_elem_parent_term(options["startNode"])
    grow_tree(options["startNode"], 1, options["angleMax"], options["angleMin"], options["branchFraction"], options["lengthLimit"], options["shortestLength"], options["rotationLimit"])

    export_node_geometry('.tmp', 'out')
    export_1d_elem_geometry('.tmp', 'out')
    
    airwayModel.load('.tmp.exnode', '.tmp.exelem')

def save(exnode, exelem):
    export_node_geometry(exnode, 'out')
    export_1d_elem_geometry(exelem, 'out')

app = QtGui.QApplication(sys.argv)
scene = Scene()
airwayModel = scene.newModel('airway')
surfaceModel = scene.newModel('surface')

view = View(scene)
view.airwayCallback(loadAirway)
view.surfaceCallback(loadSurface)
view.generateCallback(generate)
view.saveCallback(save)
view.setAirways('airway_tree_FRC.ipnode', 'airway_tree_FRC.ipelem')
view.setOutputs('out.exnode', 'out.exelem')
view.setInfo("""
<h2>Grow airway tree</h2>
<p>This GUI provides an easy interface for the grow_tree Fortran code in lungsim. It allows the visualization of the airway tree and the surface mesh and allows configuring the growth algorithm.</p>
<p>Created for use within the Auckland Bioengineering Institute at the University of Auckland.</p>
<h3>Usage</h3>
<p>Select the initial airway tree (.ipnode and .ipelem) and click Load. Then select the surface mesh (.ipnode and .ipelem) into which the airways should be grown, and click Load. Both the airway tree and surface mesh are now visible in the 3D view.</p>
<p>The algorithm can be configured using the following settings:</p>
<ul>
<li><b>Grid size:</b> distance between seed points that the surface mesh gets filled with</li>
<li><b>Start node:</b> the node number from which growing starts, this branch must have final nodes within the surface mesh!</li>
<li><b>Angle max:</b> maximum branch angle with parent</li>
<li><b>Angle min:</b> minimum branch angle with parent</li>
<li><b>Branch fraction:</b> fraction of distance (to COFM) to branch</li>
<li><b>Length limit:</b> minimum length of a generated branch</li>
<li><b>Shortest length:</b> length that short branches are reset to (shortest in model)</li>
<li><b>Rotation limit:</b> maximum angle of rotatin of branching plane</li>
</ul>
<p><b style="color:red">Warning:</b> make sure to select the largest surface mesh first to avoid the Fortran code from crashing.</p>
<p>When the airway tree is complete you can export the data by clicking Save after selecting the output file names (.exnode and .exelem).</p>
""")
view.show()
sys.exit(app.exec_())


# Print errors
num = model._logger.getNumberOfMessages()
for i in range(0, num):
    print model._logger.getMessageTextAtIndex(i)
