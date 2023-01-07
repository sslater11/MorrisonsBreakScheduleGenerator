# Copyright (C) 2020  Simon Slater
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from constants import *

class HTMLLine:
    # Takes a string containing HTML e.g. "<p>hello</p>"
    def __init__( self, line ):
        if isinstance(line, str):
            self.line = line
        else:
            raise TypeError("Must pass a string.")

    def getHTML( self ):
        return self.line

class MyHTML:
    def __init__( self ):
        self.html_tables = []
#        self.html_start = """<!DOCTYPE html>
#<html lang="en">
#    <head>
#        <meta charset="utf-8">
#        <title>Break Schedule</title>
#
#        <style type="text/css">
#            <!--
#
#page[size="A4"] {
#  background: white;
#  width: 21cm;
#  height: 29.7cm;
#  display: block;
#  margin: 0 auto;
#  margin-bottom: 0.5cm;
#  box-shadow: 0 0 0.5cm rgba(0,0,0,0.5);
#}
#            @media screen, print {
#  body, page[size="A4"] {
#    margin: 0;
#    box-shadow: 0;
#                font-size: """ + FONT_SIZE + """px;
#                font-family: Arial, sans-serif;
#                color: black;
#  }
#            .adamsNumbersTable { font-size:""" + FONT_SIZE_ADAMS_NUMBERS + """px; }
#            .adamsNumbersTable th { padding:3px 3px; }
#            .adamsNumbersTable td { padding:1px 3px; }
#
#            .actionListTable { font-size:""" + FONT_SIZE_ACTION_LIST + """px; }
#            .actionListTable th { padding:3px 3px; }
#            .actionListTable td { padding:3px 3px; }
#
#            .mainLayout td { padding:3px 3px; }
#
#            table      { background-color:white; color:black; border-collapse:collapse; }
#            .myTable td { padding:5px 10px; background-color:white; color:black; }
#            .myTable th { padding:5px 10px; background-color:#ccc;  color:black; color-adjust:exact; }
#            .myTable  { border:1px solid #000; color-adjust:exact;}
#
#            .mainLayout td { padding:5px; text-align: center; vertical-align: top; }
#            .mainLayout table { border:0px }
#            table, td, th { padding:5px 10px; border:1px solid #000; color-adjust:exact;}
#            }
#        -->
#        </style>
#    </head>
#    <body>
#"""

        papercss = """
    /* copied directly from css from paper-css at "https://cdnjs.cloudflare.com/ajax/libs/paper-css/0.4.1/paper.css" */
    /* Paper-css Start */
    /* The ISC Licence applys to just this paper-css section */
/*
ISC Licence

Copyright (c) 2017–2018, Rhyne Vlaservich rhyneav@gmail.com

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
*/
    /* Load paper.css for happy printing */
@page { margin: 0 }
body { margin: 0 }
.sheet {
  margin: 0;
  overflow: hidden;
  position: relative;
  box-sizing: border-box;
  page-break-after: always;
}

/** Paper sizes **/
body.A3               .sheet { width: 297mm; height: 419mm }
body.A3.landscape     .sheet { width: 420mm; height: 296mm }
body.A4               .sheet { width: 210mm; height: 296mm }
body.A4.landscape     .sheet { width: 297mm; height: 209mm }
body.A5               .sheet { width: 148mm; height: 209mm }
body.A5.landscape     .sheet { width: 210mm; height: 147mm }
body.letter           .sheet { width: 216mm; height: 279mm }
body.letter.landscape .sheet { width: 280mm; height: 215mm }
body.legal            .sheet { width: 216mm; height: 356mm }
body.legal.landscape  .sheet { width: 357mm; height: 215mm }

/** Padding area **/
.sheet.padding-10mm { padding: 10mm }
.sheet.padding-15mm { padding: 15mm }
.sheet.padding-20mm { padding: 20mm }
.sheet.padding-25mm { padding: 25mm }

/** For screen preview **/
@media screen {
  body { background: #e0e0e0 }
  .sheet {
    background: white;
    box-shadow: 0 .5mm 2mm rgba(0,0,0,.3);
    margin: 5mm auto;
  }
}

/** Fix for Chrome issue #273306 **/
@media print {
           body.A3.landscape { width: 420mm }
  body.A3, body.A4.landscape { width: 297mm }
  body.A4, body.A5.landscape { width: 210mm }
  body.A5                    { width: 148mm }
  body.letter, body.legal    { width: 216mm }
  body.letter.landscape      { width: 280mm }
  body.legal.landscape       { width: 357mm }
}
    /* Set page size here: A5, A4 or A3 */
    /* Set also "landscape" if you need */
    /* Paper-css End*/
"""

        normalizecss = """
/*! normalize.css v7.0.0 | MIT License | github.com/necolas/normalize.css */html{line-height:1.15;-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%}body{margin:0}article,aside,footer,header,nav,section{display:block}h1{font-size:2em;margin:.67em 0}figcaption,figure,main{display:block}figure{margin:1em 40px}hr{box-sizing:content-box;height:0;overflow:visible}pre{font-family:monospace,monospace;font-size:1em}a{background-color:transparent;-webkit-text-decoration-skip:objects}abbr[title]{border-bottom:none;text-decoration:underline;text-decoration:underline dotted}b,strong{font-weight:inherit}b,strong{font-weight:bolder}code,kbd,samp{font-family:monospace,monospace;font-size:1em}dfn{font-style:italic}mark{background-color:#ff0;color:#000}small{font-size:80%}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sub{bottom:-.25em}sup{top:-.5em}audio,video{display:inline-block}audio:not([controls]){display:none;height:0}img{border-style:none}svg:not(:root){overflow:hidden}button,input,optgroup,select,textarea{font-family:sans-serif;font-size:100%;line-height:1.15;margin:0}button,input{overflow:visible}button,select{text-transform:none}[type=reset],[type=submit],button,html [type=button]{-webkit-appearance:button}[type=button]::-moz-focus-inner,[type=reset]::-moz-focus-inner,[type=submit]::-moz-focus-inner,button::-moz-focus-inner{border-style:none;padding:0}[type=button]:-moz-focusring,[type=reset]:-moz-focusring,[type=submit]:-moz-focusring,button:-moz-focusring{outline:1px dotted ButtonText}fieldset{padding:.35em .75em .625em}legend{box-sizing:border-box;color:inherit;display:table;max-width:100%;padding:0;white-space:normal}progress{display:inline-block;vertical-align:baseline}textarea{overflow:auto}[type=checkbox],[type=radio]{box-sizing:border-box;padding:0}[type=number]::-webkit-inner-spin-button,[type=number]::-webkit-outer-spin-button{height:auto}[type=search]{-webkit-appearance:textfield;outline-offset:-2px}[type=search]::-webkit-search-cancel-button,[type=search]::-webkit-search-decoration{-webkit-appearance:none}::-webkit-file-upload-button{-webkit-appearance:button;font:inherit}details,menu{display:block}summary{display:list-item}canvas{display:inline-block}template{display:none}[hidden]{display:none}/*# sourceMappingURL=normalize.min.css.map */
"""

        self.html_start = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>Break Schedule</title>
    <!-- Normalize or reset CSS with your favorite library -->
