# ⚠️ ÉTAT ACTUEL AU 20/11/2026 — CE RÉSUMÉ FAIT FOI (en cas de contradiction plus bas)
- TikTok — ENVOI DES BROUILLONS 45 MIN AVANT l'heure de publication (constat : TikTok livre un brouillon 20 à 35 min après l'envoi). Envoyer à 11:15 / 16:15 / 20:15 pour une publication par Mathieu vers 12:00 / 17:00 / 21:00 ; dans hub/piv.json → drafts, « time » = heure de PUBLICATION conseillée.
- TikTok (Zernio 6afc525031be0a779a30b36e) : 3 vidéos/jour MAX à 12:00, 18:00, 21:00, envoyées le matin en BROUILLON (tiktok_settings draft true, 5 brouillons max/24 h). Légendes dans hub/piv.json → channel.drafts [{time,label,caption}]. Légendes SANS URL, 5 hashtags, jamais #shorts. Pas de publication directe.
- YouTube (Buffer) : 2 Shorts par 24 h GLISSANTES (validé par Mathieu le 21/11). TEST HEBDO : tous les 7 jours (le dimanche), programmer un 3e Short dans la fenêtre ; s'il passe sans erreur, noter « 3/24 h OK » dans alerts et le RUNBOOK ; sinon le replanifier et rester à 2. (Buffer envoie avec 1-3 min de retard, donc des créneaux fixes identiques chaque jour échouent). RÈGLE DE CALCUL (20/11) : avant de programmer un Short, lire dans Buffer les sentAt des 2 derniers Shorts envoyés ; le nouveau dueAt doit être ≥ (sentAt de l'AVANT-DERNIER) + 24 h 20 min. Viser ~14:30-16:00 et ~20:00-22:00 ; si l'heure calculée dépasse 22:30, reporter au lendemain. Priorité clips streamers. Chaque matin, recalculer et replanifier les posts en erreur.
- Instagram (Buffer) : clips A, B et diaporama. Max 10 posts en attente par chaîne Buffer.
- Chaque matin : réponses aux commentaires TikTok (max 15, replied_comments.json) ; liste « Chauffe TikTok » (channel.warmup, 5 liens, comptes vérifiés uniquement) ; rotation des visuels (visuals_used.json).
- Sources clips : Twitch public d'abord, YouTube : ⚠️ BLOQUÉ depuis le cloud (testé 21/11 : « Sign in to confirm you're not a bot », les listes passent mais pas le téléchargement) → ne pas compter dessus ; secours = clips Twitch d'autres streamers (FR puis US). STREAMERS FR VÉRIFIÉS (21/11, liste validée avec Mathieu) — Twitch : squeezie, michou, inoxtag (Inox), aminematue (Amine), jltomy, kamet0 (Kameto, arc GTA VI), zerator, gotaga, domingo, anyme023 ; YouTube : LaSalle (youtube.com/channel/UCyMy3i-BaVOmOwTZskm52Ew, vidéos GTA 6). Faire tourner les streamers : jamais le même streamer 2 jours de suite si un autre a du GTA 6 récent. TikTok : Michou @michouoff, Anyme @anyme023.
- STREAMERS US (21/11, demandé par Mathieu) : AUTORISÉS, max 1 clip US par jour (les autres restent FR). Twitch vérifiés avec GTA 6 : kaicenat (Kai Cenat), xqc, ishowspeed (IShowSpeed, aussi YouTube), summit1g. Toujours SOUS-TITRES EN FRANÇAIS (transcrire l'anglais avec faster-whisper, traduire en français naturel, mot-clé en rose) + accroche en français. Légende FR : « 🎥 Kai Cenat en live sur Twitch ».
- CLIPS DE STREAMERS OBLIGATOIRES (21/11) : MINIMUM 2 clips de streamers par jour (A et B), même si les moments sont moyens : jamais de journée avec un seul clip. Diaporamas/sondages seulement en 3e position (et sur Instagram). Si Twitch ne donne rien, prendre YouTube (VOD publiques, autres streamers FR).
- CLIPS (validé 20/11) : template « Réaction PIV » via tools/make_reaction.py spec.json out.mp4 (voir docstring). 60 s MINIMUM (2-3 clips Twitch du même streamer), webcam en haut, filet rose, accroche courte, sous-titres mot-clé rose, emojis/pops sur les temps forts, NOIR ET BLANC sur la désolation, repères 1/3-3/3, outro 3 s. Plus de gros titre, classement ni barre de progression. make_compil.py = ANCIEN, ne plus l'utiliser pour les clips. Repérer la webcam en regardant une image du clip (crop x,y,w,h). Template « Série » (bulle webcam, épisodes) : à construire plus tard.
- [ABANDONNÉ 21/11, voir ANTI-BANNISSEMENT] COUVERTURES (validé 20/11, option A) : 1re image de chaque diaporama = tools/make_cover.py (barre « ACTU GTA VI · SUJET », pastille rose catégorie, titre 2 lignes Inter Display Black MAJUSCULES, sous-titre rose, avatar). Titres au « tu » qui promettent un bénéfice (ex. « ARGENT ILLIMITÉ — 5 astuces cachées dans GTA 6 »). Inspiration : @radioleonida.fr.
- FORMAT TIKTOK (validé 21/11) : 12:00 = clip LONG (60 s+, monétisation) ; 17:00 = clip COURT 15-25 s (portée/abonnés : meilleur moment d'un clip long, réplique culte ou chute, coupé juste avant la fin pour la boucle ; make_reaction.py avec "short": true, sans repères ni outro) ; 21:00 = clip LONG. Le clip court va aussi en YouTube Short et Reel Instagram si un créneau est libre.
- WEEK-END (21/11) : samedi et dimanche, les 3 TikTok sont 3 CLIPS DE STREAMERS (pas de diaporama), horaires 12:00, 17:00, 21:00 ; Instagram peut recevoir en plus le diaporama.
- ZONES SÛRES TikTok (CORRIGÉES 21/11, mesurées sur iPhone de Mathieu) : les écrans de téléphone rognent ~110 px de CHAQUE côté. Tout texte/encart dans le rectangle x 130→950 (largeur max 800), y 230→1500 ; rien à droite de x=930 entre y 1000 et 1700 (icônes). Avant chaque export, vérifier une image du clip avec le cadre de contrôle (tools/safezone_check.py video.mp4 <seconde> check.jpg) et corriger si un élément dépasse. Accroche ≤ 20 caractères pour tenir sur 1 ligne.
- ANTI-BANNISSEMENT (21/11, décision de Mathieu, PRIORITÉ ABSOLUE) — politiques YouTube « contenu réutilisé » et « contenu générique ou répétitif », mêmes principes sur TikTok :
  1. YouTube : UNIQUEMENT des clips de streamers. ZÉRO diaporama sur YouTube (YouTube cite les diaporamas sans narration comme non monétisables).
  2. TikTok : clips de streamers en priorité ; diaporama max 1 par semaine et seulement s'il apporte une vraie info (actu sourcée), jamais une simple galerie d'images. Les diaporamas déjà publiés restent en ligne.
  3. Instagram : clips + diaporamas autorisés.
  4. FINI LE MODÈLE FIXE : make_reaction.py tire au hasard un style différent (palette, bulle, position de l'accroche, filet) — ne jamais forcer le même style 2 clips de suite. Varier aussi chaque jour : formulation des accroches, emojis, effets (noir et blanc, zoom), structure des légendes. make_cover.py (couverture fixe façon Radio Leonida) est ABANDONNÉ.
  4b. LAYOUTS (21/11, idée de Mathieu) : alterner "split" (webcam en haut / jeu en bas : moments d'ACTION) et "double" (live complet en haut, gros plan visage du streamer en bas, accroche au milieu : moments où le streamer PARLE/RÉAGIT, parfait pour les clips COURTS). En "double", renseigner "zoom" = cadre serré sur le visage.
  5. VALEUR AJOUTÉE dans chaque clip : 1 à 2 « réactions de la chaîne » en pop-up (champ pops), écrites par nous, ex. « On aurait fait pareil 😂 », « Le pire c'est qu'il avait raison », « Rockstar l'a fait exprès 👀 ». Jamais 2 fois la même phrase dans la semaine.
- Slack ARRÊTÉ (20/11) : plus aucun message Slack, tout passe par le HUB (hub/piv.json → alerts).
- Jamais : automatiser likes/commentaires, deviner un handle, fan art/IA, VidIQ, outils payants.

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

## TikTok : retour en publication AUTO (19/11, 19:05) — remplace le mode brouillon
Mathieu ne veut pas publier à la main. TikTok repasse en publication directe programmée via Zernio (sans draft), MAIS 3 vidéos/jour max à 12:00, 18:00, 21:00, jamais 2 à moins de 3 h d'écart, légende sans URL. Ne plus remplir channel.drafts (laisser vide).

## ANNULE la section précédente (19/11, 19:06) : TikTok reste en BROUILLON
Erreur d'interprétation : Mathieu veut le mode brouillon (Zernio tiktok_settings draft true, 3/jour à 12:00, 18:00, 21:00, légendes dans hub/piv.json → channel.drafts). Ce qu'il refuse, c'est télécharger la vidéo à la main. Pas de publication directe sur TikTok.

## Anyme (19/11)
Ajouté par Mathieu : TikTok @anyme023 (handle confirmé par lui) → à inclure dans la chauffe et dans les créateurs FR à surveiller pour les clips. Twitch NON vérifié : avant tout clip, vérifier si twitch.tv/anyme023 existe et diffuse GTA 6 ; sinon prendre ses vidéos YouTube publiques. Jamais d'URL dans la légende TikTok.
MAJ 19/11 19:25 : Twitch CONFIRMÉ — twitch.tv/anyme023 diffuse GTA VI (« 5 JOURS NON STOP GTA VI »), VODs accessibles avec yt-dlp. YouTube aussi accessible depuis l'environnement (yt-dlp OK) : les VODs YouTube publiques des streamers FR sont une source valable quand Twitch est en sub-only.

## Nouveaux templates de clip (20/11, validés en maquette, À TESTER avant usage quotidien)
Template 1 « Réaction PIV » (principal) : écran partagé, webcam du streamer en haut (~46 %), jeu en bas, filet rose #E52E9E entre les deux ; accroche courte (3-4 mots) dans la pastille blanche en haut ; sous-titres discrets façon TikTok, mot-clé en rose ; repères 1/3, 2/3, 3/3 ; ON GARDE les gros mots/emojis qui apparaissent sur les temps forts ; NOIR ET BLANC sur les moments de désolation (+ léger zoom). On SUPPRIME : gros titre 2 lignes, classement #1/#3, barre de progression.
Template 2 « Série » : jeu plein écran, webcam en bulle ronde cerclée de rose, étiquette « Épisode N · titre », fin « La suite au prochain clip ». Pour les histoires en plusieurs parties.
Tant que Mathieu n'a pas validé un clip test, garder l'ancien montage.
MAJ 20/11 (retours de Mathieu sur le test) : durée MINIMUM 60 s (enchaîner 2-3 clips Twitch du même streamer, même cadrage webcam) + outro endcard.py 3 s à la fin. Qualité webcam petite/floue = OK, ne pas écarter un streamer pour ça. Doubles sous-titres (stream + nos sous-titres) = acceptable. Référence : clips/tests/2026-11-20_anyme_reaction_piv_71s.mp4.

## 20/11 08:40 : diaporama « Bienvenue à Vice City » (clips/2026-11-21/vc_welcome.mp4)
Son envoi TikTok direct du 21/11 a été supprimé. Le 21/11 au matin, l'envoyer en BROUILLON comme les autres (légende : « Bienvenue à Vice City 🌴 Tu commences par quoi : la plage, les néons ou les grosses cylindrées ? 👇 📸 Visuels officiels Rockstar Games · 🎵 son original #gtavi #vicecity #leonida #gta6fr #gamingfr »). Attention : dans Zernio, un brouillon programmé à une heure n'arrive dans la boîte TikTok qu'à cette heure-là.
- Drapeaux emoji (🇺🇸…) NON supportés par title_png/emoji_png : ne pas en mettre.

## 22/11 : clip court DÉJÀ PRÊT
Le clip court de 17:00 du 22/11 est clips/2026-11-22/kai_short.mp4 (Kai Cenat, 20 s, validé par Mathieu). Ne pas en refaire un ; l'envoyer en brouillon à 16:15. Légende : « Kai Cenat prend 6 étoiles en 20 secondes 😱 Tu fais mieux ? 👇 🎥 Kai Cenat en live sur Twitch #gta6 #kaicenat #gta6fr #gamingfr #gta6gameplay ». Comme c'est le clip US du jour, les 2 clips longs du 22/11 sont FRANÇAIS.
