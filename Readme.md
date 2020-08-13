# Okinawa COVID-19 Cases PDF parser

## About
The tool will download the latest PDF from [新型コロナウイルス感染症患者・無症状病原体保有者の発生について](https://www.pref.okinawa.lg.jp/site/hoken/chiikihoken/kekkaku/press/20200214_covid19_pr1.html) and convert it to a csv file.

## Important Notice
### ⚠️‼️ This output result cannot be used as a raw data directly ‼️⚠️
Because of the extracted data relies on the PDF format, this parser may miss some data from the PDF document due to incomplete table border.
Please check the raw data before implement to your project.

## Require tool
[pdfplumber](https://github.com/jsvine/pdfplumber)

```
$ pip install request BeautifulSoup4 pdfplumber pandas
```

## How-To

### Execute converter

#### Auto download PDF from Okinawa Prefecture Government
```
$ python3 auto_parser.py
```

#### Parse local PDF file
```
$ python3 parser.py [path/to/file.pdf]
```

## Output File
```
./data/auto_output.csv
./data/manual_output.csv
```

## Project Folder Structure
```
├── archive (old dev code)
├── data
│   ├── auto_output.csv (created hourly from auto_parser.py)
│   └── manual_ouput.csv (created from parser.py)
└── pdf
    ├── 68_1308.pdf
    ├── 67_1243.pdf
    └── [...].pdf
```