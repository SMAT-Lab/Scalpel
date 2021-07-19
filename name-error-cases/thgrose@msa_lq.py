#Tim Grose - timothy.h.grose@gmail.com
#instructions for running
#download as a .py.  save as main.py into lq_app folder.
#open command prompt in folder containing lq_app folder and type "bokeh serve lq_app --show"
#import packages
import bokeh, pandas as pd
#import necessary portions of bokeh
from bokeh.plotting import *
from bokeh.models import HoverTool, ColumnDataSource, Axis, Span, NumeralTickFormatter, Label, LabelSet
from bokeh.layouts import row, widgetbox, column
from bokeh.models.widgets import Select, Div
from bokeh.io import curdoc, show
from bokeh.palettes import Inferno256
from os.path import dirname, join
#read processed lq data file
#for main.py
lqdf=pd.read_csv(join(dirname(__file__),'data','Trimmed_MSA_LQs_2017-08-06.csv'))
#read processed lq data file
#for ipynb
#lqdf=pd.read_csv("data/Trimmed_MSA_LQs_2017-08-06.csv")
lqdf_agg=lqdf[(lqdf['agglvl_title']=='Supersector')&(lqdf['area_title']=='New York-Newark-Jersey City, NY-NJ-PA MSA')]
x=lqdf_agg['msa_lq']
y=lqdf_agg['annual_avg_emplvl']
desc=lqdf_agg['industry_title']
#set source data
#may need to add columns used in Select
source=ColumnDataSource(data=dict(
    x=x,
    y=y,
    desc=desc,
))
#set up contents  of hover tool with source data
hover = HoverTool(
    tooltips="""    
    <div style="background:white;">
            <div>
                <span style="font-size: 12px; color: blue;">Industry:</span>
                <span style="font-size: 12px; color: black;">@desc</span>
            </div>
            <div>
                <span style="font-size: 12px; color: blue;">MSA Location Quotient</span>
                <span style="font-size: 12px; color: black;">@x</span>
                
            </div>
            <div>
                <span style="font-size: 12px; color: blue;">Employment:</span>
                <span style="font-size: 12px; color: black;">@y</span>
            </div>
        </div>
        """
)
#set up figure with titles and hover
p1=Figure(x_axis_label='MSA Employment Location Quotient versus all MSAs',
          y_axis_label='MSA Employment',
          tools=[hover],
          logo=None,
          plot_width=600, 
          plot_height=600,
          )
p1.yaxis[0].formatter=NumeralTickFormatter(format="0,0")
p1.xaxis[0].formatter=NumeralTickFormatter(format="0,0.00")
#circle plot on p1 figure
p1.circle('x','y',size=9,fill_color='#ff9000',line_color='firebrick',alpha=.9,source=source)
vline=Span(location=1,dimension='height',line_color='yellow',line_width=1)
p1.renderers.extend([vline])
#get unique agg levels
agglvl=lqdf['agglvl_title'].unique()
#set up select agg level widget
agglvl_select=Select(
    title="Industry Aggregation Level:",
    value=agglvl[0],
    options=agglvl.tolist()
)
#get unique MSAs
geo=lqdf['area_title'].unique()
#set up select geo widget
geo_select=Select(
    title="Geography:",
    value='New York-Newark-Jersey City, NY-NJ-PA MSA',
    options=geo.tolist()
)
def update(attrname,old,new):
    lqdf_agg=lqdf[(lqdf['agglvl_title']==agglvl_select.value)&(lqdf['area_title']==geo_select.value)]
    source.data=dict(
        x=lqdf_agg['msa_lq'],
        y=lqdf_agg['annual_avg_emplvl'],
        desc=lqdf_agg['industry_title'],
        )
for menu in [agglvl_select,geo_select]:
    menu.on_change('value', update)
#put controls in widget box
controls = widgetbox([agglvl_select,geo_select],width=420)
#add explanatory text
desc=Div(text="""
    <h1>
    How is Your City's Economy Unique?
    </h1>
    <p>
    Location Quotients (LQs) compare the proportion of a particular region's employment in a particular industry
    to the proportion of a larger reference area's employment in that same industry. An LQ of greater than 1 indicates
    that an industry has a higher concentration of employment in that region than in the overall reference area.  An LQ of
    less than 1 indicates that an industry has a lower concentration of employment in that region than in the overall
    reference area.
    <br>
    <br>
    This chart shows 2016 LQs for each Metropolitan Statistical Area (MSA) in the U.S. with a reference area of
    all MSAs in the U.S.  It conveys how concentrations in employment vary from city to city.  These LQs are recalcualted
    from overall LQs provided by the Bureau of Labor Statistics (BLS) Quarterly Census of Employment and Wages. 
    <br>
    <br>
    Use the filters below to view LQs for different MSAs and different industry aggregation levels, ranging from
    supersector (larger groupings) down to NAICS 4-digit sector (smaller groupings). (NAICS: North American Industry 
    Classification System)
    </p>
    """,width=400)
cit=Div(text="""
    <br>
    <i>
    <font-size:9px;font-style:italic>
    These MSA LQs are recalculated from overall LQs provided by the Bureau of Labor Statistics (BLS) 
    Quarterly Census of Employment and Wages. Government LQs are incorporated into the displayed industry 
    aggregation levels too; these do not appear directly in the BLS data. 
    <br>
    <br>
    U.S. Bureau of Labor Statistics, 'Quarterly Census of Employment and Wages,' 
    26 June 2017. www.bls.gov/cew/datatoc.htm.
    </i>
    """,width=1000)
#make layout with controls and figure p1
layout = column(row(column(desc,controls),p1),cit)
#for inline viewing
show(layout)
curdoc().add_root(layout)
curdoc().title="LQ"