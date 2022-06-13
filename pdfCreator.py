import mysql.connector
from datetime import date

from fpdf_mc import PDF_MC_Table
from fpdf import FPDF




import json

def createpdf(data,c,t):
    try:
        pdf = PDF_MC_Table()
        pdf.add_page()
        pdf.set_font('Arial','',12)
        pdf.SetWidths([7,30,20,35,30,20,15,20,20])
        pdf.SetLineHeight(5)
        # add table heading using standerd cells
        page_width = pdf.setpagewidth()
        c= c.upper()
        pdf.cell(page_width, 5, '{0} - Bill Entry Status {1}'.format(c,t),0,0,'C')
        pdf.ln(12)
        pdf.set_font('Arial','B',6.5)
        pdf.cell(7,5,'S.No',1,0)
        pdf.cell(30,5,'Corporation',1,0)
        pdf.cell(20,5,'Type',1,0)
        pdf.cell(35,5,'Vendor_Name',1,0)
        pdf.cell(30,5,'Bill_Date',1,0)
        pdf.cell(20,5,'Invoice_number',1,0)
        pdf.cell(15,5,'Amount',1,0)
        pdf.cell(20,5,'Created Date',1,0)
        pdf.cell(20,5,'Created_by',1,0)
        pdf.ln()
        pdf.set_font('Arial','',5)
        count = 0
        for r in data:
            count= (count+1)
            r['id'] =str( count)
            pdf.Row([
                    r['id'],
                    r['Corporation'],
                    r['Type'],
                    r['Vendor_Name'],
                    r['Bill/Debit_memo_Date'],
                    r['Invoice_number'],
                    r['Amount'],
                    r['Created Date'],
                    r['Created_by'],
                    ])
        pdf.set_font('Times','',10.0) 
        pdf.cell(page_width, 5, '- end of report -',0,0,'C')
        pdf.output('{0}_daily_report_{1}.pdf'.format(c,t))
        
        
    except Exception as e:
        print('ex',e)
    
try:
    
    mydb= mysql.connector.connect(

        host="localhost",

        user="root",

        # password="Nimble@123",

        database="mysql"

    )

    mycursor= mydb.cursor()
    today = date.today()
    Y = today.strftime("%Y")
    M = today.strftime("%m")
    D = today.strftime("%d")
    
    #  select_query = mycursor.execute(
#     f"select * from verified_bills where timestamp '{today} 00:00:00' AND '{today} 23:59:00'"
#     #  ("%{}%".format(today),)
# )



    select_query = mycursor.execute(
    "select * from verified_bills where timestamp like %s",
     ("%{}%".format(today),)
)
    myresult = mycursor.fetchall()
    today = M+"-"+D+"-"+Y
    print(today)
    json_obj = []
    client = {*()}
    for row in myresult:
        print(row[12])
        if(row[17]==0) : type='Bill Entry'
        elif(row[17]==1) : type='Check'
        elif(row[17]==2) : type='Credit card'
        elif(row[17]==3) : type='Bill Pay'

        if(row[18]==7) : userid='Manikanta'
        else:userid='user'

        json_obj.append({"Corporation": row[4],'client':row[3],'Invoice_number':row[6],'Type':type,'Vendor_Name':row[5],'Bill/Debit_memo_Date': row[7],'Amount': row[8],'Created Date':str(row[12]).split(" ")[0],'Created_by': str(userid) ,"status":"success"})
        client.add(row[3])
    
    for c in client:
        print(c)
        data=[]
        for r in json_obj:
            if c == r['client']:
                data.append(r)
        
        createpdf(data,c,today)
        


    
    print('end')
except Exception as e:
    print('ex',e)
finally:
        mycursor.close() 
        mydb.close()

