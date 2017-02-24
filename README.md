# org-process
Org-Process is an application for bulk processing of GC-MS data acquired from Agilent Mass Hunter analysis reports for TRH analysis.

## Usage
Usage is very simple:

1. Select the source folder - this should contain all the “AnalysisReport” Excel files exported from MassHunter that you want to calculate results for. The folder must contain all the blanks that you require and the blanks must have “BLK” in the filename. Additionally, the selected folder must have only either TRH C6-C10 results or TRH >C10-C40 results. You will need a separate folder for each batch that has different blanks.
2. Choose a file location and file name for the exported csv results file.
3. Select the test type (TRH C6-C10 or TRH >C10-C40)
4. Make any modifications to the default values presented for internal standards and calibrations (if required).
5. Press the “Start calculation” button.

A message box will let you know once the results file has been successfully exported.

If no internal standard peaks are found within the retention time (rt +- rt tolerance) and with the expected integration area (area +- area tolerance), then you’ll need to increase the tolerance of one or both of these until peaks are found. A message box will alert you to this as well as letting you know which sample failed the peak search, so you can go straight to the culprit data file to inspect it. In the case of a blank failing the peak search, the message will only tell you that a blank failed, not which one.
