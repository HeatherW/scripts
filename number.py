'''Attempting to make an automatic numbering script
This script does the following:
1. Updates the anchor tags to have the correct figure or table reference. This is only needed for science at present.
2. Updates the figure and table caption tags to have a prefix of table x: or figure x:. Again only for science.
3. Updates chapter titles, section titles and subsection titles. Chapter titles need chapter x: as  a prefix, section titles need no title shortcode and subsection titles just need the shortcode at the end.
4. Numbers the worked examples.
5. Numbers the exercises
'''

# Import the necessary items
import os

from lxml import etree

# Make the figure reference dictionary (for grade 12 science at present)
fig_ref_dict = {"#fig:scienceskills:science":"1.1",
"#fig:scimeth:scientificmethod":"1.2",
"#fig:scienceskills:ruler":"1.3",
"#fig:scienceskills:thermometerread":"1.4",
"#fig:scienceskills:thermometer":"1.5",
"#fig:scienceskills:scale":"1.6",
"#fig:scienceskills:meniscus":"1.7",
"#fig:scienceskills:measuringcyl":"1.8",
"#fig:scienceskills:volpipette":"1.9",
"#fig:scienceskills:graduatedpipette":"1.10",
"#fig:scienceskills:straightline":"1.11",
"#fig:scienceskills:exponential":"1.12",
"#fig_mom1":"2.1",
"#fig_mom2":"2.2",
"#fig:pc:types:elast:before":"2.3",
"#fig:pc:types:elast:after":"2.4",
"#fig:p:m2d12:inelastic:example":"2.5",
"#fig:p:m:m2d12:projectile":"3.1",
"#fig:p:m:m2d12:maxheighttime":"3.2",
"#fig:slopeandarea":"3.3",
"#fig:relation":"3.4",
"#fig:motion:graphs":"3.5",
"#fig:motion:graphs2":"3.6",
"#fig:motion:graphs2":"3.7",
"#fig:motion:graphs2":"3.8",
"#fig:organic:molecules":"4.1",
"#fig:organic:carbon":"4.2",
"#fig:organic:unbranched":"4.3",
"#fig:organic:branched":"4.4",
"#fig:organic:structuralformula":"4.5",
"#fig:organic:carbonrep":"4.6",
"#fig:organic:semistructural":"4.7",
"#fig:organic:condensed":"4.8",
"#fig:organic:methanerep":"4.9",
"#fig:organic:ethanerep":"4.10",
"#fig:organic:butanerep":"4.11",
"#fig:organic:saturated":"4.12",
"#fig:organic:unsaturated":"4.13",
"#fig:organic:classhydro":"4.14",
"#fig:organic:methane":"4.15",
"#fig:organic:ethane":"4.16",
"#fig:organic:propane":"4.17",
"#fig:organic:methaneandpropane":"4.18",
"#fig:organic:petrolstation":"4.19",
"#fig:organic:ethene3rep":"4.20",
"#fig:organic:propene3rep":"4.21",
"#fig:organic:pentene":"4.22",
"#fig:organic:etheneplants":"4.23",
"#fig:organic:lampofpolyprop":"4.24",
"#fig:organic:ethyne":"4.25",
"#fig:organic:branchedchain":"4.26",
"#fig:organic:meth":"4.27",
"#fig:organic:eth":"4.28",
"#fig:organic:alcoholimage":"4.29",
"#fig:organic:halomethane":"4.30",
"#fig:organic:halopropane":"4.31",
"#fig:organic:substituent":"4.32",
"#fig:organic:chloroform":"4.33",
"#fig:organic:carbonyl":"4.34",
"#fig:organic:aldket":"4.35",
"#fig:organic:butanal":"4.36",
"#fig:organic:butanone":"4.37",
"#fig:organic:methanoicacid":"4.38",
"#fig:organic:ethanoicacid":"4.39",
"#fig:organic:wine":"4.40",
"#fig:organic:dichromate":"4.41",
"#fig:organic:ester":"4.42",
"#fig:organic:methylmethanoateester":"4.43",
"#fig:organic:butane2":"4.44",
"#fig:organic:pentanol":"4.45",
"#fig:organic:esterisomers":"4.46",
"#fig:organic:isomers":"4.47",
"#fig:organic:acidesterisomer":"4.48",
"#fig:organic:ethylbutanoateester":"4.49",
"#fig:organic:ethylbutanoate":"4.50",
"#fig:organic:ethylbutanoate2":"4.51",
"#fig:organic:phasesofwater":"4.52",
"#fig:organic:hbondalcohol":"4.53",
"#fig:organic:honey":"4.54",
"#fig:organic:viscosity":"4.55",
"#fig:organic:structural":"4.56",
"#fig:organic:carboxylicdimer":"4.57",
"#fig:organic:vapourpressure":"4.58",
"#fig:organic:chlorinehaloalk":"4.59",
"#fig:organic:mpbpClhaloalk":"4.60",
"#fig:organic:dissociationcarboxylicacid":"4.61",
"#fig:organic:carboxylicdimer2":"4.62",
"#fig:organic:ketonehbond":"4.63",
"#fig:organic:alkanespic":"4.64",
"#fig:organic:intermolecular":"4.65",
"#fig:organic:alkanelength":"4.66",
"#fig:organic:chainlength":"4.67",
"#fig:organic:chains":"4.68",
"#fig:organic:branchedprop":"4.69",
"#fig:organic:cracking":"4.70",
"#fig:organic:fractionating_column1":"4.71",
"#fig:organic:fractionating_column":"4.72",
"#fig:organic:combust":"4.73",
"#fig:organic:combustexample":"4.74",
"#fig:organic:esterification":"4.75",
"#fig:organic:butylpropanoate":"4.76",
"#fig:organic:hydrohalogenation":"4.77",
"#fig:organic:halogenadd":"4.78",
"#fig:organic:halogenation":"4.79",
"#fig:organic:hydration":"4.80",
"#fig:organic:hydrationmajor":"4.81",
"#fig:organic:hydrogenation":"4.82",
"#fig:organic:hydrogenation":"4.83",
"#fig:organic:PVC":"4.84",
"#fig:organic:KIelim":"4.85",
"#fig:organic:elimination":"4.86",
"#fig:organic:bromobutane":"4.87",
"#fig:organic:elimethanol":"4.88",
"#fig:organic:dehydrationsaturated":"4.89",
"#fig:organic:haloalkanestert":"4.90",
"#fig:organic:forminghaloalkanes":"4.91",
"#fig:organic:subformingalcohols":"4.92",
"#fig:organic:subformingalcohols2":"4.93",
"#fig:organic:haloalkanesub":"4.94",
"#fig:organic:polyethenepics":"4.95",
"#fig:organic:ethylene":"4.96",
"#fig:organic:polyethene_n":"4.97",
"#fig:organic:polypropene":"4.98",
"#fig:organic:PVC":"4.99",
"#fig:organic:PVAslime":"4.100",
"#fig:organic:PVA":"4.101",
"#fig:organic:polystyrene2":"4.102",
"#fig:organic:polyesterlinkage":"4.103",
"#fig:organic:polyester2":"4.104",
"#fig:organic:PLA":"4.105",
"#fig:organic:PLA2":"4.106",
"#fig:wpe12:wgeneral":"5.1",
"#fig:wpe12:wgeneral":"5.2",
"#fig:wpe12:powerlifters":"5.3",
"#fig:wpe12:wparallel":"5.4",
"#fig:wep:carry":"5.5",
"#fred":"5.6",
"#p:wsl:de12:sss":"6.1",
"#fig:reactionrates:physical":"7.1",
"#fig:reactionrates:surfacearea":"7.2",
"#fig:reactionrates:hydrogenperoxide":"7.3",
"#fig:reactionrates:gassyringe":"7.4",
"#fig:reactionrates:gasgraph":"7.5",
"#fig:reactionrates:cross":"7.6",
"#fig:reactionrates:gasescape":"7.7",
"#fig:reactionrates:massloss":"7.8",
"#fig:reactionrates:particleenergydistribution":"7.9",
"#fig:reactionrates:distributionwithT":"7.10",
"#fig:reactionrates:activationenergyendo":"7.11",
"#fig:reactionrates:activationenergyexo":"7.12",
"#fig:reactionrates:catalystprob":"7.13",
"#fig:reactionrates:catalyst":"7.14",
"#fig:chemequil:equilibrium":"8.1",
"#fig:tab:Kcval":"8.2",
"#fig:chemicalequilibrium:pressure":"8.3",
"#fig:acidsandbases:acids":"9.1",
"#fig:acidsandbases:acidetching":"9.3",
"#fig:acidsandbases:indicators":"9.4",
"#fig:acidsandbases:cystine":"9.5",
"#fig:acidsandbases:aminoacid":"9.6",
"#fig:acidsandbases:cysteine":"9.7",
"#fig:acidsandbases:guanidine":"9.8",
"#fig:conductor":"11.1",
"#fig:ac":"11.2",
"#fig:ACgen":"11.3",
"#fig:ACGraph":"11.4",
"#fig:DCgen":"11.5",
"#fig:DCsignal":"11.6",
"#fig:ACmotor":"11.7",
"#fig:DCmotor":"11.8",
"#phot_el":"12.1",
"#fig:red-electroscope":"12.2",
"#fig:blue-electroscope":"12.3",
"#photo_app":"12.2",
"#dischargetube":"12.3",
"#hydrogenspectrum":"12.4",
"#fig:Henergy":"12.5",
"#fig:emissionSpec":"12.6",
"#fig:absorptionSpec":"12.7",
"#fig:electrochemical:batterytypes":"13.1",
"#fig:electrochemical:lemonbattery":"13.2",
"#fig:electrochemical:coppersulfatezinc":"13.3",
"#fig:electrochemical:zinctocopper":"13.4",
"#fig:electrochemical:abbreviations":"13.5",
"#fig:electrochemical:galvanic":"13.6",
"#fig:electrochemical:electrolytics":"13.7",
"#fig:electrochemical:hoffman":"13.8",
"#fig:electrochemical:hydrogenelectrode":"13.9",
"#fig:electrochemical:zinchydrogen":"13.10",
"#fig:electrochemical:copperhydrogen":"13.11",
"#fig:electrochemical:spontaneity":"13.12",
"#fig:electrochemical:electroplating":"13.13",
"#fig:electrochemical:electrowinning":"13.14",
"#fig:mercurycell":"13.15",
"#fig:diaphragmcell":"13.16",
"#fig:membranecell":"13.17",
"#fig:chemind:farming":"14.1",
"#fig:chemind:fertilisers":"14.2",
"#fig:chemind:manufacturing":"14.3",
"#fig:chemind:fractionaldist":"14.4",
"#fig:chemind:ammoniumnitrate":"14.5",
"#fig:chemind:urea":"14.6",
"#fig:chemind:manure":"14.7",
"#fig:chemind:guano":"14.8",
"#fig:chemind:guano":"14.9",
"#fig:chemind:limestone":"14.10",
"#fig:chemind:potash":"14.11",
"#fig:chemind:algalbloom":"14.12",}

