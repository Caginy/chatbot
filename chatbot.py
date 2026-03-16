import json
import torch
import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util
import streamlit as st

class AsistanBeyni:
    def __init__(self):
        # 1. Yerel NLP Modeli
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # 2. Gemini API Kurulumu (Secrets'tan güvenli bir şekilde alıyoruz)
        try:
            self.api_key = st.secrets["GEMINI_API_KEY"]
        except:
            self.api_key = "AIzaSyC4VjssfY4gucT3FlHDKhYbQu0MgJoOMy0" # Eğer Secrets kullanmıyorsan buraya yaz
            
        genai.configure(api_key=self.api_key)
        self.gemini = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        self.hafiza = {}
        self.veriyi_yukle()

    def veriyi_yukle(self):
        try:
            with open('diyalog_veri.json', 'r', encoding='utf-8') as f:
                self.diyaloglar = json.load(f)
            
            # Eğer JSON boş değilse soruları hazırla
            if self.diyaloglar and len(self.diyaloglar) > 0:
                self.sorular = [d['soru'] for d in self.diyaloglar]
                self.soru_embeddings = self.model.encode(self.sorular, convert_to_tensor=True)
            else:
                self.sorular = []
                self.soru_embeddings = None
        except Exception as e:
            st.warning(f"JSON verisi yüklenemedi veya boş: {e}")
            self.sorular = []
            self.soru_embeddings = None

    def cevap_ver(self, kullanici_mesaji):
        # A. JSON'da özel bir cevap var mı?
        if self.soru_embeddings is not None and len(self.sorular) > 0:
            kullanici_embedding = self.model.encode(kullanici_mesaji, convert_to_tensor=True)
            skorlar = util.cos_sim(kullanici_embedding, self.soru_embeddings)[0]
            en_iyi_index = torch.argmax(skorlar).item()

            if skorlar[en_iyi_index] > 0.7:
                return self.diyaloglar[en_iyi_index]['cevap']

        # B. JSON'da yoksa Gemini'ye sor
        try:
            response = self.gemini.generate_content(kullanici_mesaji)
            return response.text
        except Exception as e:
            return f"Üzgünüm, bir hata oluştu: {e}"
