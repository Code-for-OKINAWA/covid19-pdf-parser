# Okinawa COVID-19 Cases PDF parser

## Require tool
[pdfplumber](https://github.com/jsvine/pdfplumber)

```
pip install pdfplubmer
```

## How-To

### Download PDF from Okinawa Prefecture official report
[新型コロナウイルス感染症患者・無症状病原体保有者の発生について](https://www.pref.okinawa.lg.jp/site/hoken/chiikihoken/kekkaku/press/20200214_covid19_pr1.html)

```
$ curl -OL [PDF Url]
```

### Execute converter
```
$ python3 convert_table.py path/to/file
```

### Output File

```
./output.csv
```
