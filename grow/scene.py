from opencmiss.zinc.context import Context
from opencmiss.zinc.material import Material

from .model import Model

class Scene(object):

    def __init__(self):
        self._context = Context("Scene")
        self._logger = self._context.getLogger()
        self._initialize()

    def getContext(self):
        return self._context

    def newModel(self, name):
        region = self._context.getDefaultRegion().createChild(name)
        return Model(self._context, region, self._materialModule)

    def _initialize(self):
        tess = self._context.getTessellationmodule().getDefaultTessellation()
        tess.setRefinementFactors(12)

        self._materialModule = self._context.getMaterialmodule()
        self._materialModule.defineStandardMaterials()

        mat = self._materialModule.createMaterial()
        mat.setName('solidBlue')
        mat.setManaged(True)
        mat.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.0, 0.2, 0.6])
        mat.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.0, 0.7, 1.0])
        mat.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        mat.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
        mat.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)

        mat = self._materialModule.createMaterial()
        mat.setName('transBlue')
        mat.setManaged(True)
        mat.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.0, 0.2, 0.6])
        mat.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.0, 0.7, 1.0])
        mat.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        mat.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
        mat.setAttributeReal(Material.ATTRIBUTE_ALPHA, 0.2)
        mat.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)

        mat = self._materialModule.createMaterial()
        mat.setName('transLightBlue')
        mat.setManaged(True)
        mat.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.0, 0.2, 0.6])
        mat.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.4, 0.8, 1.0])
        mat.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        mat.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
        mat.setAttributeReal(Material.ATTRIBUTE_ALPHA, 0.5)
        mat.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.7)

        mat = self._materialModule.createMaterial()
        mat.setName('solidTissue')
        mat.setManaged(True)
        mat.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.9, 0.7, 0.5])
        mat.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.9, 0.7, 0.5])
        mat.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        mat.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.2, 0.2, 0.3])
        mat.setAttributeReal(Material.ATTRIBUTE_ALPHA, 1.0)
        mat.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)

        glyphmodule = self._context.getGlyphmodule()
        glyphmodule.defineStandardGlyphs()

    def getScene(self):
        return self._context.getDefaultRegion().getScene()

