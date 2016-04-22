'''
Created on Apr 13, 2016

@author: lancer
'''
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import string

suffixes = {};
suffixes['ALLEE']= ('ALY','ALLEY','STREET')
suffixes['ALLEY']= ('ALY','ALLEY','STREET')
suffixes['ALLY']= ('ALY','ALLEY','STREET')
suffixes['ALY']= ('ALY','ALLEY','STREET')
suffixes['ANEX']= ('ANX','ANEX','STREET')
suffixes['ANNEX']= ('ANX','ANEX','STREET')
suffixes['ANNX']= ('ANX','ANEX','STREET')
suffixes['ANX']= ('ANX','ANEX','STREET')
suffixes['ARC ']= ('ARC','ARCADE','STREET')
suffixes['ARCADE ']= ('ARC','ARCADE','STREET')
suffixes['AV']= ('AVE','AVENUE','STREET')
suffixes['AVE']= ('AVE','AVENUE','STREET')
suffixes['AVEN']= ('AVE','AVENUE','STREET')
suffixes['AVENU']= ('AVE','AVENUE','STREET')
suffixes['AVENUE']= ('AVE','AVENUE','STREET')
suffixes['AVN']= ('AVE','AVENUE','STREET')
suffixes['AVNUE']= ('AVE','AVENUE','STREET')
suffixes['BAYOO']= ('BYU','BAYOU','STREET')
suffixes['BAYOU']= ('BYU','BAYOU','STREET')
suffixes['BCH']= ('BCH','BEACH','STREET')
suffixes['BEACH']= ('BCH','BEACH','STREET')
suffixes['BEND']= ('BND','BEND','STREET')
suffixes['BND']= ('BND','BEND','STREET')
suffixes['BLF']= ('BLF','BLUFF','STREET')
suffixes['BLUF']= ('BLF','BLUFF','STREET')
suffixes['BLUFF']= ('BLF','BLUFF','STREET')
suffixes['BLUFFS ']= ('BLFS','BLUFFS','STREET')
suffixes['BOT']= ('BTM','BOTTOM','STREET')
suffixes['BTM']= ('BTM','BOTTOM','STREET')
suffixes['BOTTM']= ('BTM','BOTTOM','STREET')
suffixes['BOTTOM']= ('BTM','BOTTOM','STREET')
suffixes['BLVD']= ('BLVD','BOULEVARD','STREET')
suffixes['BOUL']= ('BLVD','BOULEVARD','STREET')
suffixes['BOULEVARD ']= ('BLVD','BOULEVARD','STREET')
suffixes['BOULV']= ('BLVD','BOULEVARD','STREET')
suffixes['BR']= ('BR','BRANCH','STREET')
suffixes['BRNCH']= ('BR','BRANCH','STREET')
suffixes['BRANCH']= ('BR','BRANCH','STREET')
suffixes['BRDGE']= ('BRG','BRIDGE','STREET')
suffixes['BRG']= ('BRG','BRIDGE','STREET')
suffixes['BRIDGE']= ('BRG','BRIDGE','STREET')
suffixes['BRK']= ('BRK','BROOK','STREET')
suffixes['BROOK']= ('BRK','BROOK','STREET')
suffixes['BROOKS ']= ('BRKS','BROOKS','STREET')
suffixes['BURG']= ('BG','BURG','STREET')
suffixes['BURGS']= ('BGS','BURGS','STREET')
suffixes['BYP']= ('BYP','BYPASS','STREET')
suffixes['BYPA']= ('BYP','BYPASS','STREET')
suffixes['BYPAS']= ('BYP','BYPASS','STREET')
suffixes['BYPASS']= ('BYP','BYPASS','STREET')
suffixes['BYPS']= ('BYP','BYPASS','STREET')
suffixes['CAMP']= ('CP','CAMP','STREET')
suffixes['CP']= ('CP','CAMP','STREET')
suffixes['CMP']= ('CP','CAMP','STREET')
suffixes['CANYN']= ('CYN','CANYON','STREET')
suffixes['CANYON']= ('CYN','CANYON','STREET')
suffixes['CNYN']= ('CYN','CANYON','STREET')
suffixes['CAPE']= ('CPE','CAPE','STREET')
suffixes['CPE']= ('CPE','CAPE','STREET')
suffixes['CAUSEWAY']= ('CSWY','CAUSEWAY','STREET')
suffixes['CAUSWA']= ('CSWY','CAUSEWAY','STREET')
suffixes['CSWY']= ('CSWY','CAUSEWAY','STREET')
suffixes['CEN']= ('CTR','CENTER','STREET')
suffixes['CENT']= ('CTR','CENTER','STREET')
suffixes['CENTER']= ('CTR','CENTER','STREET')
suffixes['CENTR']= ('CTR','CENTER','STREET')
suffixes['CENTRE']= ('CTR','CENTER','STREET')
suffixes['CNTER']= ('CTR','CENTER','STREET')
suffixes['CNTR']= ('CTR','CENTER','STREET')
suffixes['CTR']= ('CTR','CENTER','STREET')
suffixes['CENTERS ']= ('CTRS','CENTERS','STREET')
suffixes['CIR']= ('CIR','CIRCLE','STREET')
suffixes['CIRC']= ('CIR','CIRCLE','STREET')
suffixes['CIRCL']= ('CIR','CIRCLE','STREET')
suffixes['CIRCLE']= ('CIR','CIRCLE','STREET')
suffixes['CRCL']= ('CIR','CIRCLE','STREET')
suffixes['CRCLE']= ('CIR','CIRCLE','STREET')
suffixes['CIRCLES']= ('CIRS','CIRCLES','STREET')
suffixes['CLF']= ('CLF','CLIFF','STREET')
suffixes['CLIFF']= ('CLF','CLIFF','STREET')
suffixes['CLFS']= ('CLFS','CLIFFS','STREET')
suffixes['CLIFFS']= ('CLFS','CLIFFS','STREET')
suffixes['CLB']= ('CLB','CLUB','STREET')
suffixes['CLUB']= ('CLB','CLUB','STREET')
suffixes['COMMON']= ('CMN','COMMON','STREET')
suffixes['COMMONS']= ('CMNS','COMMONS','STREET')
suffixes['COR']= ('COR','CORNER','STREET')
suffixes['CORNER']= ('COR','CORNER','STREET')
suffixes['CORNERS']= ('CORS','CORNERS','STREET')
suffixes['CORS']= ('CORS','CORNERS','STREET')
suffixes['COURSE']= ('CRSE','COURSE','STREET')
suffixes['CRSE']= ('CRSE','COURSE','STREET')
suffixes['COURT']= ('CT','COURT','STREET')
suffixes['CT']= ('CT','COURT','STREET')
suffixes['COURTS']= ('CTS','COURTS','STREET')
suffixes['CTS']= ('CTS','COURTS','STREET')
suffixes['COVE']= ('CV','COVE','STREET')
suffixes['CV']= ('CV','COVE','STREET')
suffixes['COVES']= ('CVS','COVES','STREET')
suffixes['CREEK']= ('CRK','CREEK','STREET')
suffixes['CRK']= ('CRK','CREEK','STREET')
suffixes['CRESCENT']= ('CRES','CRESCENT','STREET')
suffixes['CRES']= ('CRES','CRESCENT','STREET')
suffixes['CRSENT']= ('CRES','CRESCENT','STREET')
suffixes['CRSNT']= ('CRES','CRESCENT','STREET')
suffixes['CREST']= ('CRST','CREST','STREET')
suffixes['CROSSING ']= ('XING','CROSSING','STREET')
suffixes['CRSSNG ']= ('XING','CROSSING','STREET')
suffixes['XING ']= ('XING','CROSSING','STREET')
suffixes['CROSSROAD']= ('XRD','CROSSROAD','STREET')
suffixes['CROSSROADS']= ('XRDS','CROSSROADS','STREET')
suffixes['CURVE ']= ('CURV','CURVE','STREET')
suffixes['DALE ']= ('DL','DALE','STREET')
suffixes['DL ']= ('DL','DALE','STREET')
suffixes['DAM ']= ('DM','DAM','STREET')
suffixes['DM ']= ('DM','DAM','STREET')
suffixes['DIV']= ('DV','DIVIDE','STREET')
suffixes['DIVIDE']= ('DV','DIVIDE','STREET')
suffixes['DV']= ('DV','DIVIDE','STREET')
suffixes['DVD']= ('DV','DIVIDE','STREET')
suffixes['DR']= ('DR','DRIVE','STREET')
suffixes['DRIV']= ('DR','DRIVE','STREET')
suffixes['DRIVE']= ('DR','DRIVE','STREET')
suffixes['DRV']= ('DR','DRIVE','STREET')
suffixes['DRIVES']= ('DRS','DRIVES','STREET')
suffixes['EST']= ('EST','ESTATE','STREET')
suffixes['ESTATE']= ('EST','ESTATE','STREET')
suffixes['ESTATES']= ('ESTS','ESTATES','STREET')
suffixes['ESTS']= ('ESTS','ESTATES','STREET')
suffixes['EXP']= ('EXPY','EXPRESSWAY','STREET')
suffixes['EXPR']= ('EXPY','EXPRESSWAY','STREET')
suffixes['EXPRESS']= ('EXPY','EXPRESSWAY','STREET')
suffixes['EXPRESSWAY']= ('EXPY','EXPRESSWAY','STREET')
suffixes['EXPW']= ('EXPY','EXPRESSWAY','STREET')
suffixes['EXPY']= ('EXPY','EXPRESSWAY','STREET')
suffixes['EXT']= ('EXT','EXTENSION','STREET')
suffixes['EXTENSION']= ('EXT','EXTENSION','STREET')
suffixes['EXTN']= ('EXT','EXTENSION','STREET')
suffixes['EXTNSN']= ('EXT','EXTENSION','STREET')
suffixes['EXTS']= ('EXTS','EXTENSIONS','STREET')
suffixes['FALL']= ('FALL','FALL','STREET')
suffixes['FALLS']= ('FLS','FALLS','STREET')
suffixes['FLS']= ('FLS','FALLS','STREET')
suffixes['FERRY']= ('FRY','FERRY','STREET')
suffixes['FRRY']= ('FRY','FERRY','STREET')
suffixes['FRY']= ('FRY','FERRY','STREET')
suffixes['FIELD']= ('FLD','FIELD','STREET')
suffixes['FLD']= ('FLD','FIELD','STREET')
suffixes['FIELDS']= ('FLDS','FIELDS','STREET')
suffixes['FLDS']= ('FLDS','FIELDS','STREET')
suffixes['FLAT']= ('FLT','FLAT','STREET')
suffixes['FLT']= ('FLT','FLAT','STREET')
suffixes['FLATS']= ('FLTS','FLATS','STREET')
suffixes['FLTS']= ('FLTS','FLATS','STREET')
suffixes['FORD']= ('FRD','FORD','STREET')
suffixes['FRD']= ('FRD','FORD','STREET')
suffixes['FORDS']= ('FRDS','FORDS','STREET')
suffixes['FOREST']= ('FRST','FOREST','STREET')
suffixes['FORESTS']= ('FRST','FOREST','STREET')
suffixes['FRST']= ('FRST','FOREST','STREET')
suffixes['FORG']= ('FRG','FORGE','STREET')
suffixes['FORGE']= ('FRG','FORGE','STREET')
suffixes['FRG']= ('FRG','FORGE','STREET')
suffixes['FORGES']= ('FRGS','FORGES','STREET')
suffixes['FORK']= ('FRK','FORK','STREET')
suffixes['FRK']= ('FRK','FORK','STREET')
suffixes['FORKS']= ('FRKS','FORKS','STREET')
suffixes['FRKS']= ('FRKS','FORKS','STREET')
suffixes['FORT']= ('FT','FORT','STREET')
suffixes['FRT']= ('FT','FORT','STREET')
suffixes['FT']= ('FT','FORT','STREET')
suffixes['FREEWAY']= ('FWY','FREEWAY','STREET')
suffixes['FREEWY']= ('FWY','FREEWAY','STREET')
suffixes['FRWAY']= ('FWY','FREEWAY','STREET')
suffixes['FRWY']= ('FWY','FREEWAY','STREET')
suffixes['FWY']= ('FWY','FREEWAY','STREET')
suffixes['GARDEN']= ('GDN','GARDEN','STREET')
suffixes['GARDN']= ('GDN','GARDEN','STREET')
suffixes['GRDEN']= ('GDN','GARDEN','STREET')
suffixes['GRDN']= ('GDN','GARDEN','STREET')
suffixes['GARDENS']= ('GDNS','GARDENS','STREET')
suffixes['GDNS']= ('GDNS','GARDENS','STREET')
suffixes['GRDNS']= ('GDNS','GARDENS','STREET')
suffixes['GATEWAY']= ('GTWY','GATEWAY','STREET')
suffixes['GATEWY']= ('GTWY','GATEWAY','STREET')
suffixes['GATWAY']= ('GTWY','GATEWAY','STREET')
suffixes['GTWAY']= ('GTWY','GATEWAY','STREET')
suffixes['GTWY']= ('GTWY','GATEWAY','STREET')
suffixes['GLEN']= ('GLN','GLEN','STREET')
suffixes['GLN']= ('GLN','GLEN','STREET')
suffixes['GLENS']= ('GLNS','GLENS','STREET')
suffixes['GREEN']= ('GRN','GREEN','STREET')
suffixes['GRN']= ('GRN','GREEN','STREET')
suffixes['GREENS']= ('GRNS','GREENS','STREET')
suffixes['GROV']= ('GRV','GROVE','STREET')
suffixes['GROVE']= ('GRV','GROVE','STREET')
suffixes['GRV']= ('GRV','GROVE','STREET')
suffixes['GROVES']= ('GRVS','GROVES','STREET')
suffixes['HARB']= ('HBR','HARBOR','STREET')
suffixes['HARBOR']= ('HBR','HARBOR','STREET')
suffixes['HARBR']= ('HBR','HARBOR','STREET')
suffixes['HBR']= ('HBR','HARBOR','STREET')
suffixes['HRBOR']= ('HBR','HARBOR','STREET')
suffixes['HARBORS']= ('HBRS','HARBORS','STREET')
suffixes['HAVEN']= ('HVN','HAVEN','STREET')
suffixes['HVN']= ('HVN','HAVEN','STREET')
suffixes['HT']= ('HTS','HEIGHTS','STREET')
suffixes['HTS']= ('HTS','HEIGHTS','STREET')
suffixes['HIGHWAY']= ('HWY','HIGHWAY','STREET')
suffixes['HIGHWY']= ('HWY','HIGHWAY','STREET')
suffixes['HIWAY']= ('HWY','HIGHWAY','STREET')
suffixes['HIWY']= ('HWY','HIGHWAY','STREET')
suffixes['HWAY']= ('HWY','HIGHWAY','STREET')
suffixes['HWY']= ('HWY','HIGHWAY','STREET')
suffixes['HILL']= ('HL','HILL','STREET')
suffixes['HL']= ('HL','HILL','STREET')
suffixes['HILLS']= ('HLS','HILLS','STREET')
suffixes['HLS']= ('HLS','HILLS','STREET')
suffixes['HLLW']= ('HOLW','HOLLOW','STREET')
suffixes['HOLLOW']= ('HOLW','HOLLOW','STREET')
suffixes['HOLLOWS']= ('HOLW','HOLLOW','STREET')
suffixes['HOLW']= ('HOLW','HOLLOW','STREET')
suffixes['HOLWS']= ('HOLW','HOLLOW','STREET')
suffixes['INLT']= ('INLT','INLET','STREET')
suffixes['IS']= ('IS','ISLAND','STREET')
suffixes['ISLAND']= ('IS','ISLAND','STREET')
suffixes['ISLND']= ('IS','ISLAND','STREET')
suffixes['ISLANDS']= ('ISS','ISLANDS','STREET')
suffixes['ISLNDS']= ('ISS','ISLANDS','STREET')
suffixes['ISS']= ('ISS','ISLANDS','STREET')
suffixes['ISLE']= ('ISLE','ISLE','STREET')
suffixes['ISLES']= ('ISLE','ISLE','STREET')
suffixes['JCT']= ('JCT','JUNCTION','STREET')
suffixes['JCTION']= ('JCT','JUNCTION','STREET')
suffixes['JCTN']= ('JCT','JUNCTION','STREET')
suffixes['JUNCTION']= ('JCT','JUNCTION','STREET')
suffixes['JUNCTN']= ('JCT','JUNCTION','STREET')
suffixes['JUNCTON']= ('JCT','JUNCTION','STREET')
suffixes['JCTNS']= ('JCTS','JUNCTIONS','STREET')
suffixes['JCTS']= ('JCTS','JUNCTIONS','STREET')
suffixes['JUNCTIONS']= ('JCTS','JUNCTIONS','STREET')
suffixes['KEY']= ('KY','KEY','STREET')
suffixes['KY']= ('KY','KEY','STREET')
suffixes['KEYS']= ('KYS','KEYS','STREET')
suffixes['KYS']= ('KYS','KEYS','STREET')
suffixes['KNL']= ('KNL','KNOLL','STREET')
suffixes['KNOL']= ('KNL','KNOLL','STREET')
suffixes['KNOLL']= ('KNL','KNOLL','STREET')
suffixes['KNLS']= ('KNLS','KNOLLS','STREET')
suffixes['KNOLLS']= ('KNLS','KNOLLS','STREET')
suffixes['LK']= ('LK','LAKE','STREET')
suffixes['LAKE']= ('LK','LAKE','STREET')
suffixes['LKS']= ('LKS','LAKES','STREET')
suffixes['LAKES']= ('LKS','LAKES','STREET')
suffixes['LAND']= ('LAND','LAND','STREET')
suffixes['LANDING']= ('LNDG','LANDING','STREET')
suffixes['LNDG']= ('LNDG','LANDING','STREET')
suffixes['LNDNG']= ('LNDG','LANDING','STREET')
suffixes['LANE']= ('LN','LANE','STREET')
suffixes['LN']= ('LN','LANE','STREET')
suffixes['LGT']= ('LGT','LIGHT','STREET')
suffixes['LIGHT']= ('LGT','LIGHT','STREET')
suffixes['LIGHTS']= ('LGTS','LIGHTS','STREET')
suffixes['LF']= ('LF','LOAF','STREET')
suffixes['LOAF']= ('LF','LOAF','STREET')
suffixes['LCK']= ('LCK','LOCK','STREET')
suffixes['LOCK']= ('LCK','LOCK','STREET')
suffixes['LCKS']= ('LCKS','LOCKS','STREET')
suffixes['LOCKS']= ('LCKS','LOCKS','STREET')
suffixes['LDG']= ('LDG','LODGE','STREET')
suffixes['LDGE']= ('LDG','LODGE','STREET')
suffixes['LODG']= ('LDG','LODGE','STREET')
suffixes['LODGE']= ('LDG','LODGE','STREET')
suffixes['LOOP']= ('LOOP','LOOP','STREET')
suffixes['LOOPS']= ('LOOP','LOOP','STREET')
suffixes['MALL']= ('MALL','MALL','STREET')
suffixes['MNR']= ('MNR','MANOR','STREET')
suffixes['MANOR']= ('MNR','MANOR','STREET')
suffixes['MANORS']= ('MNRS','MANORS','STREET')
suffixes['MNRS']= ('MNRS','MANORS','STREET')
suffixes['MEADOW']= ('MDW','MEADOW','STREET')
suffixes['MDW']= ('MDWS','MEADOWS','STREET')
suffixes['MDWS']= ('MDWS','MEADOWS','STREET')
suffixes['MEADOWS']= ('MDWS','MEADOWS','STREET')
suffixes['MEDOWS']= ('MDWS','MEADOWS','STREET')
suffixes['MEWS']= ('MEWS','MEWS','STREET')
suffixes['MILL']= ('ML','MILL','STREET')
suffixes['MILLS']= ('MLS','MILLS','STREET')
suffixes['MISSN']= ('MSN','MISSION','STREET')
suffixes['MSSN']= ('MSN','MISSION','STREET')
suffixes['MOTORWAY']= ('MTWY','MOTORWAY','STREET')
suffixes['MNT']= ('MT','MOUNT','STREET')
suffixes['MT']= ('MT','MOUNT','STREET')
suffixes['MOUNT']= ('MT','MOUNT','STREET')
suffixes['MNTAIN']= ('MTN','MOUNTAIN','STREET')
suffixes['MNTN']= ('MTN','MOUNTAIN','STREET')
suffixes['MOUNTAIN']= ('MTN','MOUNTAIN','STREET')
suffixes['MOUNTIN']= ('MTN','MOUNTAIN','STREET')
suffixes['MTIN']= ('MTN','MOUNTAIN','STREET')
suffixes['MTN']= ('MTN','MOUNTAIN','STREET')
suffixes['MNTNS']= ('MTNS','MOUNTAINS','STREET')
suffixes['MOUNTAINS']= ('MTNS','MOUNTAINS','STREET')
suffixes['NCK']= ('NCK','NECK','STREET')
suffixes['NECK']= ('NCK','NECK','STREET')
suffixes['ORCH']= ('ORCH','ORCHARD','STREET')
suffixes['ORCHARD']= ('ORCH','ORCHARD','STREET')
suffixes['ORCHRD']= ('ORCH','ORCHARD','STREET')
suffixes['OVAL']= ('OVAL','OVAL','STREET')
suffixes['OVL']= ('OVAL','OVAL','STREET')
suffixes['OVERPASS']= ('OPAS','OVERPASS','STREET')
suffixes['PARK']= ('PARK','PARK','STREET')
suffixes['PRK']= ('PARK','PARK','STREET')
suffixes['PARKS']= ('PARK','PARKS','STREET')
suffixes['PARKWAY']= ('PKWY','PARKWAY','STREET')
suffixes['PARKWY']= ('PKWY','PARKWAY','STREET')
suffixes['PKWAY']= ('PKWY','PARKWAY','STREET')
suffixes['PKWY']= ('PKWY','PARKWAY','STREET')
suffixes['PKY']= ('PKWY','PARKWAY','STREET')
suffixes['PARKWAYS']= ('PKWY','PARKWAYS','STREET')
suffixes['PKWYS']= ('PKWY','PARKWAYS','STREET')
suffixes['PASS']= ('PASS','PASS','STREET')
suffixes['PASSAGE']= ('PSGE','PASSAGE','STREET')
suffixes['PATH']= ('PATH','PATH','STREET')
suffixes['PATHS']= ('PATH','PATH','STREET')
suffixes['PIKE']= ('PIKE','PIKE','STREET')
suffixes['PIKES']= ('PIKE','PIKE','STREET')
suffixes['PINE']= ('PNE','PINE','STREET')
suffixes['PINES']= ('PNES','PINES','STREET')
suffixes['PNES']= ('PNES','PINES','STREET')
suffixes['PL']= ('PL','PLACE','STREET')
suffixes['PLAIN']= ('PLN','PLAIN','STREET')
suffixes['PLN']= ('PLN','PLAIN','STREET')
suffixes['PLAINS']= ('PLNS','PLAINS','STREET')
suffixes['PLNS']= ('PLNS','PLAINS','STREET')
suffixes['PLAZA']= ('PLZ','PLAZA','STREET')
suffixes['PLZ']= ('PLZ','PLAZA','STREET')
suffixes['PLZA']= ('PLZ','PLAZA','STREET')
suffixes['POINT']= ('PT','POINT','STREET')
suffixes['PT']= ('PT','POINT','STREET')
suffixes['POINTS']= ('PTS','POINTS','STREET')
suffixes['PTS']= ('PTS','POINTS','STREET')
suffixes['PORT']= ('PRT','PORT','STREET')
suffixes['PRT']= ('PRT','PORT','STREET')
suffixes['PORTS']= ('PRTS','PORTS','STREET')
suffixes['PRTS']= ('PRTS','PORTS','STREET')
suffixes['PR']= ('PR','PRAIRIE','STREET')
suffixes['PRAIRIE']= ('PR','PRAIRIE','STREET')
suffixes['PRR']= ('PR','PRAIRIE','STREET')
suffixes['RAD']= ('RADL','RADIAL','STREET')
suffixes['RADIAL']= ('RADL','RADIAL','STREET')
suffixes['RADIEL']= ('RADL','RADIAL','STREET')
suffixes['RADL']= ('RADL','RADIAL','STREET')
suffixes['RAMP']= ('RAMP','RAMP','STREET')
suffixes['RANCH']= ('RNCH','RANCH','STREET')
suffixes['RANCHES']= ('RNCH','RANCH','STREET')
suffixes['RNCH']= ('RNCH','RANCH','STREET')
suffixes['RNCHS']= ('RNCH','RANCH','STREET')
suffixes['RAPID']= ('RPD','RAPID','STREET')
suffixes['RPD']= ('RPD','RAPID','STREET')
suffixes['RAPIDS']= ('RPDS','RAPIDS','STREET')
suffixes['RPDS']= ('RPDS','RAPIDS','STREET')
suffixes['REST']= ('RST','REST','STREET')
suffixes['RST']= ('RST','REST','STREET')
suffixes['RDG']= ('RDG','RIDGE','STREET')
suffixes['RDGE']= ('RDG','RIDGE','STREET')
suffixes['RIDGE']= ('RDG','RIDGE','STREET')
suffixes['RDGS']= ('RDGS','RIDGES','STREET')
suffixes['RIDGES']= ('RDGS','RIDGES','STREET')
suffixes['RIV']= ('RIV','RIVER','STREET')
suffixes['RIVER']= ('RIV','RIVER','STREET')
suffixes['RVR']= ('RIV','RIVER','STREET')
suffixes['RIVR']= ('RIV','RIVER','STREET')
suffixes['RD']= ('RD','ROAD','STREET')
suffixes['ROAD']= ('RD','ROAD','STREET')
suffixes['ROADS']= ('RDS','ROADS','STREET')
suffixes['RDS']= ('RDS','ROADS','STREET')
suffixes['ROUTE']= ('RTE','ROUTE','STREET')
suffixes['ROW']= ('ROW','ROW','STREET')
suffixes['RUE']= ('RUE','RUE','STREET')
suffixes['RUN']= ('RUN','RUN','STREET')
suffixes['SHL']= ('SHL','SHOAL','STREET')
suffixes['SHOAL']= ('SHL','SHOAL','STREET')
suffixes['SHLS']= ('SHLS','SHOALS','STREET')
suffixes['SHOALS']= ('SHLS','SHOALS','STREET')
suffixes['SHOAR']= ('SHR','SHORE','STREET')
suffixes['SHORE']= ('SHR','SHORE','STREET')
suffixes['SHR']= ('SHR','SHORE','STREET')
suffixes['SHOARS']= ('SHRS','SHORES','STREET')
suffixes['SHORES']= ('SHRS','SHORES','STREET')
suffixes['SHRS']= ('SHRS','SHORES','STREET')
suffixes['SKYWAY']= ('SKWY','SKYWAY','STREET')
suffixes['SPG']= ('SPG','SPRING','STREET')
suffixes['SPNG']= ('SPG','SPRING','STREET')
suffixes['SPRING']= ('SPG','SPRING','STREET')
suffixes['SPRNG']= ('SPG','SPRING','STREET')
suffixes['SPGS']= ('SPGS','SPRINGS','STREET')
suffixes['SPNGS']= ('SPGS','SPRINGS','STREET')
suffixes['SPRINGS']= ('SPGS','SPRINGS','STREET')
suffixes['SPRNGS']= ('SPGS','SPRINGS','STREET')
suffixes['SPUR']= ('SPUR','SPUR','STREET')
suffixes['SPURS']= ('SPUR','SPURS','STREET')
suffixes['SQ']= ('SQ','SQUARE','STREET')
suffixes['SQR']= ('SQ','SQUARE','STREET')
suffixes['SQRE']= ('SQ','SQUARE','STREET')
suffixes['SQU']= ('SQ','SQUARE','STREET')
suffixes['SQUARE']= ('SQ','SQUARE','STREET')
suffixes['SQRS']= ('SQS','SQUARES','STREET')
suffixes['SQUARES']= ('SQS','SQUARES','STREET')
suffixes['STA']= ('STA','STATION','STREET')
suffixes['STATION']= ('STA','STATION','STREET')
suffixes['STATN']= ('STA','STATION','STREET')
suffixes['STN']= ('STA','STATION','STREET')
suffixes['STRA']= ('STRA','STRAVENUE','STREET')
suffixes['STRAV']= ('STRA','STRAVENUE','STREET')
suffixes['STRAVEN']= ('STRA','STRAVENUE','STREET')
suffixes['STRAVENUE']= ('STRA','STRAVENUE','STREET')
suffixes['STRAVN']= ('STRA','STRAVENUE','STREET')
suffixes['STRVN']= ('STRA','STRAVENUE','STREET')
suffixes['STRVNUE']= ('STRA','STRAVENUE','STREET')
suffixes['STREAM']= ('STRM','STREAM','STREET')
suffixes['STREME']= ('STRM','STREAM','STREET')
suffixes['STRM']= ('STRM','STREAM','STREET')
suffixes['STREET']= ('ST','STREET','STREET')
suffixes['STRT']= ('ST','STREET','STREET')
suffixes['ST']= ('ST','STREET','STREET')
suffixes['STR']= ('ST','STREET','STREET')
suffixes['STREETS']= ('STS','STREETS','STREET')
suffixes['SMT']= ('SMT','SUMMIT','STREET')
suffixes['SUMIT']= ('SMT','SUMMIT','STREET')
suffixes['SUMITT']= ('SMT','SUMMIT','STREET')
suffixes['SUMMIT']= ('SMT','SUMMIT','STREET')
suffixes['TER']= ('TER','TERRACE','STREET')
suffixes['TERR']= ('TER','TERRACE','STREET')
suffixes['TERRACE']= ('TER','TERRACE','STREET')
suffixes['THROUGHWAY']= ('TRWY','THROUGHWAY','STREET')
suffixes['TRACE']= ('TRCE','TRACE','STREET')
suffixes['TRACES']= ('TRCE','TRACE','STREET')
suffixes['TRCE']= ('TRCE','TRACE','STREET')
suffixes['TRACK']= ('TRAK','TRACK','STREET')
suffixes['TRACKS']= ('TRAK','TRACK','STREET')
suffixes['TRAK']= ('TRAK','TRACK','STREET')
suffixes['TRK']= ('TRAK','TRACK','STREET')
suffixes['TRKS']= ('TRAK','TRACK','STREET')
suffixes['TRAFFICWAY']= ('TRFY','TRAFFICWAY','STREET')
suffixes['TRAIL']= ('TRL','TRAIL','STREET')
suffixes['TRAILS']= ('TRL','TRAIL','STREET')
suffixes['TRL']= ('TRL','TRAIL','STREET')
suffixes['TRLS']= ('TRL','TRAIL','STREET')
suffixes['TRAILER']= ('TRLR','TRAILER','STREET')
suffixes['TRLR']= ('TRLR','TRAILER','STREET')
suffixes['TRLRS']= ('TRLR','TRAILER','STREET')
suffixes['TUNEL']= ('TUNL','TUNNEL','STREET')
suffixes['TUNL']= ('TUNL','TUNNEL','STREET')
suffixes['TUNLS']= ('TUNL','TUNNEL','STREET')
suffixes['TUNNEL']= ('TUNL','TUNNEL','STREET')
suffixes['TUNNELS']= ('TUNL','TUNNEL','STREET')
suffixes['TUNNL']= ('TUNL','TUNNEL','STREET')
suffixes['TRNPK']= ('TPKE','TURNPIKE','STREET')
suffixes['TURNPIKE']= ('TPKE','TURNPIKE','STREET')
suffixes['TURNPK']= ('TPKE','TURNPIKE','STREET')
suffixes['UNDERPASS']= ('UPAS','UNDERPASS','STREET')
suffixes['UN']= ('UN','UNION','STREET')
suffixes['UNION']= ('UN','UNION','STREET')
suffixes['UNIONS']= ('UNS','UNIONS','STREET')
suffixes['VALLEY']= ('VLY','VALLEY','STREET')
suffixes['VALLY']= ('VLY','VALLEY','STREET')
suffixes['VLLY']= ('VLY','VALLEY','STREET')
suffixes['VLY']= ('VLY','VALLEY','STREET')
suffixes['VALLEYS']= ('VLYS','VALLEYS','STREET')
suffixes['VLYS']= ('VLYS','VALLEYS','STREET')
suffixes['VDCT']= ('VIA','VIADUCT','STREET')
suffixes['VIA']= ('VIA','VIADUCT','STREET')
suffixes['VIADCT']= ('VIA','VIADUCT','STREET')
suffixes['VIADUCT']= ('VIA','VIADUCT','STREET')
suffixes['VIEW']= ('VW','VIEW','STREET')
suffixes['VW']= ('VW','VIEW','STREET')
suffixes['VIEWS']= ('VWS','VIEWS','STREET')
suffixes['VWS']= ('VWS','VIEWS','STREET')
suffixes['VILL']= ('VLG','VILLAGE','STREET')
suffixes['VILLAG']= ('VLG','VILLAGE','STREET')
suffixes['VILLAGE']= ('VLG','VILLAGE','STREET')
suffixes['VILLG']= ('VLG','VILLAGE','STREET')
suffixes['VILLIAGE']= ('VLG','VILLAGE','STREET')
suffixes['VLG']= ('VLG','VILLAGE','STREET')
suffixes['VILLAGES']= ('VLGS','VILLAGES','STREET')
suffixes['VLGS']= ('VLGS','VILLAGES','STREET')
suffixes['VILLE']= ('VL','VILLE','STREET')
suffixes['VL']= ('VL','VILLE','STREET')
suffixes['VIS']= ('VIS','VISTA','STREET')
suffixes['VIST']= ('VIS','VISTA','STREET')
suffixes['VISTA']= ('VIS','VISTA','STREET')
suffixes['VST']= ('VIS','VISTA','STREET')
suffixes['VSTA']= ('VIS','VISTA','STREET')
suffixes['WALK']= ('WALK','WALK','STREET')
suffixes['WALKS']= ('WALK','WALKS','STREET')
suffixes['WALL']= ('WALL','WALL','STREET')
suffixes['WY']= ('WAY','WAY','STREET')
suffixes['WAY']= ('WAY','WAY','STREET')
suffixes['WAYS']= ('WAYS','WAYS','STREET')
suffixes['WELL']= ('WL','WELL','STREET')
suffixes['WELLS']= ('WLS','WELLS','STREET')
suffixes['WLS']= ('WLS','WELLS','STREET')

