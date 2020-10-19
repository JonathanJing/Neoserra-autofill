# Neoserra-autofill

### Required environment:

​	Anaconda: Contains Python and  Jupiter lab 

​		https://www.anaconda.com/products/individual

​	Selenium

​		https://pypi.org/project/selenium/

​	ChromeDriver depends on Chrome version

​		https://chromedriver.chromium.org/downloads

​	Adding chromedriver to PATH 		

​		https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/



### Excel VBA Script for create new tab and copy awardee information 

```vbscript
Sub loopnewtab()

'sheet num
Dim i As Long
'applicant num
Dim ii As Long
Dim wb As Workbook
Dim sht1 As Worksheet
Dim sht2 As Worksheet
Dim sht3 As Worksheet

Set wb = ThisWorkbook
'Change if needed
'contact information (Awardee Applications)
Set sht1 = wb.Sheets(3)
'consulatant information (Director Review)
Set sht2 = wb.Sheets(4)
'awardee tab template, for create new tab (Company A)
Set sht3 = wb.Sheets(5)

'sheet number after Sheet Company A
i = 6

'This is the beginning of the loop
For ii = 2 To 21
    
    'create new tab
    sht3.Copy After:=Sheets(Sheets.Count)
    
    'Copy Contact information to tabs
    'Business Name
    wb.Sheets(i).Range("C2") = sht1.Range("A" & ii).Value
    'Owner Name
    wb.Sheets(i).Range("C3") = sht1.Range("C" & ii).Value
    'Business Address
    wb.Sheets(i).Range("C4") = sht1.Range("F" & ii).Value
    'City
    wb.Sheets(i).Range("C5") = sht1.Range("H" & ii).Value
    'Business Phone Number
    wb.Sheets(i).Range("C6") = sht1.Range("Q" & ii).Value
    'Email Address
    wb.Sheets(i).Range("C7") = sht1.Range("L" & ii).Value
    'Consultant Assigned
    wb.Sheets(i).Range("C9") = sht2.Range("D" & ii + 1).Value
    
    'rename tab
    'remove any symbol in Column, like "+,.&%':-_=
    wb.Sheets(i).Name = sht1.Range("BQ" & ii).Value
    i = i + 1
    
Next ii

End Sub
```



### Google sheet script for send Neoserra ID to each tab

```typescript
function copy_id() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheets()[4];
  var ii = 5;
  for (var i = 3; i < 60; i++) {
    var ts = SpreadsheetApp.getActiveSpreadsheet();
    var target = ts.getSheets()[ii];
    var sourceRange = sheet.getRange(i,5);
    var targetRange = target.getRange("C8");
    targetRange.setValues(sourceRange.getValues());
    sourceRange.copyTo(targetRange);
    ii = ii + 1;
  }
};
```

