import os

from scaffoldmaker.utils.zinc_utils import *

from opencmiss.zinc.graphics import Graphics
from opencmiss.zinc.glyph import Glyph
from opencmiss.zinc.element import Element
from opencmiss.zinc.field import Field

class Model(object):

    def __init__(self, context, region, materialModule):
        self._context = context
        self._region = region
        self._materialModule = materialModule

        self._surfaces = []

    def load(self, exnode, exelem):
        for graphics in self._surfaces:
            graphics.setMaterial(self._materialModule.findMaterialByName('transBlue'))

        subregion = self._region.createChild(exelem)
        subregion.readFile(exnode)
        subregion.readFile(exelem)
        
        fm = subregion.getFieldmodule()
        fm.beginChange()
        self._coordinates = fm.findFieldByName('coordinates')
        self._magnitude = fm.createFieldMagnitude(self._coordinates)
        self._magnitude.setName('magnitude')
        self._magnitude.setManaged(True)
        fm.endChange()

        scene = subregion.getScene()
        scene.beginChange()
        #self._createPointGraphics(scene, self._coordinates, 'points', 'white')
        self._createLineGraphics(scene, self._coordinates, 'lines', 'white')
        self._createSurfaceGraphics(scene, self._coordinates, 'surfaces', 'transLightBlue')
        scene.endChange()
    
    def _createPointGraphics(self, scene, coordinates, name, color):
        graphics = scene.createGraphicsPoints()
        graphics.setCoordinateField(coordinates)
        graphics.setMaterial(self._materialModule.findMaterialByName(color))
        graphics.setName(name)
        samplingAttr = graphics.getGraphicssamplingattributes()
        samplingAttr.setElementPointSamplingMode(Element.POINT_SAMPLING_MODE_SET_LOCATION)
        samplingAttr.setLocation([0.0])
        graphics.setFieldDomainType(Field.DOMAIN_TYPE_NODES)

        glyph = self._context.getGlyphmodule().findGlyphByGlyphShapeType(Glyph.SHAPE_TYPE_SPHERE)

        pointAttr = graphics.getGraphicspointattributes()
        pointAttr.setGlyph(glyph)
        pointAttr.setBaseSize([3, 3, 3])

    def _createLineGraphics(self, scene, coordinates, name, color):
        graphics = scene.createGraphicsLines()
        graphics.setCoordinateField(coordinates)
        graphics.setMaterial(self._materialModule.findMaterialByName(color))
        graphics.setName(name)

    def _createSurfaceGraphics(self, scene, coordinates, name, color):
        graphics = scene.createGraphicsSurfaces()
        graphics.setCoordinateField(coordinates)
        graphics.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_SHADED)
        graphics.setMaterial(self._materialModule.findMaterialByName(color))
        graphics.setName(name)
        self._surfaces.append(graphics)
