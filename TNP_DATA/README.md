### Tudor Networks of Power - Correspondence Network Dataset

Ruth Ahnert and Sebastian E. Ahnert

© 2023. This work is licensed under a CC BY-NC-SA 4.0 license. 

---

**If using this dataset, please cite:**
**R. Ahnert, S E. Ahnert, "Tudor Networks of Power", Oxford University Press, 2023.**

The data is released under a Creative Commons BY-NC-SA 4.0 license, which:
- requires attribution
- permits distribution, remixing, adaptation, or building upon this data as long as the modified material is licensed under identical terms
- only permits non-commercial uses of the work

This data contains a temporal, directed edgelist representing (to the best of our knowledge) all items of correspondence in the Tudor State Papers (1509-1603), which are the official government records of the Tudor period in England. The data covers State Papers Domestic and Foreign.

The dataset was created by first extracting the relevant XML metadata of the State Papers Online resource developed by Gale Cengage. We would like to acknowledge the help and support that Gale Cengage provided for our research. The XML metadata closely corresponds to the State Papers Calendars of the 19th century. These contain many ambiguities regarding the identities of people and places, resulting in an extensive effort on our part to disambiguate and de-duplicate person identities and places of writing. The details of this process can be found in our book (see citation above).

The dataset contains:

- letter_edgelist.tsv	Directed temporal edge list of letters
- people_labels.tsv	Key for the person IDs used in letter_edgelist.tsv
- place_labels.tsv	Key for the place IDs used in letter_edgelist.tsv
- people_metadata.tsv	Additional metadata and URIs for a subset of people
- places_metadata.tsv	Geolocations and metadata for a large subset of places

Both the code and more extensive datasets that give context to the data curation process, the network analysis methods, and quantitative results in the book will be made available separately.
