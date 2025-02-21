FROM quay.io/rgrindle/rename_transcripts_xenium:v1.1.1

RUN apt-get update

RUN apt-get install gzip -y

RUN wget -O xeniumranger-3.1.0.tar.gz "https://cf.10xgenomics.com/releases/xeniumranger/xeniumranger-3.1.0.tar.gz?Expires=1740129043&Key-Pair-Id=APKAI7S6A5RYOXBWRPDA&Signature=VlckasZH3L6Y59KZmnW-HVnbFutxa6UQvA~oPg6KlPJD9N~3fUrykvcZKG~KqPOYJMIE8OEVnpldKlsVVcQALuvhQamzMNdvpF2TRs4tmQBp0IvYjdzvqb9bwILx6KZFKWfFNwPSfQfnr90CYLsqlyo~lVJyELRV4Q2STNcolKYea8tkzSllTkzY0M36aLvGCxs6QxnOZVDV0v4Bxffuv-KZB6TD5GyYyhEonEJYqR7SKs0J5FBKQCSIIWcLvq61UbkgbdnhTiOkZaxUVWaS4~cPpHe7VyDGZXsfA4YZ4vFH732An~afOd8c7gw~RrMIv1JQJ6siA-IPIk7CM4b9CQ__"

RUN tar -xzvf xeniumranger-3.1.0.tar.gz

ENV PATH="/app/xeniumranger-xenium3.1/bin/":$PATH

WORKDIR /mnt

ENV gene_panel /mnt/gene_panel.json
ENV features /mnt/custom_features.tsv
ENV xenium /mnt/

RUN sed -i.bak 's|modified-panel.json|/mnt/modified-panel.json|' /usr/local/bin/rename_gene_panel.py

ENTRYPOINT rename_gene_panel.py --gene_panel $gene_panel --map $features; modified=/mnt/modified-panel.json; xeniumranger relabel --id=relabled --xenium-bundle=$xenium --panel=$modified --localcores=32 --localmem=128
