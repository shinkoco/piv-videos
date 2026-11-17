# Partners in Vice — runbook de la tâche quotidienne

Chaîne de clips GTA 6 en français : TikTok @partnersinvicefr + YouTube « Partners in Vice | GTA 6 🌴 ».
Publication via le connecteur **Buffer** (organisation « My organization ») :
- YouTube channelId `6afa0f34ece6dfde5fd78fb8`
- TikTok channelId `6afa0f0eece6dfde5fd78eaa`
- Instagram (Reels) channelId `6afb16d7ece6dfde5fe51faf` — `metadata.instagram = {type: "reel", shouldShareToFeed: true}`,
  hashtags dans la légende (le 1er commentaire est payant sur Buffer gratuit), `thumbnailOffset` comme TikTok.

Les vidéos sont hébergées dans ce dépôt public (`clips/AAAA-MM-JJ/…mp4`), servies par
`https://raw.githubusercontent.com/shinkoco/piv-videos/main/<chemin>`.

## Règles
- Ne rien faire avant le **2026-11-19** (sortie de GTA 6) : si la date est antérieure, écrire « pas encore » dans le rapport et s'arrêter.
- Uniquement des VODs de **GTA 6 / GTA VI** (titre ou contenu). Pas d'anciens GTA.
- **Mode** (dans `tools/streamers.json`) :
  - `B` (départ) : tous les streamers de la liste.
  - `C` : seulement les campagnes Content Rewards actives + streamers qui autorisent publiquement le clipping.
  - Au premier avertissement / retrait signalé par Mathieu : passer `mode` à `C`, ajouter le streamer à `blocked`, commit.
- Toujours **créditer** le streamer dans la légende (nom + lien de sa chaîne).
- Ne jamais republier un moment déjà publié : vérifier `published.json`.
- Beaucoup de streamers FR (Squeezie, ZeratoR, Gotaga, AmineMaTué, Kameto, Locklear, Ponce, MisterMV, Domingo, JLTomy)
  ont des VODs réservées aux abonnés : pour eux, utiliser `python3 tools/clips.py LAST_DAY` (clips publics faits par
  les viewers, filtrés sur la catégorie GTA VI, triés par vues). Ces clips sont déjà des moments forts : en prendre
  3 (même streamer ou thème commun), télécharger chacun avec yt-dlp, et mettre `"src"` par moment dans le spec
  (`start` 0 / `end` = durée, `peak` = moment fort repéré à la transcription ou au volume).
- Sources possibles chaque jour : VODs (`discover.py`) ET clips (`clips.py`). Préférer les plus vus.

## Étapes (2 vidéos par jour)
1. `python3 tools/discover.py 36` → liste des VODs GTA des dernières 36 h.
2. Choisir 2 VODs (les plus vues / streamers différents si possible).
3. Pour chaque VOD :
   - Télécharger un segment de 15–30 min autour de la partie la plus active :
     `yt-dlp --download-sections "*HH:MM:SS-HH:MM:SS" -f "best[height<=720]/best" -o src.mp4 URL`
   - Twitch : `python3 tools/chat.py <id sans v> <start_s> <end_s> chat.json` → pics du chat.
     Kick : pas de chat → pics de volume audio (fenêtres de 20 s).
   - Transcrire (faster-whisper `small`, int8, audio passé en numpy float32, `language` = langue du stream, `word_timestamps=True`).
   - Choisir **3 moments** (pics), 22–26 s chacun → vidéo de 70–85 s (> 60 s obligatoire).
   - Écrire le `spec.json` : `hook` (court, percutant, FR, MAJUSCULES OK), et pour chaque moment
     `rank` (3,2,1), `start`, `end`, `peak`, `context` (1 phrase FR), `reaction` (1–3 mots, MAJ),
     `captions` = sous-titres **en français** (traduire si stream anglais, adoucir les insultes),
     `[start_abs, end_abs, "texte"]`.
   - `layout` : `split` si `cam` connu dans streamers.json (et `cam` dans le spec), sinon `classic`
     (image entière du stream, on ne cache jamais la webcam).
   - `avatar` : `tools/avatar.png`. Rendu : `python3 tools/make_compil.py spec.json`.
   - Vérifier 3 images extraites du rendu (texte lisible, rien coupé), corriger si besoin.
