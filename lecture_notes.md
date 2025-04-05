# Lecture Notes

## Page 1

Okay, here are the processed lecture notes, based on the OCR output and image, formatted in Markdown:

# DATA PREPROCESSING OF ILLUMINA SEQUENCE DATA

**Page No.:** 14

**AIM:**

*   To preprocess raw data from Illumina using different tools and remove or trim any bad data.

**SOFTWARES USED:**

*   (i) FastQC: for initial and post-processing quality check
*   (ii) BBDuk: for adapter contamination removal

**DATASETS:**

*   (i) Raw sequencing data (paired-end FASTQ files)
*   (ii) Reference Genome

**PROCEDURE:**

*   Unzip folders and datasets.
*   Download necessary tools.
*   Run FastQC on the raw FASTQ files.
    *   Checked:
        *   Per base sequence quality
        *   Adapter contamination
        *   GC content
        *   Read length distribution
        *   Per base N content
        *   Per sequence quality score
        *   Per tile sequence quality
        *   Duplicate sequences
*   Adapter contamination was found.
*   BBDuk was used to remove adapter contamination.
*   FastQC was used again to check the preprocessed data.
*   Adapter contamination was removed.

**Teacher's Signature:**


---

## Page 2

Okay, here are the processed lecture notes, based on the OCR output and image, formatted in Markdown:

# RESULTS:

**Page No.:** 15

*   Adapter contamination was removed, and preprocessed data passed Quality Control.


---

## Page 3

Okay, based on the image, here's the information extracted and presented as a structured overview of the Illumina sequence data preprocessing workflow. Since the image depicts a flowchart, I've used a numbered list to represent the sequential steps.

# Illumina Sequence Data Preprocessing Workflow

1.  **START**
2.  **Raw FASTQ files (Paired-end reads)**
3.  **Quality Control: FastQC**
    *   If QC fails due to contamination:
        *   **Adapter Contamination**
        *   **Adapter Trimming using BBDuk**
        *   Return to Step 3 (Quality Control)
    *   If **No Contamination, QC passed**
4.  **Final Preprocessed Data**
5.  **STOP**


---

