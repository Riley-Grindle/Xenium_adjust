import sys
import io
from alive_progress import alive_bar


with open(sys.argv[1], "r") as tx_file:
    transcripts = tx_file.readlines()

with open(sys.argv[2], "r") as subset_file:
    subset_cells = subset_file.readlines()

subset_ls = [None] * len(subset_cells)
total = len(subset_cells)
with alive_bar(total) as bar:
    for i in range(len(subset_cells)):
        if i < 3:
            pass
        else:
            subset_ls[i] = subset_cells[i].split(",")[0]
        bar()

kept_transcripts = [None] * len(transcripts)
count = 0
additions = 0
total = len(transcripts)
with alive_bar(total) as bar:
    for line in transcripts:
        cell_id = line.split(",")[1]
        if cell_id in subset_ls:
           kept_transcripts[count] = line
           additions += 1
        count += 1
        bar()


cleaned_list = list(filter(None, kept_transcripts))

transcript_writeable = "\n".join(cleaned_list)

with open("subset_transcripts.csv", "w") as  subset_tx_file:
    subset_tx_file.write(transcript_writeable)
subset_tx_file.close()