prefixes = {};
prefixes['APT']= ('Apartment','APT','SECONDARY UNIT')
prefixes['BSMT']= ('Basement','BSMT','SECONDARY UNIT')
prefixes['BLDG']= ('Building','BLDG','SECONDARY UNIT')
prefixes['DEPT']= ('Department','DEPT','SECONDARY UNIT')
prefixes['FL']= ('Floor','FL','SECONDARY UNIT')
prefixes['FRNT']= ('Front','FRNT','SECONDARY UNIT')
prefixes['HNGR']= ('Hanger','HNGR','SECONDARY UNIT')
prefixes['KEY']= ('Key','KEY','SECONDARY UNIT')
prefixes['LBBY']= ('Lobby','LBBY','SECONDARY UNIT')
prefixes['LOT']= ('Lot','LOT','SECONDARY UNIT')
prefixes['LOWR']= ('Lower','LOWR','SECONDARY UNIT')
prefixes['OFC']= ('Office','OFC','SECONDARY UNIT')
prefixes['PH']= ('Penthouse','PH','SECONDARY UNIT')
prefixes['PIER']= ('Pier','PIER','SECONDARY UNIT')
prefixes['REAR']= ('Rear','REAR','SECONDARY UNIT')
prefixes['RM']= ('Room','RM','SECONDARY UNIT')
prefixes['SIDE']= ('Side','SIDE','SECONDARY UNIT')
prefixes['SLIP']= ('Slip','SLIP','SECONDARY UNIT')
prefixes['SPC']= ('Space','SPC','SECONDARY UNIT')
prefixes['STOP']= ('Stop','STOP','SECONDARY UNIT')
prefixes['STE']= ('Suite','STE','SECONDARY UNIT')
prefixes['SUITE']= ('Suite','STE','SECONDARY UNIT')
prefixes['TRLR']= ('Trailer','TRLR','SECONDARY UNIT')
prefixes['UNIT']= ('Unit','UNIT','SECONDARY UNIT')
prefixes['UPPR']= ('Upper','UPPR','SECONDARY UNIT')
#prefixes['BOX']= ('PO BOX','PO BOX','SECONDARY UNIT')