4. Copier les rendus dans `clips/AAAA-MM-JJ/`, commit + push (`git -c push.negotiate=true push`).
5. Buffer `create_post` × 2 chaînes × 2 vidéos, `schedulingType: automatic`, `mode: customScheduled`,
   `dueAt` heure de Paris (offset +01:00 en hiver), créneaux décalés par plateforme :
   vidéo A → TikTok 08:00 + Instagram 12:30 + YouTube 16:00 ; vidéo B → Instagram 18:00 + YouTube 19:00 + TikTok 21:00.
   Si la vidéo A n'est pas prête avant 07:55, TikTok au plus tôt possible.
   - YouTube : `metadata.youtube` = `{title (≤ 90 car., FR, accrocheur), categoryId "20", privacy "public", madeForKids false}`
   - Texte / légende (les deux) :
     ```
     <phrase d'accroche FR>
     🎥 <Streamer> en live sur <Twitch|Kick> : <lien chaîne>
     #gta6 #gtavi #<streamer> #gta6fr #clipsgta6
     ```
5. Ajouter les entrées à `published.json` (date, streamer, vod id, segments, post ids), commit + push.
6. Rapport final en français à Mathieu (court) : vidéos publiées / programmées, streamers, problèmes.
   Supprimer de `clips/` les vidéos de plus de 7 jours (Buffer les a déjà récupérées).

## Titres, légendes et hashtags
- **Titre** (YouTube) et **accroche** (1re ligne de légende TikTok) : en français, 40–70 caractères, nom du streamer +
  ce qui se passe + tension ou curiosité, 1 emoji max. Jamais de fausse promesse (« leak », « secret » inventé).
  Formats qui tournent : « <Streamer> découvre … 💀 », « <Streamer> se fait … dans GTA 6 », « TOP 3 des moments de
  <Streamer> sur GTA 6 », « Il pensait s'en sortir… », « Le moment où <Streamer> … ».
- Varier les formules d'un jour à l'autre (vérifier published.json).
- **Chaque publication a sa propre légende et son propre jeu de hashtags** : jamais le même texte sur YouTube et TikTok,
  ni d'un jour à l'autre. TikTok : finir par une question pour les commentaires. YouTube : phrase descriptive.
- TikTok : choisir la miniature avec `assets[].video.metadata.thumbnailOffset` (ms) sur l'image la plus forte
  (gros texte / pic d'action), différente de l'image de début. YouTube : pas de choix de miniature via Buffer.
- **Hashtags** (4–5, pas de #fyp ni #pourtoi) : 2 larges `#gta6 #gtavi`, 1 FR `#gta6fr`, 1 streamer `#<login>`,
  1 lieu/thème du moment si pertinent (`#vicecity #leonida #police #course`…). YouTube : mêmes hashtags en fin de description.

## Musique de fond des clips (validé le 17/11/2026)
- `make_compil.py` ajoute automatiquement notre musique Outrun (tools/music_outrun.wav) à ~13 % du volume,
  baissée automatiquement quand le streamer parle (sidechain), et à plein volume sur l'écran de fin.
- Si le stream contient déjà de la musique (audible pendant les moments choisis) : mettre `"music": null` dans le spec.
- Option `"music": "tools/music_heist.wav"` pour varier. Jamais de musique sous droits.

## Publication TikTok
- Jusqu'au 18/11 inclus : TikTok en mode notification (publication manuelle par Mathieu). À partir du 19/11 : tout en automatique.

## Design (validé le 15/11/2026)
- Titre en bulle blanche, texte noir, en haut. Numéros #3 #2 #1 orange. Bulle de contexte violette.
- Sous-titres FR mot par mot (jaune). Zoom + flash + mot de réaction au pic.
- Filigrane `@partnersinvicefr` translucide avec contour, dans le dernier quart du gameplay.
- Barre de progression orange. Écran de fin 3 s : logo + « Abonne-toi pour la suite ».
- Marges : rien dans les ~150 px de droite (icônes TikTok/YouTube) ni en bas (légende).

## Montages de visuels officiels (template « edit »)
- `tools/make_montage.py` : visuels officiels Rockstar (rockstargames.com/VI), coupes calées sur le tempo,
  titre bulle blanche avec emojis (tools/title_png.py) qui pulse, filigrane, écran de fin. **Pas de barre de progression.**
- Musique 100 % originale : `tools/music.py outrun` (préférée de Mathieu, 118 bpm) ou `heist` (108 bpm). **Jamais de phonk.**
- Jamais de visuels non officiels (fan arts, edits d'autres créateurs).
