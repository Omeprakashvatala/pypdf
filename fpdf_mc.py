#call main fpdf library
from fpdf import FPDF

#create new class extending fpdf class
class PDF_MC_Table(FPDF):
    def __init__(self):
        # variable to store widths and aligns of cells, and line height
        self.widths = None
        self.aligns = []
        self.lineHeight = None
        self.pdf = FPDF('P', 'mm', 'A4')
    def add_page(self):
        return self.pdf.add_page()
    def output(self,x):
        return self.pdf.output(x)
    def set_font(self, n,t,s):
        return self.pdf.set_font(n,t,s)
    def cell(self,wt,ht,t,b,x,a=None):
        if(a==None): return self.pdf.cell(wt,ht,t,b,x)
        else: return self.pdf.cell(wt,ht,t,b,x,a)
        
    def ln(self,x=None):
        if(x==None):return self.pdf.ln()
        else: return self.pdf.ln(x)
    def setpagewidth(self):
        return self.pdf.w - 4 * self.pdf.l_margin
        
    
    # Set the array of column widths
    def SetWidths(self,w):
        self.widths = w

    #Set the array of column alignments
    def SetAligns(self,a):
        self.aligns = a

    # Set line height
    def SetLineHeight(self,h):
        self.lineHeight =  h
    
    # Calculate the height of the row
    def Row(self, data):
        # number of line
        nb = 0

        # loop each data to find out greatest line number in a row.
        for i in range(0,len(data)):
            # NbLines will calculate how many lines needed to display text wrapped in specified width.
            #  then max function will compare the result with current $nb. Returning the greatest one. And reassign the $nb.
            nb=max(nb,self.NbLines(self.widths[i],data[i]))
        # multiply number of line with line height. This will be the height of current row

        h = self.lineHeight*nb

        # Issue a page break first if needed
        self.CheckPageBreak(h)

        # print(len(data),data)
        # Draw the cells of current row
        for i in range(len(data)):
            #  width of the current col
            # print(self.widths,i,self.widths)
            w = self.widths[i]
            # alignment of the current col. if unset, make it left.
            if(len(self.aligns)>0): a = self.aligns[i]
            else: a ='L'
            # Save the current position
            self.x = self.pdf.get_x()
            self.y = self.pdf.get_y()
            # Draw the border
            self.pdf.rect(self.x,self.y,w,h)
            # Print the text
            self.pdf.multi_cell(w,5,data[i],0,a)
            # Put the position to the right of the cell
            self.pdf.set_xy(self.x+w,self.y)
        # Go to the next line
        self.pdf.ln(h)
    def CheckPageBreak(self,h):
        # If the height h would cause an overflow, add a new page immediately
        if(self.pdf.get_y()+h>self.pdf.page_break_trigger): self.pdf.add_page(self.pdf.cur_orientation)
    def NbLines(self,w,txt):
        #calculate the number of lines a Multicell  of width w will take
       
        cw = self.pdf.current_font['cw']
        if(w==0):
            w = w-self.pdf.r_margin-self.x
        wmax = (w-2*self.pdf.c_margin)*1000/self.pdf.font_size
        s = txt.replace('\r','')
        nb = len(s)
        if(nb>0 and s[nb-1]=='\n'):
            nb=nb-1
        sep = -1
        i =0
        j=0
        l=0
        nl=1
        while(i<nb):
            c=s[i]
            if(c=='\n'):
                i=i+1
                sep=-1
                j=i
                l=0
                nl=nl+1
                continue
            if(c==' '):sep=i
            # print(cw,c)
            l+=cw[c]
            if(l>wmax):
                if(sep==-1):
                    if(i==j): i=i+1
                else:
                    i=sep+1
                sep=-1
                j=i
                l=0
                nl=nl+1
            else: i = i+1
        return nl

                       