# and the table ref dictionary
table_ref_dict = {"#table:momentumandimpulse:units":"2.1",
"#table:verticalprojectilemotion:units":"3.1",
"#tab:organic:summary":"4.1",
"#tab:organic:homologousseries":"4.2",
"#tab:organic:isomertable":"4.3",
"#tab:organic:acidesterisomertable":"4.4",
"#tab:organic:suffix":"4.5",
"#tab:organic:prefix":"4.6",
"#tab:organic:prefix2":"4.7",
"#tab:organic:halogens":"4.8",
"#tab:organic:meltingboiling":"4.9",
"#tab:organic:flammability":"4.10",
"#tab:organic:functionalprop":"4.11",
"#tab:organic:bpdimerisation":"4.12",
"#tab:organic:alkaneprop":"4.13",
"#tab:organic:alkane2":"4.14",
"#tab:organic:branchedprop":"4.15",
"#tab:organic:esteruses":"4.16",
"#tab:organic:polymersadd":"4.17",
"#tab:organic:monomerpolymeradd":"4.18",
"#tab:organic:polymerscond":"4.19",
"#tab:organic:monomerpolymercond":"4.20",
"#tab:organic:recycling":"4.21",
"#table:doppler:units":"6.1",
"#tab:chemicalequilibrium:RICEtable":"8.1",
"#tab:acidsandbases":"9.1",
"#tab:acidsandbases:arrhenius":"9.2",
"#tab:acidsandbases:bronstedlowry":"9.3",
"#tab:acidsandbases:summarytable":"9.4",
"#tab:acidsandbases:Kavalues":"9.5",
"#tab:acidsandbases:commonpH":"9.6",
"#tab:acidsandbases:phinfo":"9.7",
"#tab:acidsandbases:salthydrolysis":"9.8",
"#tab:acidsandbases:indicators":"9.9",
"#tab:acidsandbases:hairrelaxers":"9.1",
"#table:waves::units":"10.1",
"#tab:work_fun":"12.1",
"#table:opticalphenomena:units":"12.2",
"#tab:electrochemical:reductionpotential":"13.1",
"#tab:electrochemical:redpotexamples":"13.2",
"#tab:electrochemical:comparison":"13.3",
"#tab:chemind:nonmineralnutrientsource":"14.1",
"#tab:chemind:mineralnutrientsource":"14.2",
"#tab:chemind:NPK":"14.3",
"#tab:chemind:detailmineral":"14.4",}

