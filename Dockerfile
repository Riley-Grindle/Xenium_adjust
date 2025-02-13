FROM quay.io/rgrindle/rename_transcripts_xenium:v1.1.1

RUN apt-get update

RUN apt-get install gzip -y

RUN wget -O xeniumranger-3.1.0.tar.gz "https://cf.10xgenomics.com/releases/xeniumranger/xeniumranger-3.1.0.tar.gz?Expires=1739526168&Key-Pair-Id=APKAI7S6A5RYOXBWRPDA&Signature=coNnrvvDg5YptF9mT8SbKHa8E5DRZv7-AOMygjBP1HUfxizhQkgdu21Uh0KAHDjvSSqcgfhw5v6Na6ky8YWzh4i-jXQta74ieU1GHeGbjSRKYRrBSMHmjQiIVSKDqwdf9DKnyFjGPWdU0cu0PPLS94kaNS706HtbvaC0R2SQL4PIV8InWwwdyU6YBwfzzLnE9Pm34RbPfomPSC8gWhROZJu7fgpeRB03Nk-eBNot0oLn15hG4RBBAX-n3LKKcXCdbJw~cC5v~JJp1IwElufk8MaUlDCbO9LPPyBFqaMmDPHyBEd4FPofTdnQajHjtegvkC9gS3DnCzWVR8XteTOVbg__"

RUN tar -xzvf xeniumranger-3.1.0.tar.gz

ENV PATH="/app/xeniumranger-xenium3.1/bin/":$PATH

WORKDIR /mnt

ENV gene_panel /mnt/gene_panel.json
ENV features /mnt/custom_features.tsv
ENV xenium /mnt/

RUN sed -i.bak 's|modified-panel.json|/mnt/modified-panel.json|' /usr/local/bin/rename_gene_panel.py

ENTRYPOINT rename_gene_panel.py --gene_panel $gene_panel --map $features; modified=/mnt/modified-panel.json; xeniumranger relabel --id=relabled --xenium-bundle=$xenium --panel=$modified --localcores=32 --localmem=128
