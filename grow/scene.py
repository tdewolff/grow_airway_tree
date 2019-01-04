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
        return Model(region, self._materialModule)

    def _initialize(self):
        tess = self._context.getTessellationmodule().getDefaultTessellation()
        tess.setRefinementFactors(12)

        self._materialModule = self._context.getMaterialmodule()
        self._materialModule.defineStandardMaterials()

        solidBlue = self._materialModule.createMaterial()
        solidBlue.setName('solidBlue')
        solidBlue.setManaged(True)
        solidBlue.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.0, 0.2, 0.6])
        solidBlue.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.0, 0.7, 1.0])
        solidBlue.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        solidBlue.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
        solidBlue.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)

        transBlue = self._materialModule.createMaterial()
        transBlue.setName('transBlue')
        transBlue.setManaged(True)
        transBlue.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.0, 0.2, 0.6])
        transBlue.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.0, 0.7, 1.0])
        transBlue.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        transBlue.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
        transBlue.setAttributeReal(Material.ATTRIBUTE_ALPHA, 0.3)
        transBlue.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)

        solidTissue = self._materialModule.createMaterial()
        solidTissue.setName('solidTissue')
        solidTissue.setManaged(True)
        solidTissue.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.9, 0.7, 0.5])
        solidTissue.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.9, 0.7, 0.5])
        solidTissue.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        solidTissue.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.2, 0.2, 0.3])
        solidTissue.setAttributeReal(Material.ATTRIBUTE_ALPHA, 1.0)
        solidTissue.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)

        glyphmodule = self._context.getGlyphmodule()
        glyphmodule.defineStandardGlyphs()

