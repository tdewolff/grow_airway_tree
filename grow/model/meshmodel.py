import os

from scaffoldmaker.utils.zinc_utils import *

from opencmiss.zinc.graphics import Graphics
from opencmiss.zinc.field import Field
from opencmiss.utils.maths import vectorops
from opencmiss.zinc.status import OK as ZINC_OK

class MeshModel(object):

    def __init__(self, region, materialModule):
        self._region = region
        self._materialModule = materialModule

    def load(self, exnode, exelem):
        self._region.readFile(exnode)
        self._region.readFile(exelem)
        
        self._scene = self._region.getScene()
        fm = self._region.getFieldmodule()
        fm.beginChange()
        self._coordinates = fm.findFieldByName('coordinates')
        self._magnitude = fm.createFieldMagnitude(self._coordinates)
        self._magnitude.setName('leftmag')
        self._magnitude.setManaged(True)
        fm.endChange()

        self.__setupScene()

    def __setupScene(self):
        scene = self._region.getScene()
        scene.beginChange()
        self._createLineGraphics(scene, self._coordinates, 'displayLinesLeft', 'white')
        self._surface = self._createSurfaceGraphics(scene, self._coordinates, 'displaySurfacesLeft', 'transBlue')

        scene.endChange()

    def _createLineGraphics(self, scene, coordinates, name, color):
        materialModule = self._materialModule
        lines = scene.createGraphicsLines()
        lines.setCoordinateField(coordinates)
        lines.setName(name)
        black = materialModule.findMaterialByName(color)
        lines.setMaterial(black)

    def _createSurfaceGraphics(self, scene, coordinates, name, color):
        surface = scene.createGraphicsSurfaces()
        surface.setCoordinateField(coordinates)
        surface.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_SHADED)
        surfacesMaterial = self._materialModule.findMaterialByName(color)
        surface.setMaterial(surfacesMaterial)
        surface.setName(name)
        return surface