<!--
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css">
-->

    <!-- Load paper.css for happy printing -->
<!--
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/paper-css/0.4.1/paper.css">
-->
    <!-- Set page size here: A5, A4 or A3 -->
    <!-- Set also "landscape" if you need -->
    <style>""" + normalizecss + papercss + """

@media print {
   .sheet {
         /* firefox, safari extra page fix */
                              }
                              }

        @page { size: A4 ; }
        @media screen, print {
            body{ font-size: """ + FONT_SIZE + """px; font-family: Arial, sans-serif;}
            .tableGap{ font-size:1px; padding: 3px 3px; }
            table { background-color:white; color:black; border-collapse:collapse; }
            table th{ background-color:#ccc;  color:black; color-adjust:exact; }
            .mainLayout td { vertical-align: top; border:1px solid #fff; }
            .mainLayout { vertical-align: top; }
            table, td, th { padding:2px 5px; border:1px solid #000; color-adjust:exact; -webkit-print-color-adjust:exact;}
            .adamsNumbersTable { font-size:""" + FONT_SIZE_ADAMS_NUMBERS + """px; margin-left: auto; margin-right: auto;}
            .actionListTable { font-size:""" + FONT_SIZE_ACTION_LIST + """px; margin-left: auto; margin-right: auto;}
            .actionListTable td {padding: 1px 3px;}
            .myTable  { font-size:""" + FONT_SIZE + """px; border:1px solid #000; margin-left: auto; margin-right: auto; }
            .myTableSmall  { font-size:""" + FONT_SIZE_SMALL + """px; margin-left: auto; margin-right: auto; }
            .actionListHighlightRow { background-color:#ccc;  color:black; color-adjust:exact; -webkit-print-color-adjust:exact;}
            .actionListHighlightRow td{ background-color:#ccc;  color:black; color-adjust:exact; -webkit-print-color-adjust:exact;}
            .myTable td { border:1px solid #000; }
            .myTableSmall td { border:1px solid #000; }
            .actionListTable td { border:1px solid #000; }
            .adamsNumbersTable  { color:#444; color-adjust:exact; -webkit-print-color-adjust:exact; }
            .adamsNumbersTable td { border:1px solid #000; }
            .adamsNumbersHourHighlight { background-color:#ccc; color:black; font-weight:bold; color-adjust:exact; -webkit-print-color-adjust:exact;}
            .departmentCell {font-size: """ + FONT_SIZE_DEPARTMENT + """px; }

            /* Highlight the background of every even numbered table cell */
            table.myTable tr:nth-child(2n+2){
                background:#e8e8e8;
            }
            table.myTableSmall tr:nth-child(2n+2){
                background:#e8e8e8;
            }
        }
    </style>
</head>

<!-- Set "A5", "A4" or "A3" for class name -->
<!-- Set also "landscape" if you need -->
<body class="A4 ">
"""
        self.html_end = """</body>
</html>
"""

    def addHTMLTable( self, table, font_size=None ):
        self.html_tables.append( table )

    def addDate( self, the_date ):
        # Print out "Monday 31 / Aug / 2020"
        str_the_date = the_date.strftime( "%A %d / %b / %Y" )
        str_html = """ <p style=\"font-size: """ + FONT_SIZE_TODAYS_DATE + """px\">""" + str_the_date + """</p> """

        date_as_html = HTMLLine( str_html )
        self.html_tables.append( date_as_html )

    def addHTML(self, html):
        if isinstance(html, str):
            # All variables are strings,
            # so add them to the table.
            self.html_tables.append( HTMLLine(html) )
        else:
            print( type(html) )
            raise TypeError("Must pass a string.")

    def addPageBreak( self ):
        self.html_tables.append( PageBreak() )

    def getHTML( self ):
        all_tables = ""
        for i in self.html_tables:
            all_tables = all_tables + i.getHTML()

        return self.html_start + all_tables + self.html_end