chapterList = [[1, "Sequences and series"],
[2, "Functions"],
[3, "Finance"],
[4, "Trigonometry"],
[5, "Polynomials"],
[6, "Differential calculus"],
[7, "Analytical geometry"],
[8, "Euclidean geometry"],
[9, "Statistics"],
[10, "Probability"],]

sectionList = {"scEMCDP": 1.1,
"scEMCDR": 1.2,
"scEMCDV": 1.3,
"scEMCDX": 1.4,
"scEMCDZ": 1.5,
"scEMCF3": 1.6,
"scEMCF5": 1.7,
"scEMCF6": 2.1,
"scEMCF7": 2.2,
"scEMCF8": 2.3,
"scEMCF9": 2.4,
"scEMCFF": 2.6,
"scEMCFC": 2.5,
"scEMCFQ": 2.7,
"scEMCFR": 2.8,
"scEMCFX": 3.1,
"scEMCFY": 3.2,
"scEMCFZ": 3.3,
"scEMCG4": 3.4,
"scEMCG6": 3.5,
"scEMCG8": 3.6,
"scEMCG9": 4.1,
"scEMCGB": 4.2,
"scEMCGD": 4.3,
"scEMCGH": 4.4,
"scEMCGK": 4.5,
"scEMCGP": 4.6,
"scEMCGQ": 5.1,
"scEMCGT": 5.2,
"scEMCGV": 5.3,
"scEMCGW": 5.4,
"scEMCGX": 5.5,
"scEMCGY": 5.6,
"scEMCGZ": 6.1,
"scEMCH6": 6.2,
"scEMCH7": 6.3,
"scEMCH8": 6.4,
"scEMCH9": 6.5,
"scEMCHB": 6.6,
"scEMCHH": 6.7,
"scEMCHM": 6.8,
"scEMCHN": 7.1,
"scEMCHW": 7.3,
"scEMCHS": 7.2,
"scEMCHX": 7.4,
"scEMCHY": 8.1,
"scEMCJ8": 8.2,
"scEMCJ9": 8.3,
"scEMCJB": 8.4,
"scEMCJD": 8.5,
"scEMCJH": 8.6,
"scEMCJJ": 8.7,
"scEMCJK": 9.1,
"scEMCJP": 9.2,
"scEMCJS": 9.3,
"scEMCJT": 9.4,
"scEMCJV": 10.1,
"scEMCJX": 10.2,
"scEMCJY": 10.3,
"scEMCJZ": 10.4,
"scEMCK3": 10.5,
"scEMCK4": 10.6,
"scEMCK5": 10.7,
"scEMCK6": 10.8,}

