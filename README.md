# WyJJD Jupyter
Wyoming Juvenile Justice Data Report: Jupyter Development

**Attention:** This branch (jupyter) focuses on developing data views and cleaning data sources using Jupyter Notebooks.

By using data compiled from various state and federal agencies this project aims to provide valuable insights into the
Juvenile Justice system of the State of Wyoming. This interactive web-based report has been developed to help provide
those who are involved in the Juvenile Justice system with easy to read depictions of standard data points so that they
may make even more informed decisions to assist our youth.

This project contains two main folders, new-data/ which contains all data compiled from various sources for use in the reports found in the code-reports/ folder.

[Click-here](https://github.com/coolcomputers/WyJJD/blob/master/new-data/DataGuide.md) to view a description of all available sources of data. All credit for the data used for this report goes to the companies and organizations listed in the data description.

# View Reports
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CoolComputers/WyJJD/master?filepath=code-report%2FDisplay_CountySnapshot.ipynb) - County Snapshot Interactive Report  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CoolComputers/WyJJD/master?filepath=code-report%2FDisplay_CountySnapshot.ipynbcode-report%2FDisplay_StateStats_Exploratory.ipynb) - State Exploratory Graphs. DISCLAIMER: these are merely experimental graphs to test different data representations.

---

## Installation
In order to run this project on your local system you may need to install some software. If you are unable to install software on your computer, [read how to run this through a web browser](#run-online).  

One goal of this project was to use free and readily available software and services in order to avoid any financial barriers. However, editing the current programs will require a knowledge of the Python programming language.  

The current software suite consists of the following tools:  
- Python3
- Pandas
- Jupyter Notebook
- Various graphing libraries (see requirements.txt)
- Selenium Browser Automation

To install the libraries required for this project run the following command from your [python terminal(opentechschool.github.io)](https://opentechschool.github.io/python-beginners/en/getting_started.html#what-is-python-exactly): `pip install -r requirements.txt`


### Windows Installation
* [Install Python(howtogeek.com)](https://www.howtogeek.com/197947/how-to-install-python-on-windows/)
* [Install Jupyter Notebook](http://jupyter.org/install)

### MacOS Installation
* [How to Use Python on Mac(macworld.com)](https://www.macworld.co.uk/how-to/mac/python-coding-mac-3635912/)
* [Install Jupyter Notebook](http://jupyter.org/install)

---
## Running Online
There are several free services that allow for the execution of Jupyter Notebooks(such as those used in this project) inside of a virtual, online environment. This method requires no software installation on the users computer, however there are often time limits imposed on execution and it is often hard to save changes made during the sessions.

The solution recommended for this project is using mybinder.org. Steps to run this project within mybinder are listed below.

1. Navigate to the [folder containing project notebooks](https://github.com/CoolComputers/WyJJD/tree/master/new-data)
2. Select the URL of the notebook you would like to run
3. Paste that URL into the 'GitHub repository name or URL' field of the main form on [mybinder.org](mybinder.org).
4. Click 'Launch'
5. After a quick loading period you should see the Notebook open up in your web browser and allow you to explore and manipulate the code and data for some amount of time. The changes you make are not saved to the projects public repository so you do not need to worry about breaking anything in the project.
