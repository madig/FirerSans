from pathlib import Path

import ufoLib2

FAMILY_NAME = "Firer Sans"

for path in Path("sources").glob("*.ufo"):
    ufo = ufoLib2.Font.open(path)

    ufo.info.familyName = FAMILY_NAME
    ufo.info.openTypeNamePreferredFamilyName = FAMILY_NAME
    if ufo.info.styleMapFamilyName is not None:
        ufo.info.styleMapFamilyName = ufo.info.styleMapFamilyName.replace(
            "Fira Sans", FAMILY_NAME
        )
    if ufo.info.postscriptFullName is not None:
        ufo.info.postscriptFullName = ufo.info.postscriptFullName.replace(
            "Fira Sans", FAMILY_NAME
        )

    area = ufo.lib["com.ht.spacer.area"]
    ufo["underscore"].lib["com.ht.spacer.area"] = area - 150
    ufo["one"].lib["com.ht.spacer.area"] = area + 150

    ufo.save()
