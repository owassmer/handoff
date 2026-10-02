#!/usr/bin/env python3
"""Build the three reader-facing PDF reports from their editable Markdown."""
from pathlib import Path
import re, html, math
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT.parent if (ROOT.parent/'01_playbook').is_dir() else ROOT/'deliverables'
FONT=Path('/usr/share/fonts/truetype/dejavu')
for name,fn in [('DejaVu','DejaVuSans.ttf'),('DejaVu-Bold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT/fn)))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu',boldItalic='DejaVu-Bold')
NAVY=colors.HexColor('#132C3C');TEAL=colors.HexColor('#087D84');INK=colors.HexColor('#26343D');MUTED=colors.HexColor('#60717C');PALE=colors.HexColor('#EFF5F6')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Text',fontName='DejaVu',fontSize=9.2,leading=14.4,textColor=INK,spaceAfter=8))
styles.add(ParagraphStyle(name='TitleX',fontName='DejaVu-Bold',fontSize=26,leading=31,textColor=NAVY,spaceAfter=15))
styles.add(ParagraphStyle(name='H2X',fontName='DejaVu-Bold',fontSize=15,leading=20,textColor=NAVY,spaceBefore=17,spaceAfter=9,keepWithNext=True))
styles.add(ParagraphStyle(name='H3X',fontName='DejaVu-Bold',fontSize=11.2,leading=16,textColor=TEAL,spaceBefore=12,spaceAfter=6,keepWithNext=True))
styles.add(ParagraphStyle(name='Cell',fontName='DejaVu',fontSize=8,leading=11.5,textColor=INK,spaceAfter=1,splitLongWords=True))
styles.add(ParagraphStyle(name='CellHead',parent=styles['Cell'],fontName='DejaVu-Bold',textColor=colors.white))
styles.add(ParagraphStyle(name='QuoteX',parent=styles['Text'],fontSize=11,leading=17,leftIndent=14,rightIndent=12,textColor=NAVY,spaceBefore=6,spaceAfter=12))
styles.add(ParagraphStyle(name='SmallX',parent=styles['Text'],fontSize=7.7,leading=11,textColor=MUTED))

def clean(s):
    return s.translate(str.maketrans({'\u2011':'-','\u2013':'-','\u2014':' - ','\u2212':'-','\u00a0':' '}))

def inline(s):
    s=html.escape(clean(s.strip()))
    s=re.sub(r'\[([^\]]+)\]\((https?://[^\s]+?)\)',lambda m:f'<a href="{m[2]}" color="#087D84">{m[1]}</a>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="DejaVu">\1</font>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    return s

class RelationshipMap(Flowable):
    """An exact relationship diagram; no generated imagery or inferred data."""
    def __init__(self):
        super().__init__()
        self.width=499
        self.height=267
    def draw(self):
        c=self.canv
        c.setFillColor(PALE);c.roundRect(0,0,self.width,self.height,7,fill=1,stroke=0)
        c.setFillColor(NAVY);c.setFont('DejaVu-Bold',10)
        c.drawString(12,248,'The manager joins rights, physical work and money')
        def box(x,y,w,h,title,lines):
            c.setFillColor(colors.white);c.setStrokeColor(colors.HexColor('#C8D8DC'));c.roundRect(x,y,w,h,4,fill=1,stroke=1)
            c.setFillColor(NAVY);c.setFont('DejaVu-Bold',8.7);c.drawString(x+8,y+h-15,title)
            c.setFont('DejaVu',7.8);c.setFillColor(INK)
            for i,line in enumerate(lines):c.drawString(x+8,y+h-29-i*11,line)
        def arrow(x1,y1,x2,y2):
            c.setStrokeColor(TEAL);c.setFillColor(TEAL);c.setLineWidth(.9);c.line(x1,y1,x2,y2)
            a=math.atan2(y2-y1,x2-x1);p=c.beginPath();p.moveTo(x2,y2);p.lineTo(x2-5*math.cos(a-.5),y2-5*math.sin(a-.5));p.lineTo(x2-5*math.cos(a+.5),y2-5*math.sin(a+.5));p.close();c.drawPath(p,fill=1,stroke=0)
        box(12,173,149,58,'Owner / board / lender',['Mandate, money, constraints','Reserved decisions'])
        box(175,173,149,58,'Manager / operating team',['Choices, priorities, promises','Authority and follow-through'])
        box(338,173,149,58,'Occupants / prospects',['Rights, requests, payments','Access and commitments'])
        box(12,72,149,70,'Trades / staff / suppliers',['Diagnosis, parts, physical work','Attendance and quality','Capacity and warranties'])
        box(175,72,149,70,'Property / space / asset',['Condition and actual use','Readiness and legal possession','Shared-system dependencies'])
        box(338,72,149,70,'Accounting / bank / insurer',['Charges, invoices, claims','Restricted and available funds','Settlement and reconciliation'])
        arrow(161,211,175,211);arrow(175,189,161,189)
        arrow(324,211,338,211);arrow(338,189,324,189)
        arrow(210,173,96,143);arrow(249,173,249,143);arrow(290,173,412,143)
        arrow(161,111,175,111);arrow(324,111,338,111)
        c.setFont('DejaVu',7.5);c.setFillColor(MUTED)
        c.drawString(13,49,'Laws, contracts, regulators and courts define or change rights across this map.')
        c.drawString(13,34,'Reports return to the manager; confirmed outcomes update the next decision.')
        c.drawString(13,19,'A completed task is not sufficient proof that every connected obligation is complete.')

def table(rows,width=499):
    n=len(rows[0])
    proportions={2:[.32,.68],3:[.23,.38,.39],4:[.2,.27,.27,.26],5:[.25,.18,.18,.2,.19]}.get(n,[1/n]*n)
    if any('Share of' in x for x in rows[0]) and n==3:proportions=[.44,.28,.28]
    data=[[Paragraph(inline(v),styles['CellHead'] if i==0 else styles['Cell']) for v in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=[width*p for p in proportions],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,TEAL),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#D7E2E5'))]))
    return t

def parse(md,diagram=False):
    lines=md.splitlines();story=[];i=0;heading_count=0
    while i<len(lines):
        l=lines[i].strip()
        if not l:i+=1;continue
        if l.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',x.replace(' ','')) for x in row):rows.append(row)
                i+=1
            if rows:story.extend([table(rows),Spacer(1,10)])
            continue
        if l.startswith('# '):
            story.append(Paragraph(inline(l[2:]),styles['TitleX']));story.append(Spacer(1,4));i+=1;continue
        if l.startswith('## '):
            heading_count+=1
            if diagram and heading_count==2:story.extend([Spacer(1,8),RelationshipMap(),Spacer(1,8)])
            story.append(Paragraph(inline(l[3:]),styles['H2X']));i+=1;continue
        if l.startswith('### '):story.append(Paragraph(inline(l[4:]),styles['H3X']));i+=1;continue
        if l.startswith('> '):story.append(Paragraph(inline(l[2:]),styles['QuoteX']));i+=1;continue
        if l.startswith('- ') or re.match(r'^\d+\. ',l):
            content=l[2:] if l.startswith('- ') else l
            prefix='• ' if l.startswith('- ') else ''
            story.append(Paragraph(prefix+inline(content),styles['Text']));i+=1;continue
        if l=='---':story.append(Spacer(1,10));i+=1;continue
        para=[l];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||>|- |\d+\. )',lines[i].strip()):para.append(lines[i].strip());i+=1
        story.append(Paragraph(inline(' '.join(para)),styles['Text']))
    return story

class NumberCanvas(canvas.Canvas):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.states=[]
    def showPage(self):self.states.append(dict(self.__dict__));self._startPage()
    def save(self):
        n=len(self.states)
        for s in self.states:self.__dict__.update(s);self.setFont('DejaVu',7.5);self.setFillColor(MUTED);self.drawRightString(554,30,f'{self._pageNumber} / {n}');super().showPage()
        super().save()

def build(path,text,label,diagram=False,appendix=None):
    doc=SimpleDocTemplate(str(path),pagesize=(612,792),rightMargin=56,leftMargin=56,topMargin=58,bottomMargin=51,title=label,author='Owen Wassmer | Research and analysis',subject='Property management operating model and company playbook')
    def page(c,d):
        c.setStrokeColor(colors.HexColor('#D2DFE4'));c.setLineWidth(.6);c.line(56,751,556,751)
        c.setFillColor(MUTED);c.setFont('DejaVu',7.4);c.drawString(56,762,'PROPERTY MANAGEMENT');c.drawRightString(556,762,label.upper())
        c.drawString(56,30,'Research cutoff: 15 September 2026')
    story=parse(text,diagram)
    if appendix:story.extend([PageBreak()]+parse(appendix))
    doc.build(story,onFirstPage=page,onLaterPages=page,canvasmaker=NumberCanvas)
    print(path)

if __name__=='__main__':
    build(OUT/'01_playbook/Property_Management_Playbook.pdf',(OUT/'01_playbook/Property_Management_Playbook.md').read_text(),'Action playbook',True)
    build(OUT/'01_playbook/Field_Guide.pdf',(OUT/'01_playbook/Field_Guide.md').read_text(),'Field guide')
    build(OUT/'02_research/Research_and_Operating_Model.pdf',(OUT/'02_research/Research_Synthesis.md').read_text(),'Research and operating model',False,(ROOT/'research/operating_model.md').read_text())
