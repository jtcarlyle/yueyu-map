import re
import pandas as pd

df = pd.read_csv("cy_lex_77.csv", encoding='utf8')
df = df[["gloss_en", "dialect", "transcription"]]
df["gloss_en"] = df["gloss_en"].str.replace(r"\s", "_")

#sanitization tweaks
df.transcription = df.transcription.str.replace(r'e(ŋ|k)', r'i\1', regex=True)
df.transcription = df.transcription.str.replace(r'o(ŋ|k)', r'u\1', regex=True)
df.transcription = df.transcription.str.replace(r'(^|\s)j?i([aɐəeɛɔuyœøɪʏ])', r'\1j\2', regex=True)
df.transcription = df.transcription.str.replace(r'(^|\s)w?u([aɐəeɛɔuyœøɪʏ])', r'\1w\2', regex=True)
df.transcription = df.transcription.str.replace(r'(^|\s)ii?', r'\1ji', regex=True)
df.transcription = df.transcription.str.replace(r'(^|\s)uu?', r'\1wu', regex=True)
df.transcription = df.transcription.str.replace(r'(^|\s)ʔ', r'\1', regex=True)
df.transcription = df.transcription.str.replace(r'niɐ', r'ȵiɐ', regex=True)
df.transcription = df.transcription.str.replace(r'ǝ', r'ə', regex=True)
df.transcription = df.transcription.str.replace(r'ᵉ', r'e', regex=True)
df.transcription = df.transcription.str.replace(r'ʷʰ', r'ʰʷ', regex=True)
df.transcription = df.transcription.str.replace(r'ʷ|ᵘ', r'u', regex=True)
df.transcription = df.transcription.str.replace(r'ʃ|ʂ|ɕ', r's', regex=True) # not phonemic
df.transcription = df.transcription.str.replace(r'(.)$', r'\1.', regex=True)

df["transcription"] = df["transcription"].str.replace(r"\s", ".")
# print(df[df["transcription"].map(type) == float])
df = df.dropna(subset=["transcription"])
df = df.groupby(["gloss_en", "dialect"]).agg({"transcription" : lambda x : " / ".join(x)}).reset_index()
df = df.pivot(index='dialect', columns='gloss_en', values='transcription')

chao_dict = {
    "¹" : "1",
    "²" : "2",
    "³" : "3",
    "⁴" : "4",
    "⁵" : "5"
}

tone_dict = {
    # HTR
    # HBR
    r"33[4-5]|445" : "HBR",
    # HTF
    r"55[1-4]" : "HTF",
    # HBF
    r"44[1-3]" : "HBF",
    # HRT
    r"[3-4]55" : "HRT",
    # HRB
    r"344" :"HRB",
    # HFT
    # HFB
    r"533|544|433" : "HFB",
    # HRF
    r"343|342|341|353|354|352|351|453|454|452|451" : "HRF", 
    # HFR
    r"414|412|413|414|415|424|423|425|434|435|515|512|513|514|525|523|524|535|534" : "HFR",
    # LTR
    r"22[3-5]" : "LTR",
    # LBR
    r"11[1-5]" : "LBR",
    # LTF
    r"221" : "LTF",
    # LBF
    # LRT
    r"[1-2]33|122" : "LRT",
    # LRB
    # LFT
    r"322" : "LFT",
    # LFB
    r"311|211" : "LFB",
    # LFR
    r"313|312|314|315|323|324|325|212|213|214|215" : "LFR",
    # LRF
    r"252|253|254|251|242|241|243|232|231|121|131|132|141|142|143|151|152|153|154" : "LRF",
    # HT
    r"55" : "HT",
    # HB
    r"44|33" : "HB",
    # HR
    r"3[4-5]|45" : "HR",
    # HF
    r"5[1-4]" : "HF",
    r"4[1-3]" : "HF",
    # LT
    r"22" : "LT",
    # LB
    r"11" : "LB",
    # LR
    r"1[2-5]" : "LR",
    r"2[3-5]" : "LR",
    # LF
    r"3[1-2]|21" : "LF"
}

mtone_dict = {
    # HTR
    # HBR
    r"33[4-5]|445" : "HMR",
    # HTF
    r"55[1-4]" : "HTF",
    # HBF
    r"44[1-3]" : "HMF",
    # HRT
    r"[3-4]55" : "HRT",
    # HRB
    r"344" :"HRM",
    # HFT
    # HFB
    r"533|544|433" : "HFM",
    # HRF
    r"343|342|341|353|354|352|351|453|454|452|451" : "HRF", 
    # HFR
    r"414|412|413|414|415|424|423|425|434|435|515|512|513|514|525|523|524|535|534" : "HFR",
    # LTR
    r"22[3-5]" : "LMR",
    # LBR
    r"11[1-5]" : "LBR",
    # LTF
    r"221" : "LMF",
    # LBF
    # LRT
    r"[1-2]33|122" : "LRM",
    # LRB
    # LFT
    r"322" : "LFM",
    # LFB
    r"311|211" : "LFB",
    # LFR
    r"313|312|314|315|323|324|325|212|213|214|215" : "LFR",
    # LRF
    r"252|253|254|251|242|241|243|232|231|121|131|132|141|142|143|151|152|153|154" : "LRF",
    # HT
    r"55" : "HT",
    # HB
    r"44|33" : "HM",
    # HR
    r"3[4-5]|45" : "HR",
    # HF
    r"5[1-4]" : "HF",
    r"4[1-3]" : "HF",
    # LT
    r"22" : "LM",
    # LB
    r"11" : "LB",
    # LR
    r"1[2-5]" : "LR",
    r"2[3-5]" : "LR",
    # LF
    r"3[1-2]|21" : "LF"
}

df.to_csv("yue-string-data.txt", encoding="utf8", sep="\t", index_label=False)
with open("yue-string-data.txt", "r+") as f:
    data = f.read()
    for k,v in chao_dict.items():
        data = re.sub(k, v, data)
    for k,v in tone_dict.items():
        data = re.sub(k, v, data)
    f.seek(0)
    f.truncate()
    f.write(data)

df = pd.read_csv("cy_lex_77.csv", encoding='utf8')
df = df[["gloss_en", "dialect", "form"]]
df["gloss_en"] = df["gloss_en"].str.replace(r"\s", "_")
df["form"] = df["form"].str.replace(r"\s", "_")
# print(df[df["transcription"].map(type) == float])
df = df.dropna(subset=["form"])
df = df.groupby(["gloss_en", "dialect"]).agg({"form" : lambda x : " / ".join(x)}).reset_index()
df = df.pivot(index='dialect', columns='gloss_en', values='form')
df.to_csv("yue-categorical-data.txt", encoding="utf8", sep="\t", index_label=False)
