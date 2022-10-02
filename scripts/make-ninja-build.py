from pathlib import Path

from fontTools.designspaceLib import DesignSpaceDocument
from ninja.ninja_syntax import Writer

SOURCE_DIR = Path("sources")
OUTPUT_DIR = Path("build")

OUTPUT_DIR.mkdir(exist_ok=True)
with open(OUTPUT_DIR / "build.ninja", "w") as f:
    w = Writer(f)
    w.variable("letterspacer_conf", str(SOURCE_DIR / "htletterspacer.txt"))
    w.variable("stylespace", str(SOURCE_DIR / "FiraSans.stylespace"))
    w.rule(
        "autospace",
        command="py -m htletterspacer --config $letterspacer_conf $in --output $out",
    )
    w.rule("copy_file", command="cp -p $in $out")
    w.rule(
        "fontmake",
        command=[
            "py -m fontmake --verbose WARNING -m $in -o variable --output-path $out \
            && py -m statmake --stylespace $stylespace --designspace $in $out"
        ],
    )

    family_fea = SOURCE_DIR / "family.fea"
    family_fea_target = OUTPUT_DIR / family_fea.name
    w.build(str(family_fea_target), rule="copy_file", inputs=[str(family_fea)])

    for path in SOURCE_DIR.glob("*.designspace"):
        designspace = DesignSpaceDocument.fromfile(path)
        source_path_targets = []
        for source in designspace.sources:
            source_path = path.parent / source.filename
            source_path_target = OUTPUT_DIR / source_path.name
            w.build(
                str(source_path_target),
                rule="autospace",
                inputs=[str(source_path)],
                implicit=[str(family_fea_target)],
            )
            source_path_targets.append(source_path_target)

        path_target = OUTPUT_DIR / path.name
        w.build(str(path_target), rule="copy_file", inputs=[str(path)])
        target_ttf = OUTPUT_DIR / path_target.with_suffix(".ttf").name
        w.build(
            str(target_ttf),
            rule="fontmake",
            inputs=[str(path_target)],
            implicit=[str(p) for p in source_path_targets] + [str(family_fea_target)],
        )