sectionListKeys = sectionList.keys()

subsectionList = ["scEMCDQ",
"scEMCDS",
"scEMCDT",
"scEMCDW",
"scEMCDY",
"scEMCF2",
"scEMCF4",
"scEMCFB",
"scEMCFD",
"scEMCFG",
"scEMCFH",
"scEMCFJ",
"scEMCFK",
"scEMCFM",
"scEMCFN",
"scEMCFP",
"scEMCFS",
"scEMCFT",
"scEMCFV",
"scEMCFW",
"scEMCG2",
"scEMCG3",
"scEMCG5",
"scEMCG7",
"scEMCGC",
"scEMCGF",
"scEMCGG",
"scEMCGJ",
"scEMCGM",
"scEMCGN",
"scEMCGR",
"scEMCGS",
"scEMCH2",
"scEMCH3",
"scEMCH4",
"scEMCH5",
"scEMCHC",
"scEMCHD",
"scEMCHF",
"scEMCHG",
"scEMCHJ",
"scEMCHK",
"scEMCHP",
"scEMCHQ",
"scEMCHR",
"scEMCHT",
"scEMCHV",
"scEMCHZ",
"scEMCJ2",
"scEMCJ3",
"scEMCJ4",
"scEMCJ5",
"scEMCJ6",
"scEMCJ7",
"scEMCJC",
"scEMCJF",
"scEMCJG",
"scEMCJM",
"scEMCJN",
"scEMCJQ",
"scEMCJR",
"scEMCJW",
"scEMCK2",]