qualifiers = {}
qualifiers['N']= ('North','N','GEOGRAPHIC DIRECTIONAL')
qualifiers['E']= ('East','E','GEOGRAPHIC DIRECTIONAL')
qualifiers['S']= ('South','S','GEOGRAPHIC DIRECTIONAL')
qualifiers['W']= ('West','W','GEOGRAPHIC DIRECTIONAL')
qualifiers['NE']= ('Northeast','NE','GEOGRAPHIC DIRECTIONAL')
qualifiers['SE']= ('Southeast','SE','GEOGRAPHIC DIRECTIONAL')
qualifiers['NW']= ('Northwest','NW','GEOGRAPHIC DIRECTIONAL')
qualifiers['SW']= ('Southwest','SW','GEOGRAPHIC DIRECTIONAL')


class Address:
    def __init__(self, a1, a2, c, s, z, row='US', msg=''):
        self.msg = msg.upper();
        self.addr1 = a1.strip().upper();
        self.addr2 = a2.strip().upper();
        self.city = c.strip().upper();
        self.state = s.strip().upper();
        self.nation = row.strip().upper();
        z = z.strip().upper();
        if len(z) >=5 :
            self.zip5 = z[0:5];
            self.zip4 = z[5:];
        else :
            self.zip5 = z;
            self.zip4 = ''
        self.zip4 = self.zip4.strip(' -');
        if len(self.zip5) < 5:
            self.zip5 = '{:0<5s}'.format(self.zip5);
        if len(self.zip4) < 4:
            self.zip4 = '{:0<4s}'.format(self.zip4);
            
    def __eq__(self, other):
        if other == None:
            return False;
        if not isinstance(other, Address) :
            return False
        if self.nation != other.nation :
            return False
        if self.city == other.city and self.state == other.state and self.zip5 == other.zip5 :
            return (self.addr1 == other.addr1 and self.addr2 == other.addr2) or (self.addr1 == other.addr2 and self.addr2 == other.addr1) 
        else :
            return False
    
    def tokeystr(self, usezip4=False):
        tranmap = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        keylist = [self.state, self.zip5] + self.city.split()
        if usezip4 :
            keylist.append(self.zip4)
        keylist += self.addr1.translate(tranmap).split()
        keylist += self.addr2.translate(tranmap).split()

        keylist.sort();
        return ' '.join(keylist)
        
    def __str__(self) :
        out = [self.addr1, self.addr2, self.city, self.state, self.zip5, self.zip4]
        if len(self.msg) > 0 :
            out.append(self.msg);
        return ','.join(out);
    
    def getSortStr(self):
        return ','.join((self.zip5, self.zip4, self.state, self.city, self.addr1, self.addr2)) ;
    
    def isEmpty(self):
        if len((self.addr1 + self.addr2).strip()) > 0 : 
            return False
        else :
            return True
        
    def isForeign(self):
        if self.nation == 'USA' :
            return False
        if len(self.state) == 2 : 
            return False
        else :
            return True;
        
    def isPOBox(self):
        addr = self.addr1 + " " + self.addr2;
        if addr.find('BOX') >= 0 and addr.find('PO') >= 0:
            return True;
        else :
            return False;
        

