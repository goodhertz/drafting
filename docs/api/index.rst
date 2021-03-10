API
===

**Work in progress**

.. rubric:: Geometry

.. autosummary::
    :toctree: reference
    :template: module.rst

    drafting.geometry.Point
    drafting.geometry.Line
    drafting.geometry.Curve
    drafting.geometry.Rect

.. rubric:: Textsetting Classes

.. autosummary::
    :toctree: reference
    :template: module.rst

    drafting.text.reader.Style
    drafting.text.reader.StyledString
    drafting.text.composer.Composer

The most important thing to understand is that textsetting classes can be turned into vector classes via the ``.pen`` or ``.pens`` methods available on both ``StyledString`` and ``Composer`` — ``.pen`` gets you a single vector representation of a piece of text (aka a ``DATPen``), while ``.pens`` gets you a structured list of DATPen’s, aka a ``DATPens``.

.. rubric:: Vector/Path Classes

.. autosummary::
    :toctree: reference
    :template: module.rst

    drafting.pens.draftingpen.DraftingPen
    drafting.pens.draftingpens.DraftingPens