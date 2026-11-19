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

## Rotation des musiques (17/11)
On a 2 musiques : Outrun (118 bpm) et Heist (108 bpm). Jamais de phonk.
- Alterner d'une vidéo à l'autre : si la dernière vidéo publiée (voir published.json, champ "music") était en Outrun, la suivante est en Heist, et inversement.
- Pour ne pas réutiliser exactement le même morceau, générer une variante avec `python3 tools/music.py outrun|heist OUT.wav <durée> <seed>`, avec seed = la date du jour au format AAAAMMJJ plus le numéro de la vidéo.
- Passer le bon bpm aux outils : 118 pour Outrun, 108 pour Heist.
- Noter le style utilisé dans published.json.

## Installation au démarrage de chaque exécution (OBLIGATOIRE, 18/11)
L'environnement de la tâche repart de zéro à chaque exécution. Avant toute chose, lancer :
`pip install --break-system-packages -q yt-dlp faster-whisper numpy pillow`
Vérifier ensuite que `ffmpeg` est présent (sinon : `apt-get install -y -q ffmpeg`). Ne JAMAIS sauter les clips parce qu'un outil manque : l'installer.

## Calendrier : clips du jour J, rotation du lendemain (18/11)
- Clips de streamers A et B : pour le JOUR MÊME (horaires du runbook, de TikTok 08:00 à TikTok 21:00). Ils sont faits à partir des streams GTA 6 des dernières 24 h. Si un créneau est déjà passé ou à moins de 20 min, le décaler au prochain créneau libre du jour.
- Rotation (diaporama et 3e vidéo) : programmée pour le LENDEMAIN.

## Stats
- TikTok PIV : `call_tool posts_list_posts` avec `account_id` "6afc525031be0a779a30b36e" et `status` "published", puis `analytics_get_analytics` pour chaque post. Ne pas filtrer sur le profil : les deux comptes TikTok partagent le même profil Zernio.
- Les stats Buffer peuvent avoir jusqu'à 24 h de retard : l'indiquer dans le récap si tout est à 0.

## Charte graphique v2 (18/11, à appliquer à toutes les vidéos)
- Police : Inter Display uniquement (Black pour les titres et chiffres, Bold ou SemiBold pour le reste). Aucune police script ou fantaisie.
- Couleurs (nouvel avatar) : violet profond #1B0A3C, violet #7B3FE4, magenta #E52E9E, rose #FF3DA8. Dégradé = violet → magenta → rose.
- Titre (hook) : pastille blanche arrondie avec une ombre douce, texte Inter Display Black.
- Fin de vidéo : fond violet profond, avatar `tools/avatar_v2.png` en rond au centre, puis une pastille blanche « Abonne-toi pour la suite ». Ne JAMAIS écrire « Partners in Vice » en texte.
- Choix V2 (18/11) : texte du titre en dégradé violet → rose dans la pastille blanche (géré par title_png.py), grand chiffre en blanc. Fin de vidéo générée par tools/endcard.py (utilisée automatiquement par make_montage et make_compil).

## Mots-clés et hashtags (VidIQ, 18/11) : rotation obligatoire
Source : VidIQ, recherches en France. Chaque post combine 1 tag CŒUR, 2 tags THÈME (selon le contenu), 1 tag FR et 1 tag NICHE, soit 5 au total, jamais le même assortiment deux fois de suite.
- CŒUR (gros volume, à alterner) : #gta6, #gtavi, #gta6gameplay, #grandtheftauto6
- FR (moins de concurrence, notre cible) : #gta6fr, #gta6français, #gta6infos, #gta6nouveautés
- THÈMES, selon le contenu :
  - Gameplay et clips : #gta6gameplay, #gta6online, #gaming
  - Carte et monde : #gta6map, #vicecity, #leonida, #gta6vicecity
  - Personnages : #gta6lucia, #jasonetlucia
  - Voitures : #gta6cars
  - Actu et infos : #gta6news, #gta6infos, #rockstargames
  - Consoles et tech : #gta6ps5, #ps5, #xboxseries, #gta630fps
- NICHE (génériques jeu vidéo, à alterner) : #gaming, #jeuxvidéo, #gamingfr, #ps5, #xboxseriesx, #easteregg (uniquement pour un vrai easter egg), #jeuxvideofr
  - JAMAIS #shorts, ni en hashtag ni dans les légendes ou les titres (inutile en 2026).
  - Tags YouTube génériques : « jeux vidéo », « gaming », « gameplay », « ps5 », « xbox series x », « easter egg » (si pertinent).