class AddressLexical:

    def __init__(self, addr1, addr2 = '', addr3 = ''):
        
        self.primary = [ ];
        self.secondary = [ ];
        self.addr1 = addr1;
        self.addr2 = addr2;
        self.addr3 = addr3;
        address = " ".join((addr1, addr2, addr3));
        words = address.split();
        
        lex = [];
        for w in words :
            w = w.strip('.,').upper();
            if w == '' :
                lex.append('B');
                continue;
            if w in list(prefixes.keys()) :
                lex.append('P');
                continue;
            if w in list(suffixes.keys()) :
                lex.append('S');
                continue;
            if w in list(qualifiers.keys()) :
                lex.append('Q');
                continue;
            lex.append('-');
        #print address
        #print lex
            
        # find index of last prefix from left, 
        index1 = 0;
        index2 = len(words);
        for i, posw in enumerate(lex) :
            if posw != 'P' :
                index1 = i;
                break;
        #find index of first prefix or last suffix from right
        lex.reverse();
        for i, posw in enumerate(lex) :
            if i >= len(words) - index1 : 
                break;
            if posw == 'S' :
                index2 = len(words) - i;
                break;
            if posw == 'P' :
                index2 = len(words) - i - 1;
                continue;
        
        # split first level address from second level address
        if index1 > 0:
            index1 += 1;
            self.secondary.append(' '.join(words[0:index1]));
        if index2 < len(words) :
            self.secondary.append(' '.join(words[index2:]));
        #print index1, index2
        self.primary.append(' '.join(words[index1:index2]));
        
    def __str__(self):
        return self.primary[0] + "|" + ' '.join(self.secondary);
    
    def replaceAbbr(self):
        a = '';
        for p in self.primary:
            if len(p.strip()) == 0 :
                continue;
            w = p.split()[-1]
            #print 'pri w' + w
            if w in list(suffixes.keys()):
                #print 'pri w', w, suffixes[w][0]
                p = p.replace(w, suffixes[w][0]);
            a += ' ' + p
        self.addr1 = a.strip();
        a = '';
        for p in self.secondary:
            if len(p.strip()) == 0 :
                continue;
            w = p.split()[0]
            #print 'sec w' + w
            if w in list(prefixes.keys()):
                #print 'sec w', w, prefixes[w][1]
                p = p.replace(w, prefixes[w][1]);
            a += ' ' + p
        self.addr2 = a.strip();
        
