from google.cloud import texttospeech
from googletrans import Translator

class TestGoogleTTS:
    LANGUAGE_CODE_MAP = {
        "en": "en-US",
        "ch": "zh-TW"
    }
    
    _instance = None
    _tts_client = None
    _translator = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._tts_client = texttospeech.TextToSpeechClient()
            cls._translator = Translator()
            
        return cls._instance
    
    @property
    def client(self):
        return self._tts_client
    
    @property
    def translator(self):
        return self._translator
        
    @property
    def tts_supported_languages(self):
        """
        Returns:
            google.cloud.texttospeech_v1.types.cloud_tts.ListVoicesResponse: 支援語音資訊
        """
        
        return self.client.list_voices()
    
    def translate_text(self, target_text:str, output_language:str='en'):
        primitive_language = self.translator.detect(target_text).lang
        
        result = self.translator.translate(target_text, dest=output_language).text
        return primitive_language, result
    
    def text_to_speech(self, text:str, output_language:str='en') -> None:
        prmitive_language, translate_text = self.translate_text(text, output_language)
        
        client = texttospeech.TextToSpeechClient()        
        
        # language_code: 要使用的語音語言, ssml_gender: 語音的性別
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.LANGUAGE_CODE_MAP.get(output_language, "en-US"), 
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        
        # 選擇一個語音
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # 定義要進行語音合成的文字, 不先翻譯會直接音翻
        input_text = texttospeech.SynthesisInput(text=translate_text)
        
        # 進行語音合成主要的三個部分 1.文本輸入 2.聲音 3.音頻
        response = client.synthesize_speech(
            request={
                "input": input_text,
                "voice": voice,
                "audio_config": audio_config
            }
        )

        # 將音頻保存為文件
        with open("output.mp3", "wb") as out:
            out.write(response.audio_content)

        return "output.mp3"


test_obj = TestGoogleTTS()
test_obj.text_to_speech("你好！我的名字是丁禹!")
