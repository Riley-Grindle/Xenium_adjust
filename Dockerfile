FROM docker.io/mdiblbiocore/amazonlinux_curl:latest

RUN yum -y install gzip

RUN wget -O xeniumranger-3.1.1.tar.gz "https://cf.10xgenomics.com/releases/xeniumranger/xeniumranger-3.1.1.tar.gz?Expires=1749629941&Key-Pair-Id=APKAI7S6A5RYOXBWRPDA&Signature=PZuWtila856Dpz3DG4Bf-CyBLREFgCHxCOTGjFZ~V2Cfd5YCH60zdIcamSMiKNnDiRjjmO~y7ZV0H46tqW6tdhdtX63vZnD-9P43ganJSeSKj7WdjOvMJYyMR3Cv9UbyJnMnTm2V7HcTnerAtv9pbTSICduq4EjUf~sxmoSDKio465b-BBnAjRzF6vc9WXyzzb1KvLRp8UIVFp1VigTOjbcmScby8~2CaX-tYKK8JZV7jzTBCJzpTMf6GRzOR8Y5d4VPumzU4WbfUPpPEQPq7dSQoj7nmrPIo8rI8QsMACYcA4qonBhQmny3d9vwtJhwrVUX4RSdALXz~DoBMQbRvg__"

RUN tar -xzvf xeniumranger-3.1.1.tar.gz

RUN mv xeniumranger-xenium3.1  /usr/local/bin/

WORKDIR /mnt

ENV xenium /mnt/

ENTRYPOINT /usr/local/bin/xeniumranger-xenium3.1/bin/xeniumranger resegment --id=relabeled --xenium-bundle=$xenium --localcores=32 --localmem=128 --reset