wex_dictionary = {'Inverses - domain, range and restrictions': 8, 'Further arrangement of outcomes without repetition': 14, 'Proportion theorem': 3, 'Determining the value of ': 1, 'Double angle identities': 8, 'Logarithmic form to exponential form': 11, 'Revision': 1, 'Similar polygons': 4, 'Intuitive curve fitting': 4, 'Probability of word arrangements': 20, 'Using a calculator: inverse logarithm function': 16, 'Population growth': 21, 'Gradient at a point': 6, 'Exponential function': 3, 'Choices without repetition': 10, 'Inclination of a straight line': 2, 'Problems in three dimensions - height of a building': 16, 'Finding the remainder': 7, 'Using the SHARP EL-531VH calculator': 7, 'Compound angle formulae': 6, 'Derivation of ': 4, 'Finding stationary points': 18, 'Flu epidemic': 3, 'Using the quadratic formula': 2, 'Fitting by hand': 5, 'Finding the general solution': 9, 'Calculating the monthly payments': 9, 'Personal Identification Numbers (PINs)': 18, 'Factorising cubic polynomials': 12, 'Solving logarithmic equations': 26, 'Graphs of the inverse of ': 18, 'Graphs of ': 19, 'Sum to infinity': 17, 'Linear function': 1, 'Five number summary': 1, 'Long division': 4, 'Variance and standard deviation': 2, 'Finding the second derivative': 16, 'Solving quadratic equations by completing the square': 3, 'The number of letter arrangements for a longer word': 17, 'Differentiation from first principles': 10, 'Present value annuities': 8, 'Inverses - average gradient': 9, 'Arrangement of objects with constraints': 15, 'Equation of a circle with centre at the origin': 6, 'Determining the value of an investment': 6, 'Inverse of the function ': 6, 'Limit notation': 1, 'The arrangement of outcomes without repetition': 12, 'Two-way contingency tables': 9, 'Independent and dependent events': 3, 'Equation of a tangent to a circle': 15, 'Sum of a geometric series': 13, 'Tree diagrams': 8, 'Analysing loan options': 13, 'Inverses - domain, range and intercepts': 5, 'Properties of polygons': 1, 'Theorem of Pythagoras': 8, 'Using the CASIO ':8,
'Determining the intercepts': 17, 'Using a calculator: logarithm function': 15, 'Arithmetic sequence': 1, 'Using the remainder to solve for an unknown variable': 8, 'Choices with repetition': 11, 'Using a calculator: change of base': 17, 'Method of least squares by hand': 6, 'Proportionality of triangles': 2, 'Solving cubic equations': 14, 'Exponential form to logarithmic form': 10, 'Rate of change': 23, 'Sigma notation': 6, 'Interpreting graphs': 20, 'Applying the logarithm definition': 1, 'The addition rule for ': 4, 'Factor theorem': 10, 'Graph of ': 20, 'Limits': 3, 'General formula for the sum of an arithmetic sequence': 7, 'The addition rule': 5, 'Future value annuities': 4, 'Solving quadratic equations using factorisation': 1, 'Optimisation problems': 22, 'Using the sum to infinity to convert recurring decimals to fractions': 16, 'Analysing investment opportunities': 12, 'Parallel lines': 3, 'Sinking funds': 7, 'Applying the logarithmic law ': 23, 'Simplification of logarithms': 24, 'Rules of differentiation': 12, 'Quadratic function': 2, 'Synthetic division': 6, 'Sum to infinity of a geometric series': 15, 'Special logarithmic values': 2, 'Skewed and symmetric data': 3, 'Sum of an arithmetic sequence if first and last terms are known': 8, 'Finding ': 10, 'Arrangement of letters': 16, 'Number plates': 19, 'Trigonometric equations': 12, 'Quadratic sequence': 2, 'Repayment periods': 11, 'The correlation coefficient': 9, 'Problem in two dimensions': 14, 'Area, sine and cosine rule': 13, 'Venn diagrams': 7, 'Problems in three dimensions - height of a pole': 15, 'Finding the equation of a normal to a curve': 15, 'Sketching cubic graphs': 19, 'Factorial notation': 13, 'The complementary rule': 6, 'Dependent and independent events': 1, 'Finding the equation of a tangent to a curve': 14, 'Calculating the outstanding balance of a loan': 10, 'Duration of investments': 2, 'Similarity of triangles': 7, 'Equation of a circle with centre at ': 11}

