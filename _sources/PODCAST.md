# 🎧 Podcast-filer / Podcast Files

## 🇳🇴 Norsk

### Hvordan få tak i podcast-filene

Podcast-filene er ikke inkludert i Git-repositoryet på grunn av størrelse (20MB MP3, 40MB M4A). Her er hvordan du kan få tak i dem:

#### Alternativ 1: Last ned fra ekstern kilde
- [MP3 (universell kompatibilitet)](https://example.com/podcast.mp3) - 20MB
- [M4A (høy kvalitet)](https://example.com/podcast.m4a) - 40MB

#### Alternativ 2: Generer lokalt
Hvis du har kilde-filen, kan du generere begge formater:

```bash
# Konverter til MP3
ffmpeg -i kilde_fil.m4a -codec:a libmp3lame -b:a 128k podcast/Slektstre_med_Python_og_Grafteori__Slik_Analyserer_du_Din_Famil.mp3

# Eller bruk vårt konverteringsskript
python scripts/convert_audio.py kilde_fil.m4a
```

#### Alternativ 3: Bruk Jupyter Notebook
Åpne `notebooks/99_podcast_player.ipynb` for å spille av podcasten direkte i Jupyter.

## 🇬🇧 English

### How to get the podcast files

The podcast files are not included in the Git repository due to size (20MB MP3, 40MB M4A). Here's how you can get them:

#### Option 1: Download from external source
- [MP3 (universal compatibility)](https://example.com/podcast.mp3) - 20MB
- [M4A (high quality)](https://example.com/podcast.m4a) - 40MB

#### Option 2: Generate locally
If you have the source file, you can generate both formats:

```bash
# Convert to MP3
ffmpeg -i source_file.m4a -codec:a libmp3lame -b:a 128k podcast/Slektstre_med_Python_og_Grafteori__Slik_Analyserer_du_Din_Famil.mp3

# Or use our conversion script
python scripts/convert_audio.py source_file.m4a
```

#### Option 3: Use Jupyter Notebook
Open `notebooks/99_podcast_player.ipynb` to play the podcast directly in Jupyter.

## 📝 Merk / Note

**🇳🇴 Norsk:**
- Podcasten er ca. 22 minutter lang
- MP3-formatet er anbefalt for universell kompatibilitet
- M4A-formatet gir høyere lydkvalitet

**🇬🇧 English:**
- The podcast is approximately 22 minutes long
- MP3 format is recommended for universal compatibility
- M4A format provides higher audio quality
