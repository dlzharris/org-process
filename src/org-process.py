"""
Module: org-process.py
Runs the Org-Process application for bulk processing of GC-MS data acquired
from Agilent Mass Hunter analysis reports for TRH analysis.

Author: Daniel Harris
Title: Data & Procedures Officer
Organisation: DPI Water
Date modified: 24/02/2017

External dependencies: PyQT4

Classes:
MainApp: Constructor for the main application.

Functions:
Main: Runs the Org-Process application.
"""

import glob
import sys
from pprint import pprint

from PyQt4 import QtGui

import op
import opx
import opui

__author__ = 'Daniel Harris'
__date__ = '9 March 2017'
__email__ = 'daniel.harris@dpi.nsw.gov.au'
__version__ = '1.0.1'


class MainApp(opui.Ui_MainWindow, QtGui.QMainWindow):
    """
    Constructor for the main application
    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        # Set analysis type
        self.analysis_c6_c10 = opx.DEF_ANALYSIS_C6_C10

        # Set default values
        self.doubleSpinBoxRtTarget.setValue(opx.DEF_ISTD_RT_C6_C10)
        self.doubleSpinBoxRtTolerance.setValue(opx.DEF_ISTD_RT_TOLERANCE_C6_C10)
        self.spinBoxAreaTarget.setValue(opx.DEF_ISTD_AREA_TARGET_C6_C10)
        self.spinBoxAreaTolerance.setValue(opx.DEF_ISTD_AREA_TOLERANCE_C6_C10)
        self.doubleSpinBoxConcentration.setValue(opx.DEF_ISTD_CONC_C6_C10)
        self.radioButtonC6_C10.setChecked(self.analysis_c6_c10)
        self.doubleSpinBoxDilutionFactor.setValue(opx.DEF_DILUTION_FACTOR_C6_C10)
        self.doubleSpinBoxCalibrationSlope.setValue(opx.DEF_CALIBRATION_SLOPE)
        self.doubleSpinBoxCalibrationIntercept.setValue(opx.DEF_CALIBRATION_INTERCEPT)

        # Connect signals
        self.toolButtonDataDirectory.clicked.connect(self.directoryPicker)
        self.toolButtonResultsFile.clicked.connect(self.filePicker)
        self.radioButtonC6_C10.toggled.connect(self.selectTestType)
        self.pushButtonStart.clicked.connect(self.startCalculation)


    def directoryPicker(self):
        """Shows directory picker dialog and places directory name in text box."""
        self.lineEditDataDirectory.setText(QtGui.QFileDialog.getExistingDirectory(
            caption="Open analytic report directory",
            directory="/home",
            options=QtGui.QFileDialog.ShowDirsOnly
        ))

    def filePicker(self):
        """Shows file picker dialog and places output filename in text box."""
        self.lineEditResultsFile.setText(QtGui.QFileDialog.getSaveFileName(
            caption="Save results file name",
            directory="/home",
            filter="CSV files (*.csv)"
        ))

    def selectTestType(self):
        self.analysis_c6_c10 = not self.analysis_c6_c10

        # Change displayed defaults
        if self.analysis_c6_c10:
            self.doubleSpinBoxRtTarget.setValue(opx.DEF_ISTD_RT_C6_C10)
            self.doubleSpinBoxRtTolerance.setValue(opx.DEF_ISTD_RT_TOLERANCE_C6_C10)
            self.spinBoxAreaTarget.setValue(opx.DEF_ISTD_AREA_TARGET_C6_C10)
            self.spinBoxAreaTolerance.setValue(opx.DEF_ISTD_AREA_TOLERANCE_C6_C10)
            self.doubleSpinBoxConcentration.setValue(opx.DEF_ISTD_CONC_C6_C10)
            self.doubleSpinBoxDilutionFactor.setValue(opx.DEF_DILUTION_FACTOR_C6_C10)
        else:
            self.doubleSpinBoxRtTarget.setValue(opx.DEF_ISTD_RT_C10_C40)
            self.doubleSpinBoxRtTolerance.setValue(opx.DEF_ISTD_RT_TOLERANCE_C10_C40)
            self.spinBoxAreaTarget.setValue(opx.DEF_ISTD_AREA_TARGET_C10_C40)
            self.spinBoxAreaTolerance.setValue(opx.DEF_ISTD_AREA_TOLERANCE_C10_C40)
            self.doubleSpinBoxConcentration.setValue(opx.DEF_ISTD_CONC_C10_C40)
            self.doubleSpinBoxDilutionFactor.setValue(opx.DEF_DILUTION_FACTOR_C10_C40)

    def startCalculation(self):
        # User inputs
        dir = str(self.lineEditDataDirectory.text())
        out_filepath = str(self.lineEditResultsFile.text())

        # Make list of all blank files in directory
        blank_data_list = []
        blank_pattern = dir + '\*' + opx.BLANK_TAG + '*'
        blank_file_list = glob.glob(blank_pattern)

        # Select the correct internal standard
        istd_rt = self.doubleSpinBoxRtTarget.value()
        istd_rt_tolerance = self.doubleSpinBoxRtTolerance.value()
        istd_area_target = self.spinBoxAreaTarget.value()
        istd_area_tolerance = self.spinBoxAreaTolerance.value()
        istd_concentration = self.doubleSpinBoxConcentration.value()
        dilution_factor = self.doubleSpinBoxDilutionFactor.value()
        calibration_slope = self.doubleSpinBoxCalibrationSlope.value()
        calibration_intercept = self.doubleSpinBoxCalibrationIntercept.value()

        for f in blank_file_list:
            blank = op.get_data_from_report(f)[2]
            blank_data_list.append(blank)
        try:
            blank_average = op.BlankAverage(
                blank_data=blank_data_list,
                analysis_c6_c10=self.analysis_c6_c10,
                istd_rt=istd_rt,
                istd_rt_tolerance=istd_rt_tolerance,
                istd_area_target=istd_area_target,
                istd_area_tolerance=istd_area_tolerance)
        except op.IstdError, e:
            txt = "ISTD error encountered on blank: %s" %e
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText(txt)
            msg.setWindowTitle("ISTD error encountered!")
            msg.exec_()
            return

        # Make exclude list for files that should not be analysed
        temp_files = glob.glob(dir + '~')
        excel_files = glob.glob(dir + '*.xls*')
        exclude_list = [x for x in glob.glob(dir + '\*') if x in temp_files and x not in excel_files]
        # Make list of all sample files in directory (includes QC)
        sample_file_list = [x for x in glob.glob(dir + '\*') if x not in blank_file_list and x not in exclude_list]

        # Initialise empty list for storing results
        result_set = []

        # Iterate through sample files and calculate results
        for f in sample_file_list:
            sample_name, analysis_time, peak_data = op.get_data_from_report(f)

            try:
                # Calculate C6-C10
                if self.analysis_c6_c10:
                    blank_average.area = blank_average.area_c6_c10
                    i_c6 = 0
                    i_c10 = op.get_fraction_end_index(peak_data, opx.C6_C10_END)
                    conc_c6_c10 = op.calculate_sample_concentration(
                        peak_data_list=peak_data,
                        blank=blank_average,
                        low_index=i_c6,
                        high_index=i_c10,
                        istd_rt=istd_rt,  # USER INPUT
                        istd_rt_tolerance=istd_rt_tolerance,  # USER INPUT
                        istd_area_target=istd_area_target,  # USER INPUT
                        istd_area_tolerance=istd_area_tolerance,  # USER INPUT
                        calibration_slope=calibration_slope,  # USER INPUT
                        calibration_intercept=calibration_intercept,  # USER INPUT
                        istd_concentration=istd_concentration,  # USER INPUT
                        dilution_factor=dilution_factor)  # USER INPUT

                    result = {
                        'sample_name': sample_name,
                        'analysis_time': analysis_time,
                        'conc_c6_c10': conc_c6_c10
                    }

                    result_set.append(result)

                # Calculate C10-C16
                else:
                    blank_average.area = blank_average.area_c10_c16
                    i_c10 = op.get_fraction_start_index(peak_data, opx.C10_C16_START)
                    i_c16 = op.get_fraction_end_index(peak_data, opx.C10_C16_END)
                    conc_c10_c16 = op.calculate_sample_concentration(
                        peak_data_list=peak_data,
                        blank=blank_average,
                        low_index=i_c10,
                        high_index=i_c16,
                        istd_rt=istd_rt,  # USER INPUT
                        istd_rt_tolerance=istd_rt_tolerance,  # USER INPUT
                        istd_area_target=istd_area_target,  # USER INPUT
                        istd_area_tolerance=istd_area_tolerance,  # USER INPUT
                        calibration_slope=calibration_slope,  # USER INPUT
                        calibration_intercept=calibration_intercept,  # USER INPUT
                        istd_concentration=istd_concentration,  # USER INPUT
                        dilution_factor=dilution_factor)  # USER INPUT

                    # Calculate C16-C34
                    blank_average.area = blank_average.area_c16_c34
                    i_c34 = op.get_fraction_end_index(peak_data, opx.C16_C34_END)
                    conc_c16_c34 = op.calculate_sample_concentration(
                        peak_data_list=peak_data,
                        blank=blank_average,
                        low_index=i_c16,
                        high_index=i_c34,
                        istd_rt=istd_rt,  # USER INPUT
                        istd_rt_tolerance=istd_rt_tolerance,  # USER INPUT
                        istd_area_target=istd_area_target,  # USER INPUT
                        istd_area_tolerance=istd_area_tolerance,  # USER INPUT
                        calibration_slope=calibration_slope,  # USER INPUT
                        calibration_intercept=calibration_intercept,  # USER INPUT
                        istd_concentration=istd_concentration,  # USER INPUT
                        dilution_factor=dilution_factor)  # USER INPUT

                    # Calculate C34-C40
                    blank_average.area = blank_average.area_c34_c40
                    i_c40 = op.get_fraction_end_index(peak_data, opx.C34_C40_END)
                    conc_c34_c40 = op.calculate_sample_concentration(
                        peak_data_list=peak_data,
                        blank=blank_average,
                        low_index=i_c34,
                        high_index=i_c40,
                        istd_rt=istd_rt,  # USER INPUT
                        istd_rt_tolerance=istd_rt_tolerance,  # USER INPUT
                        istd_area_target=istd_area_target,  # USER INPUT
                        istd_area_tolerance=istd_area_tolerance,  # USER INPUT
                        calibration_slope=calibration_slope,  # USER INPUT
                        calibration_intercept=calibration_intercept,  # USER INPUT
                        istd_concentration=istd_concentration,  # USER INPUT
                        dilution_factor=dilution_factor)  # USER INPUT

                    # Calculate C10-C40
                    blank_average.area = blank_average.area_c10_c40
                    conc_c10_c40 = op.calculate_sample_concentration(
                        peak_data_list=peak_data,
                        blank=blank_average,
                        low_index=i_c10,
                        high_index=i_c40,
                        istd_rt=istd_rt,  # USER INPUT
                        istd_rt_tolerance=istd_rt_tolerance,  # USER INPUT
                        istd_area_target=istd_area_target,  # USER INPUT
                        istd_area_tolerance=istd_area_tolerance,  # USER INPUT
                        calibration_slope=calibration_slope,  # USER INPUT
                        calibration_intercept=calibration_intercept,  # USER INPUT
                        istd_concentration=istd_concentration,  # USER INPUT
                        dilution_factor=dilution_factor)  # USER INPUT

                    result = {
                        'sample_name': sample_name,
                        'analysis_time': analysis_time,
                        'conc_c10_c16': conc_c10_c16,
                        'conc_c16_c34': conc_c16_c34,
                        'conc_c34_c40': conc_c34_c40,
                        'conc_c10_c40': conc_c10_c40
                    }

                    result_set.append(result)

            except op.IstdError, e:
                txt = "ISTD error encountered on sample %s: %s" % (sample_name, e)
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Warning)
                msg.setText(txt)
                msg.setWindowTitle("ISTD error encountered!")
                msg.exec_()
                return

        # Write the result set to CSV file
        if self.analysis_c6_c10:
            fieldnames = opx.FIELDNAMES_C6_C10
        else:
            fieldnames = opx.FIELDNAMES_C10_C40
        export_successful = op.write_to_csv(result_set, out_filepath, fieldnames)

        if export_successful:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("Data exported successfully!")
            msg.setWindowTitle("Export successful!")
            msg.exec_()

        # Pretty print results for verification
        pprint(result_set)


def main():
    """Run the org-process app."""
    app = QtGui.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

