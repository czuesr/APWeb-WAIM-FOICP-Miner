# FOICP-Miner

## Project Overview

FOICP-Miner is a GUI application built using PyQt5 that aims to perform interactive fuzzy ontology pattern mining and visualization. Users can select fuzzy ontology files and data files, conduct multiple rounds of interactive pattern mining, and ultimately visualize the results.

## Key Features

- Load and select fuzzy ontology files and data files
- Start and stop the interactive pattern mining process
- Visualize the fuzzy ontology tree
- Display and save the mining results

## Predefined Variables

```python
minJaccard = 0.6
OntologyToChar = {
    'A': "Hotel", 'B': "Hostel", 'C': "Airport", 'D': "Railway_Station", 'E': "Car_Parks", 'F': "Park", 
    'G': "Gymnasium", 'H': "Bubble_tea_shop", 'I': "Clothes_Shop", 'J': "Animal_Shop", 
    'K': "National_Scenic_spots", 'L': "Provincial_Scenic_spots", 'M': "Chinese_Restaurant", 
    'N': "Western_Restaurant"
}
listsNum = [
    '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', 
    '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd'
]
```

## Usage

### Running the Application

```python
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
```

### Loading Files

1. Click the "Browse..." button to select fuzzy ontology files and data files.
2. After selecting files, the file paths will be displayed in the corresponding text box.

### Starting the Mining Process

1. Click the "Start" button to initiate the interactive pattern mining process.
2. The mining process includes multiple rounds of interaction, where the user selects preferred patterns to filter the dataset.

### Stopping the Mining Process

- Click the "Stop" button to halt the current mining process.

### Visualizing the Ontology Tree

- Click the "Visualize_Fuzzy_Ontoloy_Tree" button to visualize the fuzzy ontology tree.

### Mining Results

- After the mining process is complete, results will be displayed in the "results" section of the interface, including the number of original frequent patterns and the number and content of selected frequent patterns after interaction.

## Interface Elements

```python
MainWindow.setWindowTitle(_translate("MainWindow", "FOICP-Miner"))
MainWindow.setWindowIcon(QIcon('OIP.jpg'))
self.inOntoButt.setText(_translate("MainWindow", "Browse..."))
self.inDataButt.setText(_translate("MainWindow", "Browse..."))
self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; color:black;\">FuzzyOntology:</span></p></body></html>"))
self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; color:black;\">Dataset:</span></p></body></html>"))
self.pushButton_3.setText(_translate("MainWindow", "Start"))
self.pushButton_4.setText(_translate("MainWindow", "Stop"))
self.pushButton_5.setText(_translate("MainWindow", "Visualize_Fuzzy_Ontoloy_Tree"))
self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">status:</span></p></body></html>"))
self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">results:</span></p></body></html>"))
```

## Technical Support

If you encounter any issues while using the application, please contact the project developer for technical support. Contact: cz021022@163.com

## Version History

- v1.0 (2024-06-01): Basic GUI and interactive pattern mining functionality implemented.