- Titres YouTube et légendes : placer naturellement un mot-clé fort (« GTA 6 », « GTA 6 gameplay », « Vice City », « Lucia », « carte de Leonida », « GTA 6 en français »), sans bourrage.
- YouTube : tags vidéo = les mêmes mots-clés sans #, plus « gta 6 fr » et « gta 6 français ».
- Hors sujet, à éviter : « gta 6 south park », « gta 6 edge », « gta 6 leaks » (risque d'infos non vérifiées).

## Emojis sur les clips (18/11)
Au moment fort, 2 emojis apparaissent de part et d'autre du mot-réaction : ils montent doucement en se balançant pendant environ 1,3 s. Dans spec.json, le champ optionnel `"emojis": ["🔥","😱"]` de chaque moment les choisit selon l'ambiance (🔥 action, 😱 surprise, 💀 échec, 😂 drôle, 🚨 police, 💥 crash, 😳 gênant). Sans ce champ, make_compil fait tourner des paires par défaut. Le rendu est local, donc gratuit.

## Priorité aux streamers FR (18/11)
Clips A et B : piocher d'abord parmi les streamers français de streamers.json (Squeezie, ZeratoR, Gotaga, Inoxtag, Michou, Kameto, Doigby, etc.). Les streamers US ne servent qu'en secours, si aucun moment FR assez fort n'est trouvé dans les dernières 24 h. Pour les VOD réservées aux abonnés, passer par clips.py (clips publics Twitch).
En cas d'échec d'une étape : ne jamais publier un clip à moitié fini, passer au moment ou au streamer suivant, et le signaler dans le récap.

## Musiques : 7 styles en rotation (18/11, remplace la règle des 2 musiques)
Styles validés par Mathieu, tous générés par `tools/music.py STYLE OUT.wav DURÉE SEED` (originaux, sans droits) :
- outrun (118 bpm) : synthwave pumping, polyvalent
- heist (108 bpm) : sombre, gros snare, braquages et tension
- sunset (104 bpm) : synthwave lumineuse en arpèges, le style préféré de Mathieu, à utiliser souvent
- miami (92 bpm) : planant, pour les montages et diaporamas
- drive (140 bpm) : rapide, pour l'action et les poursuites
- funk (112 bpm) : groove années 80, pour les moments drôles
- tension (88 bpm) : suspense, pour les vrai ou faux et les moments tendus
Règles : choisir selon l'ambiance, jamais le même style deux vidéos de suite (vérifier le champ "music" de published.json), toujours un seed unique (date + numéro de la vidéo), passer le bon bpm aux outils. phonk est INTERDIT.

## HUB (19/11) : écrire dans CE dépôt
La tâche n'a pas accès au dépôt studiomgi.github.io. Elle écrit donc le récap du HUB dans `hub/piv.json` de CE dépôt (shinkoco/piv-videos), puis commit et push avec le reste. La page https://studiomgi.github.io lit ce fichier en direct.
Format : {"updated": "AAAA-MM-JJTHH:MM:00+01:00", "date_label": "Jeudi 19 novembre", "alerts": ["Partners in Vice : …"], "channel": {...}}.
"channel" reprend le format décrit dans HUB.md : name, headline [début, fin en gras], summary, kpis, followers, today [{time, platform, title, status}], upcoming, trend, engagement, best_time. Partir du fichier existant et le mettre à jour. N'inventer aucun chiffre (null si inconnu).

## Clips C et D, TikTok uniquement (19/11 au 19/12/2026 minimum)
Pendant le mois de lancement : 4 clips de streamers par jour.
- Clips A et B : inchangés, sur les 3 plateformes.
- Clips C et D : TikTok seulement, via Zernio, à 15:00 et 23:00. Ce sont d'autres moments et d'autres streamers que A et B (priorité FR), avec la charte v2, les emojis, une musique différente du clip précédent et 5 hashtags de la rotation.
- Si les moments forts manquent, ne publier que ce qui est bon : mieux vaut 3 clips qu'un clip faible.
- Après le 19/12, réévaluer avec Mathieu selon les stats et la consommation d'usage.

## Rotation des visuels (19/11)
Objectif : ne presque jamais réutiliser les mêmes images.
- Tenir `visuals_used.json` à jour (nom du fichier, nombre d'utilisations, dernière date). Pour chaque diaporama ou montage, prendre en priorité les images jamais utilisées, puis les moins utilisées. Pas d'image déjà utilisée dans les 14 derniers jours.
- Sources autorisées, toutes gratuites et sans outil supplémentaire :
  1. Visuels officiels Rockstar : captures et artworks de la page GTA VI et du Newswire sur rockstargames.com. Vérifier régulièrement s'il y en a de nouveaux, et les ajouter dans `visuals/rockstar/`.
  2. Images tirées de nos propres clips : les meilleures frames 4K des streams déjà téléchargés (paysages, voitures, scènes fortes), sans webcam ni interface. Les ajouter dans `visuals/frames/`.
- Interdit : fan art, images d'autres créateurs, captures d'autres comptes de clipping, images IA.

## Limite YouTube via Buffer (19/11)
Buffer refuse au-delà d'environ 3 posts YouTube par jour et par chaîne (erreur « daily posting limit »). Règle : MAX 3 posts YouTube par jour (clips A et B + au plus 1 diaporama). Les vidéos en trop vont sur un autre jour. Chaque matin, vérifier les posts YouTube en erreur dans Buffer et les replanifier sur un jour qui a moins de 3 posts.

Buffer gratuit : 10 posts EN ATTENTE max par chaîne (place libérée à chaque publication). Ne jamais programmer au-delà.

## Chauffe TikTok dans le HUB (19/11)
Chaque matin, écrire dans hub/piv.json → channel.warmup une liste de 5 éléments {label, url, comment} : liens TikTok directs (pages hashtag tiktok.com/tag/…, recherche tiktok.com/search?q=…, profils de streamers FR du moment tiktok.com/@…), avec un commentaire court, naturel, en français, différent chaque jour. Mathieu les ouvre et agit lui-même : JAMAIS d'automatisation de likes, commentaires ou abonnements.
Chauffe : n'utiliser QUE des comptes TikTok vérifiés (handle trouvé dans une source fiable : description YouTube officielle, Social Blade). Comptes connus : @michouoff, @sniryt, @chris_klippel. JAMAIS deviner un handle (@michou est un faux compte).

## Réponses aux commentaires TikTok via Zernio (19/11)
Chaque matin : `comments_list_inbox_comments` (account_id 6afc525031be0a779a30b36e), puis pour chaque post avec commentCount > 0, lire les commentaires et répondre aux nouveaux avec `comments_reply_to_inbox_post` (post_id, account_id, comment_id).
- Réponses courtes, naturelles, en français, ton pote gamer, 1 emoji max, toujours différentes ; relancer avec une question quand c'est possible.
- Max 15 réponses par jour. Ignorer spam, insultes, liens, haine (ne pas répondre).
- Jamais de promesse, jamais de faux, jamais de demande d'abonnement agressive.
- Noter chaque comment_id traité dans replied_comments.json pour ne jamais répondre deux fois.
- Instagram et YouTube : pas d'outil de réponse gratuit (Buffer) → ne rien faire.

## YouTube : 2 posts par 24 h GLISSANTES (19/11, constaté)
Les faits : sur la chaîne PIV, YouTube refuse le 3e Short dans une fenêtre de 24 h glissantes. Règle (remplace « max 3 par jour ») :
- 2 créneaux YouTube fixes par jour : 14:30 et 20:00 (Paris). Jamais d'autre horaire.
- Priorité YouTube : clips de streamers (A puis B). Diaporamas sur YouTube seulement si un créneau est libre ; sinon diaporama TikTok + Instagram uniquement.
- Déjà programmés : 20/11 14:30 nos1 · 21/11 14:30 vc_welcome · 22/11 14:30 squeezie1 → le clip A du jour va à 20:00, le clip B ne va pas sur YouTube ces jours-là.
- Chaque matin, replanifier tout post YouTube en erreur sur le prochain créneau libre.
- Si la limite augmente (aucune erreur 7 jours de suite), tester 3 créneaux : 12:00, 16:30, 21:00.

## TikTok : pas d'URL dans les légendes (19/11)
Sur TikTok, ne JAMAIS mettre d'URL (twitch.tv/…) dans la légende : liens non cliquables et suspectés de freiner la diffusion. Crédit en texte seul : « 🎥 JLTomy en live sur Twitch ». Les URL restent OK sur YouTube et Instagram.

## TikTok : mode BROUILLON + 3 posts/jour max (19/11)
Constat : 6 posts TikTok le 19/11 sur un compte à 40 abonnés → les derniers à 0 vue. Nouvelle règle (remplace clips C et D et tout envoi direct TikTok) :
- TikTok = 3 vidéos/jour MAX, espacées : 12:00, 18:00, 21:00. Priorité : clip A, clip B, puis diaporama ou clip C. Jamais 2 vidéos à moins de 3 h d'écart.
- Envoi via Zernio en brouillon : posts_create_post avec publish_now true, tiktok_settings {"draft": true}, le matin (TikTok : 5 brouillons max par 24 h). Mathieu publie à la main depuis sa Boîte de réception TikTok.
- La légende n'est PAS transmise : l'écrire dans hub/piv.json → channel.drafts [{time, label, caption}] (sans URL, 5 hashtags, jamais #shorts).
- Les posts TikTok déjà programmés en direct dans Zernio : les supprimer et les renvoyer en brouillon le jour J.
