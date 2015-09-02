'''Attempting to make an automatic numbering script
This script does the following:
1. Updates the anchor tags to have the correct figure or table reference. This is only needed for science at present.
2. Updates the figure and table caption tags to have a prefix of table x: or figure x:. Again only for science.
3. Updates chapter titles, section titles and subsection titles. Chapter titles need chapter x: as  a prefix, section titles need no title shortcode and subsection titles just need the shortcode at the end.
4. Numbers the worked examples.
5. Numbers the exercises (to be implemented).
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

chapterList = [[1, "Skills for science"],
[2, "Momentum and impulse"],
[3, "Vertical projectile motion in one dimension"],
[4, "Organic molecules"],
[5, "Work, energy and power"],
[6, "Doppler effect"],
[7, "Rateand Extent of Reaction"],
[8, "Chemical equilibrium"],
[9, "Acids and bases"],
[10, "Electric circuits"],
[11, "Electrodynamics"],
[12, "Optical phenomena and properties of matter"],
[13, "Electrochemical reactions"],
[14, "The chemical industry"],]

sectionList = {"scESCHQ": 1.1,
"scESCHT": 1.2,
"scESCHX": 1.3,
"scESCJ4": 1.4,
"scESCJ6": 2.1,
"scESCJ7": 2.2,
"scESCJB": 2.3,
"scESCJC": 2.4,
"scESCJK": 2.5,
"scESCJM": 2.6,
"scESCJT": 2.7,
"scESCJV": 3.1,
"scESCJW": 3.2,
"scESCK2": 3.3,
"scESCK3": 4.1,
"scESCK4": 4.2,
"scESCKG": 4.3,
"scESCKP": 4.4,
"scESCKV": 4.5,
"scESCKY": 4.6,
"scESCM4": 4.7,
"scESCM8": 4.8,
"scESCM9": 5.1,
"scESCMB": 5.2,
"scESCMD": 5.3,
"scESCMG": 5.4,
"scESCMJ": 5.5,
"scESCMK": 5.6,
"scESCMM": 6.1,
"scESCMN": 6.2,
"scESCMS": 6.3,
"scESCMV": 6.4,
"scESCMW": 7.1,
"scESCMX": 7.2,
"scESCN3": 7.3,
"scESCN8": 7.4,
"scESCNC": 7.5,
"scESCND": 8.1,
"scESCNJ": 8.2,
"scESCNN": 8.3,
"scESCNY": 8.4,
"scESCNZ": 9.1,
"scESCP8": 9.2,
"scESCPB": 9.3,
"scESCPJ": 9.4,
"scESCPN": 9.5,
"scESCPR": 9.6,
"scESCPS": 10.1,
"scESCPT": 10.2,
"scESCPV": 10.3,
"scESCPW": 10.4,
"scESCPZ": 10.5,
"scESCQ2": 10.6,
"scESCQ3": 11.1,
"scESCQ4": 11.2,
"scESCQC": 11.3,
"scESCQG": 11.4,
"scESCQH": 12.1,
"scESCQJ": 12.2,
"scESCQR": 12.3,
"scESCQW": 12.4,
"scESCQX": 13.1,
"scESCQY": 13.2,
"scESCR3": 13.3,
"scESCR7": 13.4,
"scESCRB": 13.5,
"scESCRF": 13.6,
"scESCRP": 13.7,
"scESCRT": 13.8,
"scESCRV": 14.1,
"scESCRW": 14.2,
"scESCRY": 14.3,
"scESCS3": 14.4,
"scESCSJ": 14.5,
"scESCSS": 14.6,
"scESCSV": 14.7,}

sectionListKeys = sectionList.keys()

subsectionList = ["scESCHR",
"scESCHS",
"scESCHV",
"scESCHW",
"scESCHY",
"scESCHZ",
"scESCJ2",
"scESCJ3",
"scESCJ5",
"scESCJ8",
"scESCJ9",
"scESCJD",
"scESCJF",
"scESCJG",
"scESCJH",
"scESCJJ",
"scESCJN",
"scESCJP",
"scESCJQ",
"scESCJR",
"scESCJS",
"scESCJX",
"scESCJY",
"scESCJZ",
"scESCK5",
"scESCK6",
"scESCK7",
"scESCK8",
"scESCK9",
"scESCKB",
"scESCKC",
"scESCKD",
"scESCKF",
"scESCKH",
"scESCKJ",
"scESCKK",
"scESCKM",
"scESCKN",
"scESCKQ",
"scESCKR",
"scESCKS",
"scESCKT",
"scESCKW",
"scESCKX",
"scESCKZ",
"scESCM2",
"scESCM3",
"scESCM5",
"scESCM6",
"scESCM7",
"scESCMC",
"scESCMF",
"scESCMH",
"scESCMP",
"scESCMQ",
"scESCMR",
"scESCMT",
"scESCMY",
"scESCMZ",
"scESCN2",
"scESCN4",
"scESCN5",
"scESCN6",
"scESCN7",
"scESCN9",
"scESCNB",
"scESCNF",
"scESCNG",
"scESCNH",
"scESCNK",
"scESCNM",
"scESCNP",
"scESCNQ",
"scESCNR",
"scESCNS",
"scESCNT",
"scESCNV",
"scESCNW",
"scESCNX",
"scESCP2",
"scESCP3",
"scESCP4",
"scESCP5",
"scESCP6",
"scESCP7",
"scESCP9",
"scESCPC",
"scESCPD",
"scESCPF",
"scESCPG",
"scESCPH",
"scESCPK",
"scESCPM",
"scESCPP",
"scESCPQ",
"scESCPX",
"scESCPY",
"scESCQ5",
"scESCQ6",
"scESCQ7",
"scESCQ8",
"scESCQ9",
"scESCQB",
"scESCQD",
"scESCQF",
"scESCQK",
"scESCQM",
"scESCQN",
"scESCQP",
"scESCQQ",
"scESCQS",
"scESCQT",
"scESCQV",
"scESCQZ",
"scESCR2",
"scESCR4",
"scESCR5",
"scESCR6",
"scESCR8",
"scESCR9",
"scESCRC",
"scESCRD",
"scESCRG",
"scESCRH",
"scESCRJ",
"scESCRK",
"scESCRM",
"scESCRN",
"scESCRQ",
"scESCRR",
"scESCRS",
"scESCRX",
"scESCRZ",
"scESCS2",
"scESCS4",
"scESCS5",
"scESCS6",
"scESCS7",
"scESCS8",
"scESCS9",
"scESCSB",
"scESCSC",
"scESCSD",
"scESCSF",
"scESCSG",
"scESCSH",
"scESCSK",
"scESCSM",
"scESCSN",
"scESCSP",
"scESCSQ",
"scESCSR",
"scESCST",]

wex_dictionary = {'Identifying polymers': 37, 'Describing projectile motion': 6, 'NPK ratios': 2, 'The photoelectric effect using silver': 1, 'Writing expressions for ': 1, 'Concentration-time graphs': 10, 'Internal resistance in circuit with resistors in series': 7, 'Graphs of equilibrium': 12, 'Conservation of momentum': 10, 'Internal resistance and resistors in parallel': 8, "Ohm's Law, parallel network of resistors ": 5, 'Calculating work done on a box pulled at an angle.': 3, 'Interpreting velocity graphs': 7, 'Laptop transformer': 1, 'Equilibrium constant calculations': 7, 'Sliding up a slope [credit: OpenStax College Physics]': 10, 'Analysing a force graph': 17, 'Identifying types of polymerisation reactions': 39, 'Impulse and change in momentum': 15, 'A borehole': 14, 'Power in series and parallel networks of resistors': 9, 'Another elastic collision': 12, 'Determining starting materials of esters': 33, 'Calculating ': 5, 'Sliding footballer [credit: OpenStax College Physics]': 9, 'Laptop transformer power': 3, 'Naming carbonyl compounds': 28, ' [NSC 2011 Paper 1]': 3, 'Change in momentum': 6, 'Absorption': 4, 'An inelastic collision': 14, 'Block on an inclined plane [credit: OpenStax College]': 8, 'Work-energy theorem 2': 7, 'Approach 2, calculating the net force': 5, 'Naming the alcohols': 17, 'Work-energy theorem': 6, 'Reactions at the anode and cathode': 5, 'pH calculations': 12, 'Naming the alkenes': 8, 'Drawing graphs of projectile motion': 4, 'Impulsive cricketers': 16, 'Titration calculations': 14, 'Calculating the total momentum of a system': 7, 'Car chase [Excerpt from NSC 2011 Paper 1]': 18, 'Conjugate acid-base pairs': 1, 'Moving observer': 2, 'Determining ester names': 32, 'Naming carboxylic acids': 24, 'Naming esters': 26, 'Naming the haloalkanes': 14, 'Motors and generators [NSC 2011 Paper 1]': 4, 'Comparing physical properties': 29, 'Balancing redox reactions in an acid medium': 2, 'Momentum of a soccer ball': 1, 'Internal resistance and headlamps [NSC 2011 Paper 1]': 10,
'Calculating reagent concentration': 2, 'Calculating work on the car while braking': 2, 'Balancing redox reactions in an alkaline medium': 3, 'Equilibrium calculations': 4, 'Understanding galvanic cells': 4, 'Camera battery charger': 2, 'Stair climb': 13, 'Height of a projectile': 2, 'Ambulance siren': 1, 'An elastic collision': 11, 'Internal resistance': 6, 'NPK ratios in other countries': 3, 'Naming aldehydes': 18, 'Power calculation 2': 12, 'Power calculation 1': 11, 'Determining spontaneity': 13, 'Hot air balloon [NSC 2011 Paper 1]': 8, 'Calculating the EMF of a cell': 11, "Ohm's Law, all components in series": 2, "Using Le Chatelier's principle": 6, 'Balancing redox reactions': 1, 'Colliding billiard balls': 13, 'Naming ketones': 19, 'Balancing equations': 31, 'Approach 1, calculating the net work on a car': 4, 'Analysing graphs of projectile motion': 5, "Ohm's Law, series circuit": 3, 'Naming the alkynes': 11, 'Determining overall reactions': 9, 'Wheatstone bridge': 11, "Ohm's Law [NSC 2011 Paper 1]": 1, 'The photoelectric effect using gold': 2, 'Calculating work on a car when speeding up.': 1, "Ohm's Law, resistors connected in parallel": 4, 'Using the table of standard electrode potentials': 8, 'Chemical equilibrium': 11, 'Momentum of a cricket ball': 2, 'Momentum of the Moon': 3, 'Determining equations from starting materials': 10, 'Calculating concentration': 5, 'Acids and bases': 3, 'Equal displacements [attribution: Sunil Kumar Singh]': 3, 'Naming the alkanes': 5, 'Doppler effect [NSC 2011 Paper 1]': 3, 'Projectile motion': 1, 'Change in Momentum': 4, 'Identifying monomers': 36, 'Rate-time graphs': 8, 'Reaction rates': 2}

# ok, now to try the really tricksy bit: getting the right bits of the a tag that we want.
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
#def exercise_number(xml):
    #'''
    #Number the exercises using ??.
    #Still deciding where to put the number.
    #Exercises currently are <div class="section"><h2 class="title" id="toc-id-11">Exercises</h2>
    #'''
    #file_counter = 1  # set a file counter equal to 1
    #file_number = file_name[:2]  # set a file number equal to the first two chars of the file name
    #try:
        #if file_counter == int(file_number): # is the counter equal to the integer value of the file number?
            #exercise_counter = 1  # set an exercise counter equal to 1
            #for div in xml.findall('.//div[@class]'):  # find all divs with classes
                #title = div.find('.//h2')
                #if title != None:
                    #if title.text == 'Exercises':  # now find just the exercises
                        #span_code = etree.Element('span')  # make a span
                        #span_code.set('class', 'exercise_header')  # set the class of the span
                        #span_code.text = 'Exercise {}'.format(exercise_counter)  # add the counter as text
                        #title.insert(0, span_code)  #append the exercise counter after the title
                        #exercise_counter += 1  # increment the exercise counter
        #else:
            #file_counter += 1  # increment the file counter
        ##continue
    #except:
        #pass

# Put it all together
path = '/home/heather/Desktop/books/physical-sciences-12/english/build/xhtml'
#path = '/home/heather/Desktop/books/mathematics-12/english/build/xhtml/'
#path = '/home/heather/Desktop/books/scripts/test-files'

for file_name in os.listdir(path):
    full_file_name = '{}/{}'.format(path, file_name)

    # Skip directories
    if os.path.isdir(full_file_name):
        continue

    fileText = None

    xml = etree.parse(full_file_name, etree.HTMLParser())
    #xml = fig_ref_fix(xml)
    #xml = fig_caption(xml)
    #xml = chapter_section_number(xml)
    #xml = wex_number(xml)
    
    fileText = etree.tostring(xml, pretty_print=True)

    # target_filename = '{}/heather.txt'.format(path)

    if fileText:
        with open(full_file_name, 'w') as file:
            file.write(fileText)