class Distance:

    def __init__(self, a1, a2):
        if a1 == None or a2 == None :
            return [0, 0, 0, 0, 0, 0, 0]
        self.a1d = fuzz.ratio(a1.addr1, a2.addr1);
        self.a2d = fuzz.ratio(a1.addr2, a2.addr2);
        #self.ad = fuzz.token_set_ratio(a1.addr1 + ' ' + a1.addr2, a2.addr1 + ' ' + a2.addr2);
        a1line = a1.addr1 + ' ' + a1.addr2;
        a2line = a2.addr1 + ' ' + a2.addr2
        if (a1.isPOBox() and a2.isPOBox()):
            a1line = stripPOBox(a1line.replace('BOX', '').replace('PO', ''))
            a2line = stripPOBox(a2line.replace('BOX', '').replace('PO', ''))
            self.ad = fuzz.ratio(a1line, a2line);
        elif (a1.isPOBox() or a2.isPOBox()):
            self.ad = 0
        else :
            self.ad = fuzz.token_set_ratio(a1line, a2line);
            
        self.cd = fuzz.ratio(a1.city, a2.city)
        self.sd = fuzz.ratio(a1.state, a2.state)
        if a1.zip5 == '0000' or a2.zip5 == '0000' :
            self.z5d = 90;
        else :
            self.z5d = fuzz.ratio(a1.zip5, a2.zip5);
        if a1.zip4 == '0000' or a2.zip4 == '0000' :
            self.z4d = 90;
        else :
            self.z4d = fuzz.ratio(a1.zip4, a2.zip4);
    def detail(self):
        return [self.ad, self.a2d, self.a1d, self.cd, self.sd, self.z5d, self.z4d];
    
    def isMatched(self):
        if self.sd < 100 :
            return False;
        # LOCKBOX 951326 vs PO BOX 951326 = 74, so set ad = 70; it means 1/5, 2/7, 3/10
        if self.z5d == 100 and self.cd == 100 and self.ad >= 75 :
            return True
        elif self.z5d >= 80 and self.cd == 100 and self.ad > 90 :
            return True;
        elif self.z5d == 100 and self.cd >= 90 and self.ad >= 90 :
            return True;
        else :
            return False
        
def stripPOBox(line):
    a1line = line.replace('BOX', '').replace('PO', '')
    a1line = ' '.join(a1line.split())
    return a1line;
