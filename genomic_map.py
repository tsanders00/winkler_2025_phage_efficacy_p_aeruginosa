from IPython.display import Image
from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio import SeqIO

# read gbk file here with SeqIO
one=SeqIO.read("/Users/torben.sanders/Desktop/PhD/Corinna_project/p4ob1.gbk", "genbank")

assigned_functions = []
for record in [one]:
    for feature in record.features:
        if feature.qualifiers.get("function") in assigned_functions:
            continue
        else:
            assigned_functions.append(feature.qualifiers.get("function"))

gd_diagram = GenomeDiagram.Diagram("Phage Cocktail")
border_color = colors.black
marker = "BOX"
marker2 = "ARROW"
max_len = 0

for record in [one]:
    max_len = max(max_len, len(record))
    gd_track_for_features = gd_diagram.new_track(
        1,
        name=record.name,
        # title= record.name,
        greytrack=False,  # The grey background on the track
        start=0,
        end=len(record),
        height=0.3,  # change to increase the width of the elements on the map
        greytrack_labels=1,
    )

    gd_feature_set = gd_track_for_features.new_set()

    i = 0
    for feature in record.features:
        if feature.type != "CDS":
            continue

        if feature.qualifiers["function"] == ['unknown function']:  # light grey
            color = colors.lightgrey
            gd_feature_set.add_feature(
                feature,
                sigil=marker2,
                arrowshaft_height=1.0,
                color=color,
                # alpha=0.5,
                # border=colors.grey,

            )
        elif feature.qualifiers["function"] == ['connector']:  # light blue
            # color = colors.lightblue
            gd_feature_set.add_feature(
                feature,
                sigil=marker2,
                arrowshaft_height=1.0,
                color=(93, 173, 226),  # use RGB format to choose the colors for the elements on the map
                border=border_color,

            )
        elif feature.qualifiers["function"] == ['DNA, RNA and nucleotide metabolism']:  # light green
            # color = colors.khaki
            gd_feature_set.add_feature(
                feature,
                sigil=marker2,
                arrowshaft_height=1.0,
                color=(88, 214, 141),
                border=border_color,

            )
        elif feature.qualifiers["function"] == ['head and packaging']:  # light blue
            # color = colors.orange
            gd_feature_set.add_feature(
                feature,
                sigil=marker2,
                arrowshaft_height=1.0,
                arrohead_height=1.0,
                color=(93, 173, 226),
                border=border_color,

            )
        elif feature.qualifiers["function"] == ['lysis']:  # salmon
            # color = colors.salmon
            gd_feature_set.add_feature(
                feature,
                sigil=marker2,
                arrowshaft_height=1.0,
                color=(231, 76, 60),
                border=border_color,

            )
        elif feature.qualifiers["function"] == ['moron', ' auxiliary metabolic gene and host takeover']:  # purple
            # color = colors.orchid
            gd_feature_set.add_feature(
                feature,
                sigil=marker2,
                arrowshaft_height=1.0,
                color=(195, 155, 211),
                border=border_color,

            )
        elif feature.qualifiers["function"] == ['tail']:  # light blue
            # color = colors.
            gd_feature_set.add_feature(
                feature,
                sigil=marker2,
                arrowshaft_height=1,
                color=(93, 173, 226),
                border=border_color,
                borderwidth=1
            )
        elif feature.qualifiers["function"] == ['transcription regulation']:  # yellow
            # color = colors.yellow
            gd_feature_set.add_feature(
                feature,
                sigil=marker2,
                arrowshaft_height=1.0,
                color=(241, 196, 15),
                border=border_color,

            )
        elif feature.qualifiers["function"] == ['tRNAs']:  # yellow
            # color = colors.yellow
            gd_feature_set.add_feature(
                feature,
                sigil=marker2,
                arrowshaft_height=1.0,
                color=(241, 196, 15),
                border=border_color,

            )
        elif feature.qualifiers["function"] == ['other']:  # purple
            # color = colors.gray
            gd_feature_set.add_feature(
                feature,
                sigil=marker2,
                arrowshaft_height=1.0,
                color=(195, 155, 211),
                border=border_color,

            )
        else:  #
            color = colors.lightgrey
            gd_feature_set.add_feature(
                feature,
                sigil=marker2,
                arrowshaft_height=1.0,
                color=color,
                border=border_color,

            )
        i += 1

gd_diagram.draw(
    format="linear",
    orientation="landscape",
    pagesize="A1",
    fragments=1,
    start=0,
    end=max_len
)
gd_diagram.write("/Users/torben.sanders/Desktop/PhD/Corinna_project/phage_map.pdf", "PDF")