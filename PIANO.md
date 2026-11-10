# Piano editoriale mAInd studio – Instagram

## FASE 1 – Settimana di lancio (11-17 novembre 2026): ogni giorno un post SERVIZI
Il 10/11 è uscito il post di presentazione (numero 01, tema blu).
- 2026-11-11 · number "02" · theme "corallo" · people ["negozio","artigiano","titolare"] → Gestionali su misura + Dashboard e report
- 2026-11-12 · "03" · "salvia" · ["staff","barista","hotel"] → App per il personale + mAInd Personale (turni, ruoli, presenze, disponibilità dal telefono; demo gratuita su maindstudio.com/prodotti)
- 2026-11-13 · "04" · "petrolio" · ["studio","titolare","negozio"] → Automazioni + Assistenti con intelligenza artificiale
- 2026-11-14 · "05" · "ambra" · ["studio","artigiano","titolare"] → Aree riservate e portali
- 2026-11-15 · "06" · "viola" · ["dj","barista","chef"] → Per bar e locali: mAInd Bar, mAInd Club Planner, mAInd Studio Mix (demo su maindstudio.com/prodotti)
- 2026-11-16 · "07" · "rosa" · ["beauty","staff"] → mAInd Nails per centri unghie ed estetica (demo su maindstudio.com/prodotti)
- 2026-11-17 · "08" · "blu" · ["titolare","studio","artigiano","beauty"] → Comunicazione (logo, social, grafiche stampa, drone) + il metodo "sartoria digitale"

## FASE 2 – Dal 18 novembre 2026: alternanza notizie / singolo servizio
d = giorni dal 1970-01-01 (data Europe/Rome)
- d dispari → NOTIZIA AI DAL MONDO (kind "news", number "AI", theme "blu", people: 2 volti del settore più vicino alla notizia)
- d pari → SERVIZIO: i = (d // 2) % 12, number = i+1 a due cifre, theme = ["blu","corallo","salvia","viola","ambra","rosa","petrolio"][i % 7]
0 Gestionali su misura (ordini, magazzino, clienti, preventivi, scadenze in un unico posto) · ["negozio","artigiano","titolare"]
1 Assistenti con intelligenza artificiale (domande frequenti, riassunti di documenti, bozze dai contenuti aziendali) · ["studio","hotel","titolare"]
2 mAInd Bar (comande, ordini fornitori, magazzino, incassi di fine giornata) – demo su maindstudio.com/prodotti · ["barista","chef"]
3 Aree riservate e portali (clienti/fornitori trovano solo ciò che li riguarda) · ["studio","artigiano"]
4 mAInd Personale (turni, ruoli, presenze, disponibilità dello staff dal telefono) · ["staff","chef","hotel"]
5 Automazioni (email, documenti, promemoria, copie tra programmi) · ["titolare","negozio","studio"]
6 mAInd Nails (agenda, schede clienti con foto lavori, trattamenti, promemoria) · ["beauty","staff"]
7 Dashboard e report (i numeri che contano, export PDF ed Excel) · ["titolare","studio"]
8 App per il personale (turni, comunicazioni, richieste, senza installare nulla) · ["staff","barista","hotel"]
9 mAInd Club Planner (serate, DJ e vocalist, cachet e budget) + mAInd Studio Mix (musica del locale con stacchi e spot) · ["dj","barista"]
10 Comunicazione (logo, immagine coordinata, social, grafiche stampa, drone) · ["negozio","chef","artigiano"]
11 Metodo "sartoria digitale" (misure, cartamodello, taglio e cucitura per fasi, prova con dati reali, consegna e assistenza; un solo referente; preventivo scritto in fasi; primo incontro senza impegno) · ["titolare","studio","artigiano","beauty"]
Quando un servizio torna nel ciclo, cambia angolo (problema, settore, hook): non ripetere lo stesso post.

## Regole
SERVIZI: niente prezzi, numeri, clienti, città o testimonianze inventati (il sito non ne riporta). Promesse ammesse: un solo referente, preventivo scritto diviso in fasi, funziona dal browser su ogni dispositivo senza installare nulla, dati protetti (password personali, connessione protetta, backup, GDPR), primo incontro senza impegno di persona o online, demo su maindstudio.com/prodotti.
NOTIZIE: notizia AI delle ultime 48 ore utile per PMI italiane, verificata su 2 fonti, parafrasata, campione degli studi riportato correttamente, chiusura su cosa significa per una PMI (persone al centro, AI al fianco, niente allarmismo), "Fonte: …" nel copy.

## Spec grafica (render_post.py)
kind, theme, people (preset: chef, beauty, studio, artigiano, barista, hotel, negozio, dj, titolare, staff; etichetta personalizzata con ["chef","Cucina"]), kicker (2-4 parole, evita "mAInd"), headline (max 9 parole, 1-2 parole chiave tra *asterischi*), size 80, body (max 25 parole), cta (max 5 parole + " →"), number.