# number the figure and table references
def fig_ref_fix(xml):
    '''current code is <a href="blah" data-class="InternalLink">blah</a>. We want this to become <a href="blah" data-class="InternalLink">figure x</a> or table x if we are doing the tables'''
    for a in xml.findall('.//a'):
        aTag = etree.Element('a')
        href = a.get('href')  # the href of the tag
        if href in fig_ref_dict:  # we find the hRef in the figure keys
            aTag.clear()  # clear the contents of the tag
            a.text = 'Figure {}'.format(fig_ref_dict[href])  # replace the text of the tag with the value of the key in the fig ref dict and the word Figure
        elif href in table_ref_dict:  # we find the hRef in the table keys
            aTag.clear()  # clear the contents of the tag
            a.text = 'Table {}'.format(table_ref_dict[href])  # replace the text of the tag with the value of the key in the table ref dict and the word Table
    return xml  # returns what we need


# the other piece is to fix the captions
def fig_caption(xml):
    '''current code is <div id="fig-atom-plumpudding" class="figure"><img src="pspicture/90cffe92260bc3815a6825cbb0d87b39.png" alt="90cffe92260bc3815a6825cbb0d87b39.png"/><div class="figcaption"><p>The atom according to the Plum Pudding model.</p></div></div>. We need to identify the figure from the overarching href and then modify the caption div to state: Figure x: blah
    To repeat for tables we need to take the current code: <div id="blah" data-class="FigureTable"><table>code</table><div class="caption"><p>caption</p></div></div>, identify the table and modify the caption to state Table y: blah
    '''
    for div in xml.findall('.//div[@class]'):  # find all divs with attribute class
        if div.attrib['class'] == 'figure':  # only work on the divs we actually want, this may change to be the same as the tables
            caption = div.find('.//div')
            if caption is not None:
                caption = div.find('.//div').find('.//p')  # extract just the caption bit
                try:
                    figId = '#' + div.attrib['id'].replace('-', ':')  # temporary hack to get the id's correct, the # will always be needed but the replace can be removed when the validator updates are completed
                    #div.set('id', figId)  # attempting to put in a hack to fix the id problem
                    if figId in fig_ref_dict:
                        # caption.text = 'Figure ' + fig_ref_dict[figId] + ': ' + caption.text
                        caption.text = 'Figure {}: {}'.format(fig_ref_dict[figId], caption.text)
                except:
                    pass
    for div in xml.findall('.//div[@data-class]'):  # find all the divs with data-class
        if div.attrib['data-class'] == 'FigureTable':  # check that data-class does equal to FigureTable
            caption = div.find('.//div')
            if caption is not None:
                caption = div.find('.//div').find('.//p')  # extract just the caption bit
                try:
                    tableId = '#' + div.attrib['id'].replace('-', ':')  # temporary hack to get the id's correct, the # will always be needed but the replace can be removed when the validator updates are completed
                    #div.set('id', tableId)  # attempting to put in a hack to fix the id problem
                    if tableId in table_ref_dict:
                        # caption.text = 'Table ' + table_ref_dict[tableId] + ': ' + caption.text
                        caption.text = 'Table {}: {}'.format(table_ref_dict[tableId], caption.text)
                except:
                    pass
    return xml


