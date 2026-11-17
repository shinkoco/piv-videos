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

## Rotation hebdomadaire (à partir du 19/11)

Chaque jour, par compte : clips A et B (horaires inchangés) + 1 carrousel (TikTok et Instagram) + une 3e vidéo certains jours.

| Jour | Carrousel (IG 10:00, TikTok 13:00) | 3e vidéo (YT 12:00, TikTok 18:00, IG 20:00) |
|---|---|---|
| Lundi | Sondage / débat | — |
| Mardi | Actu de la semaine | Montage de visuels officiels (make_montage.py) |
| Mercredi | Guide pratique | — |
| Jeudi | Vrai ou faux | Vrai ou faux en vidéo (montage 9:16, une affirmation par segment, réponse « VRAI »/« FAUX » au beat) |
| Vendredi | Nostalgie Vice City 2002 contre GTA 6 | — |
| Samedi | Sondage / débat | Montage de visuels officiels |
| Dimanche | Top de la semaine | — |

### Règles des formats
- Carrousels : make_carousel.py, 6 à 10 slides, 1080×1350. Instagram : `type: "post"`. TikTok : publication photo ; la musique originale est ajoutée seulement si l'API le permet.
- Sondage / débat : une question clivante sur le jeu (ex. : Jason ou Lucia ?). La dernière slide dit « Réponds en commentaire ».
- Actu, guide, vrai ou faux : recherche web obligatoire, uniquement des sources fiables (Rockstar Newswire, Take-Two, grands médias jeu vidéo). Chaque fait est vérifié et la source est citée en légende. Si une info n'est pas confirmée, elle est présentée comme « rumeur non confirmée », ou laissée de côté. Zéro fake, jamais.
- Nostalgie : visuels officiels de GTA 6 uniquement. Vice City 2002 est évoqué par le texte seulement : aucune image tierce.
- Top de la semaine : les 3 meilleurs moments des clips de la semaine (captures de nos propres rendus).
- Compilation longue YouTube : EN PAUSE (décision du 17/11, focus Shorts/TikTok). Ne pas produire.
- Toujours : uniquement des visuels officiels ou nos propres clips, uniquement notre musique originale (jamais de phonk). Chaque post a sa propre légende et ses propres hashtags.
- Limite Buffer : 10 posts programmés par canal. Ne programmer que J et J+1, jamais plus loin.

## TikTok : publication manuelle (décision du 17/11)
TikTok bloque la distribution des posts publiés via l'API sur ce compte : 0 vue, et « ajouter à la story » indisponible, pour la vidéo J-3 comme pour le carrousel.
- TOUS les posts TikTok (clips, carrousels, 3e vidéo) partent avec `schedulingType: "notification"` : Mathieu reçoit un rappel et publie lui-même depuis l'appli, en ajoutant un son tendance.
- Cette règle remplace « automatique à partir du 19/11 ». Instagram et YouTube restent automatiques.

## TikTok via Zernio (décision du 17/11, remplace les sections TikTok précédentes)
TikTok ne passe PLUS par Buffer, il passe par Zernio, compte PIV `6afc525031be0a779a30b36e`. Buffer garde Instagram (`6afb16d7ece6dfde5fe51faf`) et YouTube PIV (`6afa0f34ece6dfde5fd78fb8`).
Publication automatique via `call_tool posts_create_post` :
- Vidéo : `media_items` contient 1 vidéo (URL raw GitHub). Mettre `scheduled_for` en heure locale avec `timezone` "Europe/Paris", et `platforms` = [{platform: "tiktok", accountId: "6afc525031be0a779a30b36e"}].
- `tiktok_settings` : `{"privacyLevel": "PUBLIC_TO_EVERYONE", "allowComment": true, "allowDuet": true, "allowStitch": true, "contentPreviewConfirmed": true, "expressConsentGiven": true, "videoCoverTimestampMs": <frame du grand J-x ou du pic>}`
- Carrousel : `media_items` contient les images, avec `tiktok_settings.mediaType` "photo", `autoAddMusic` true et `description` = la légende complète. `content` ≤ 90 caractères : c'est le titre.
- Limites : 15 vidéos et 15 photos par jour et par compte. Ne jamais mettre de `draft` sauf si Mathieu le demande.
- Le compte Tamko TikTok (`6af7635df038e4d78c1b8569`) est sur le même Zernio : ne JAMAIS publier dessus depuis cette tâche.

## Déjà programmé (ne pas refaire)
- Samedi 21/11 : la 3e vidéo est DÉJÀ programmée (montage « Bienvenue à Vice City », clips/2026-11-21/vc_welcome.mp4) sur YouTube 12:00, TikTok 18:00 et Instagram 20:00. Ce jour-là, ne pas produire de 3e vidéo.

## Règle de démarrage (17/11, remplace « ne rien faire avant le 19/11 »)
La rotation des formats (carrousels et 3e vidéo) tourne TOUS les jours, dès maintenant. Seuls les clips de streamers attendent la sortie du jeu, le 19/11. Chaque matin, la tâche programme les publications du lendemain. Elle n'attend jamais de validation.

## Zéro carrousel pour le moment (décision du 17/11, remplace tout ce qui concerne les carrousels)
Les carrousels font 0 vue sur Instagram comme sur TikTok, alors que les vidéos sont poussées. Tant que le compte a peu d'abonnés :
- Chaque « carrousel » de la rotation est produit en slides avec make_carousel.py, puis converti en VIDÉO diaporama 9:16 avec `tools/make_slideshow.py OUT.mp4 <musique outrun ou heist> <bpm> slides...` (6 temps par slide, environ 3 s).
- Il est publié en vidéo : en Reel sur Instagram à 10:00, en vidéo sur TikTok à 13:00 via Zernio, et en Short sur YouTube à 14:00.
- Ne JAMAIS publier en `type: "post"` ni en `mediaType: "photo"`.
