from google import genai
import yaml


# --------------------------------------------------------------------------------------------------------------------------------------------------------
client = genai.Client(api_key="AIzaSyDwvuCyPhns9VcI_hHohWYoFEsiHFVQXgA")


# --------------------------------------------------------------------------------------------------------------------------------------------------------
def get_prompt(path: str):
    with open(path, "r") as file:
        data = yaml.safe_load(file)
    return data

def get_answer(message: str, music):
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[message, music]
    )
    return response.text

# --------------------------------------------------------------------------------------------------------------------------------------------------------
class MusicPiece:
    prompts = get_prompt("prompts/MusicPiece.yml")

    def __init__(self, file_path: str):
        self.file = client.files.upload(file=file_path)
    
    def get_metadata(self) -> list:
        return get_answer(self.prompts["get_metadata"] , self.file).split("||")

class MusicTheoryAnalyzer:
    prompts = get_prompt("prompts/MusicTheoryAnalyzer.yml")

    def __init__(self, music: MusicPiece):
        self.music = music

    def detect_key(self) -> list:
        return get_answer(self.prompts["detect_key"] , self.music.file).split("||")
    
    def detect_chords(self) -> str:
        return get_answer(self.prompts["detect_chords"] , self.music.file)

    def detect_scales(self) -> str:
        return get_answer(self.prompts["detect_scales"] , self.music.file)

    def detect_cadences(self) -> str:
        return get_answer(self.prompts["detect_cadences"] , self.music.file)
    
class AiAnalyzer:
    def __init__(self, music: MusicPiece):
        self.music = music

    def summery(self) -> str:
        return get_answer("give me a summery of this piece of music" , self.music.file)
    
    def genere(self) -> str:
        return get_answer("give me genre of this music. only respond in one word" , self.music.file)
    
    def give_suggestions(self) -> str:
        return get_answer("give me suggestion on how i can improve this piece of music" , self.music.file)
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    music = MusicPiece("media/sample.mp3")
    metadata = music.get_metadata()
    print("\nMetadata:", metadata)

    mt = MusicTheoryAnalyzer(music)
    key = mt.detect_key()
    chords = mt.detect_chords()
    scales = mt.detect_scales()
    cadences = mt.detect_cadences()
    print("\nDetected Key:", key)
    print("\nChord Progressions:", chords)
    print("\nScales Identified:", scales)
    print("\nCadences Detected:", cadences)

    aia = AiAnalyzer(music)
    print("\nsummery:\n",aia.summery())
    print("\ngenere:\n",aia.genere())
    print("\nsuggestions:\n",aia.give_suggestions())