# now trying the chapter and section number function
def chapter_section_number(xml):
    '''This updates the appropriate h1 and h2 tags with a number. The number is determined from an appropriate dictionary. This uses the shortcodes to match the section and subsection headers but uses the chapter name to match the chapter numbers. The chapters might need some manual fixing while the sections and subsections should not.'''
    for h1 in xml.findall('.//h1'):  # loop over the h1's
        for i in range(len(chapterList)):  # loop over the chapter list
            if h1.text == chapterList[i][1]:  # check if h1 matches a chapter title.
                newText = 'Chapter {}: {}'.format(str(chapterList[i][0]), h1.text) # If T then add number, else ignore
                h1.text = newText
    # use the shortcode to tag the h2's with a number and the shortcode, repeat for h3's but only add the shortcode
    for div in xml.findall('.//div[@id]'):
        if div.attrib['id'] in sectionListKeys:
            for k in range(len(sectionListKeys)):
                if div.attrib['id'] == sectionListKeys[k]:
                    shortcode = etree.Element('span')
                    shortcode.text = '({})'.format(sectionListKeys[k][2:])
                    shortcode.set('class', 'shortcode')
                    h2 = div.find('h2')
                    if h2 is not None:
                        h2.text = '{} {} '.format(str(sectionList[sectionListKeys[k]]), div.find('h2').text)
                        h2.append(shortcode)
        # use the shortcode to tag the h3's with the shortcode only
        if div.attrib['id'] in subsectionList:  # iterate through the subsectionList
            for j in range(len(subsectionList)):
                if div.attrib['id'] == subsectionList[j]:
                    shortcode = etree.Element('span')
                    shortcode.text = '({})'.format(subsectionList[j][2:])
                    shortcode.set('class', 'shortcode')
                    h3 = div.find('h3')
                    try:  # for some reason using if h3 is not None fails to stop some errors so reverted to try block
                        h3.text = '{} '.format(div.find('h3').text)  # If the text matches the dictionary then add the number. Else ignore.
                        h3.append(shortcode)
                    except:
                        pass
    return xml  # Return the updated xml


