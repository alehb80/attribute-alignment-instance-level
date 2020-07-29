

ENTITY_FILE_PATH = "dirty_entity_resolution_pictureme.xlsx"
BASE_SOURCE_DIR = "sources"
BASE_CL_SOURCE_DIR = "sources_cl"
PHASE_1_SOURCE_DIR = "sources_1"
PHASE_1_CL_SOURCE_DIR = "sources_1_cl"
PHASE_2_SOURCE_DIR = "sources_2"
PHASE_2_CL_SOURCE_DIR = "sources_2_cl"

###Fase 0
SOURCES_BASE_LK_DICT = "json/00_lk_dictionary_path.json"
SOURCES_BASE_EXT_DICT = "json/00_ext_dictionary_path.json"
SOURCES_BASE_CM_DICT = "json/00_common_dictionary_path.json"

DROPPED_ATTRIBUTES_FILES = "json/01_dropped_attributes.json"
COMPOSITE_ATTRIBUTES_FILES = "json/01_composite_attributes.json"

COLLISION_DICTIONARY_DICT = "json/02_collision_dictionary.json"
COLLISION_DICTIONARY_INV_DICT = "json/02_collision_dictionary_inv.json"
COLLISION_DICTIONARY_SIM_DICT = "json/02_collision_dictionary_sim.json"

COLLISION_DICTIONARY_SIM_DYN_DICT_01 = "json/02_collision_dictionary_sim_din_01.json"
COLLISION_DICTIONARY_SIM_DYN_DICT_02 = "json/02_collision_dictionary_sim_din_02.json"

###Fase 1
SOURCES_PHASE_1_LK_DICT = "json/10_lk_dictionary_path.json"

###Fase 2 
SOURCES_PHASE_2_LK_DICT = "json/20_lk_dictionary_path.json"

###Fase 3
PHASE_3_SOURCE_DIR = "sources_3"
PHASE_3_CL_SOURCE_DIR = "sources_3_cl"


BAD_WORDS_KEY = ["an", "of", "with", "for"]
BAD_WORDS_VALUES = set([ "n", "unknown", "included", "support", "built", "optional", "manual",  "available", "how", "to", "at", "a", "or", "and", "by", "off", "an", "in", "na", "none", "n" "/", "if", "\n", "yes", "no", "on", "auto", "built-in", "for", "of", "with", 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]) 