# Partners in Vice — runbook de la tâche quotidienne

Chaîne de clips GTA 6 en français : TikTok @partnersinvicefr + YouTube « Partners in Vice | GTA 6 🌴 ».
Publication via le connecteur **Buffer** (organisation « My organization ») :
- YouTube channelId `6afa0f34ece6dfde5fd78fb8`
- TikTok channelId `6afa0f0eece6dfde5fd78eaa`

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
- Squeezie et ZeratoR ont des VODs réservées aux abonnés : ignorées tant qu'on n'a pas d'autre source.

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
   `dueAt` 12:00 et 19:00 heure de Paris (offset +01:00 en hiver) :
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

## Design (validé le 15/11/2026)
- Titre en bulle blanche, texte noir, en haut. Numéros #3 #2 #1 orange. Bulle de contexte violette.
- Sous-titres FR mot par mot (jaune). Zoom + flash + mot de réaction au pic.
- Filigrane `@partnersinvicefr` translucide avec contour, dans le dernier quart du gameplay.
- Barre de progression orange. Écran de fin 3 s : logo + « Abonne-toi pour la suite ».
- Marges : rien dans les ~150 px de droite (icônes TikTok/YouTube) ni en bas (légende).
