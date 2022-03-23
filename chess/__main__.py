import main

if __name__ == '__main__':
    main.run()


# TODAY
# aggiungere tabelle end game per re e pedoni (+ logica di quando si entra in end game)
# alla fine della partita tasto per vedere la partita e non per tornare indietro
# appena premi f il consiglio sul fullscreen va via
# testo in rosso usato anche per avvertire se server down


# TOMORROW
# testare se da vittoria quando giocatore si disconnette per mancata connessione (probabilmente no) con Damiano


# ai prova a fare scacco matto e non si muove a caso
# regole strane per i 50 turni eccetrea (anche nelle fen board)
# estetica settings single player
# ottimizzare conversione immagini pezzi (vedere se si può fare solo al cambio fullscreen)
# aggiungere tempo nel multigiocatore ???


# funzione end turn in "board.py" ???
# funzione grab piece and release ???
# AI sottoforma di classe ???
# tempo e board nel server ??? e agli utenti vengono mandate le fen ???


# SICUREZZA
# vedere se cambiando il codice di un solo utente si possono fare mosse illegali
# soluzione: server controlla con una sua board, e se mossa illegale butta fuori utente