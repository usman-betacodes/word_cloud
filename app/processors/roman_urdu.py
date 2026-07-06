from typing import List

from app.core.roman_normalize import normalize_roman

ROMAN_STOP_WORDS = {
  "hai", "hain", "han", "tha", "thi", "the", "hoga", "hogi", "honge",
  "hon", "hoon", "hota", "hoti", "hote", "ho", "hua", "hui", "hue",
  "hona", "hone", "hokar", "hoke",
  "main", "mein", "hum", "tum", "aap", "ye", "yeh", "wo", "woh",
  "is", "us", "un", "unhein", "unhe", "inhen", "jis", "jise",
  "jiska", "jiski", "jiske", "kaun", "kon", "kaunsa", "kaunsi",
  "kis", "kisne", "kisko",
  "ko", "ka", "ki", "ke", "se", "par", "tak", "liye", "keliye",
  "waste", "vaste", "taraf", "andar", "bahar", "upar", "neeche",
  "aur", "ya", "lekin", "magar", "balki", "kyunke", "kyunki",
  "chunanche", "agar", "to", "phir", "warna", "jab", "jabke",
  "isliye", "lehaza",
  "kya", "kyun", "kyu", "kab", "kahan", "kidhar", "kaise",
  "ji", "haan", "nahi", "nahin", "na", "ne",
  "theek", "theekhai", "ok", "okay",
  "yar", "yaar", "bhai", "bhaii", "dekho", "suno", "matlab",
  "yani", "bas", "sirf", "zara", "chalo",
  "ab", "tab", "abhi", "kabhi", "hamesha", "aksar", "pehle",
  "baad", "kal", "aaj", "parson", "foran",
  "oh", "oho", "wah", "are", "achaacha", "theektheek",
  "kiabaat", "chalien", "chalen",
  "ao", "aao", "jao", "karo", "karlo", "dekhona", "sunona", "chalona",
  "hi", "bhi",
  "ek", "aik", "keh", "jo", "apne", "apni",
  "ga", "ge", "gi", "diya", "di", "liya",
  "saath", "doran", "khilaf", "mutabiq",
  "zariye", "zariyey", "ilawa", "bais", "wajah",
  "b", "c", "d", "ch", "p",
  "dar", "ani", "naib", "abad",
  "j", "a", "awam", "hal",
}


class RomanUrduProcessor:
  def extract_terms(self, tokens: List[str]) -> List[str]:
    valid: List[str] = []
    for token in tokens:
      normalized = normalize_roman(token)
      if normalized in ROMAN_STOP_WORDS:
        continue
      valid.append(normalized)
    return valid
