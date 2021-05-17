import setuptools

long_description = """
# Drafting

Color and geometric primitives
"""

setuptools.setup(
    name="drafting",
    version="0.1.8",
    author="Rob Stenson / Goodhertz",
    author_email="rob@goodhertz.com",
    description="Color and geometric primitives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goodhertz/drafting",
    packages=[
        "drafting",
        "drafting.sh",
        "drafting.grid",
        "drafting.pens",
        "drafting.text",
        "drafting.color",
        "drafting.geometry",
        "drafting.fontgoggles",
        "drafting.interpolation",
        "drafting.fontgoggles.font",
        "drafting.fontgoggles.misc",
        "drafting.fontgoggles.compile",
    ],
    extras_require={
        "text": [
            "skia-pathops",
            "freetype-py",
            "uharfbuzz>=0.14.0",
            "unicodedata2",
            "ufo2ft",
            "python-bidi",
        ]
    },
    install_requires=[
        "fonttools[ufo,lxml,woff,type1]>=4.21.1",
        "fontPens",
        "more-itertools",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
