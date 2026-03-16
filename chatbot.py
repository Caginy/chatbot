import json
import torch
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai

class AsistanBeyni:
    def __init__(self):
        # 1. Yerel NLP Modeli (JSON eşleştirme için)
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # 2. Gemini API Kurulumu (Kendi anahtarını buraya yapıştır!)
        self.api_key = "SENIN_API_ANAHTARIN_BURAYA"
        genai.configure(api_key=self.api_key)
        self.gemini = genai.GenerativeModel('gemini-1.5-flash')
        
        self.hafiza = {}
        self.veriyi_yukle()

    def veriyi_yukle(self):
        with open('diyalog_veri.json', 'r', encoding='utf-8') as f:
            self.diyaloglar = json.load(f)
        self.sorular = [d['soru'] for d in self.diyaloglar]
        self.soru_embeddings = self.model.encode(self.sorular, convert_to_tensor=True)

    def cevap_ver(self, kullanici_mesaji):
        # A. Önce JSON'da özel bir cevap var mı bak?
        kullanici_embedding = self.model.encode(kullanici_mesaji, convert_to_tensor=True)
        skorlar = util.cos_sim(kullanici_embedding, self.soru_embeddings)[0]
        en_iyi_index = torch.argmax(skorlar).item()

        if skorlar[en_iyi_index] > 0.7: # Eğer çok benzer bir soru bulursa JSON'dan ver
            return self.diyaloglar[en_iyi_index]['cevap']

        # B. JSON'da yoksa internete (Gemini) sor
        try:
            response = self.gemini.generate_content(kullanici_mesaji)
            return response.text
        except Exception as e:
            return "İnternete bağlanırken bir sorun oluştu, ama Cagin üzerinde çalışıyor!"