# next up: number the worked examples
def wex_number(xml):
    '''
    Number the worked examples using the wex dictionary. This will be fuzzy matching since it uses the titles and the titles sometimes contain strange characters or maths that cannot be matched.
    Wexes are defined as <div class="worked_example"><h1 class="title">Standard notation</h1>
    This modifies the wex code to be <div class="worked_example"><h1 class="title">Worked example 5: Standard notation</h1>
    '''
    #find the worked examples
    for div in xml.findall('.//div[@class]'):  # find all divs with attribute class
        if div.attrib['class'] == 'worked_example':  # only work on the divs we actually want
            title = div.find('.//h1')
            if title is not None:
                try:
                    if title.text in wex_dictionary:
                        title.text = 'Worked example {}: {}'.format(wex_dictionary[title.text], title.text)  # add the number using the dictionary
                except:
                    pass
    return xml  # return the updated xml


# number the exerices
def exercise_number(xml):
    '''
    Number the exercises using ??.
    Still deciding where to put the number.
    Exercises currently are <div class="section"><h2 class="title" id="toc-id-11">Exercises</h2>
    This part of the script gets complicated and I am not 100% sure why each bit works
    '''
    global exercise_counter  # danger!
    for div in xml.findall('.//div[@class]'):  # find all divs with classes
        title = div.find('.//h2')  # find the title
        ps = div.find('.//div[@class]')  # find the problemset
        if ps != None and ps.attrib['class'] == 'problemset':  # verify that we do have a problemset
            if title != None and title.text == 'Exercises':  # now find just the exercises
                span_code = etree.Element('span')  # make a span
                span_code.set('class', 'exerciseTitle')  # set the class of the span
                span_code.text = 'Exercise {}.{}'.format(file_number, exercise_counter)  # add the counter as text along with the file number
                ps.insert(0, span_code)  # append the exercise counter after the initial problemset
                # to change where span is inserted find the index, see here: http://stackoverflow.com/questions/7474972/python-lxml-append-element-after-another-element
                exercise_counter += 1  # if I have this correctly this only affects the local instance of the counter
                span_end = etree.Element('span')  # trying to add the bit about practice
                span_end.set('class', 'practiceInfo')  # set the class of the span
                practice_link = etree.SubElement(span_end, 'a')  # make a link
                span_end.text = 'For more exercises, visit '  # change to science for the science one
                practice_link.set('href', 'http://www.everythingmaths.co.za')  # set the class of the link
                practice_link.text = 'www.everythingmaths.co.za'  # set the text of the link
                practice_link.tail = ' and click on "Practice Maths"'  # add a tail to the link
                ps.append(span_end)  # add it to the end of the problemset
    return xml

# Put it all together
#path = '/home/heather/Desktop/books/physical-sciences-12/english/build/xhtml'
path = '/home/heather/Desktop/books/mathematics-12/english/build/xhtml/'
#path = '/home/heather/Desktop/books/scripts/test-files'

fileList = os.listdir(path)
fileList.sort()

file_counter = 1  # set a file counter
exercise_counter = 1  # set an exercise counter

for file_name in fileList:
    full_file_name = '{}/{}'.format(path, file_name)

    # Skip directories
    if os.path.isdir(full_file_name):
        continue

    if file_name[0] not in ['0', '1', '2']:  # we need to ignore anything that does not start with a number
        continue

    xml = etree.parse(full_file_name, etree.HTMLParser())

    title_exercise = xml.findall('.//h2')  # trying to find h2's in the file

    file_number = int(file_name[:2])  # set a file number

    random_number = 0  # only way I could think of to do this
    for i in title_exercise:  # find out if there is Exercises in the file
        if i.text == 'Exercises':
            random_number += 1
    if random_number != 0:  # we did find Exercises so now we can play with the counters
        if file_counter != file_number:  # if not then we must increment the file counter and reset the exercise counter
            file_counter += 1
            exercise_counter = 1
    
    fileText = None

    #xml = fig_ref_fix(xml)
    #xml = fig_caption(xml)
    xml = chapter_section_number(xml)
    xml = wex_number(xml)
    xml = exercise_number(xml)
    
    fileText = etree.tostring(xml, pretty_print=True)

    # target_filename = '{}/heather.txt'.format(path)

    if fileText:
        with open(full_file_name, 'w') as file:
            file.write(fileText)
