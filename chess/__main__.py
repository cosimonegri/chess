import main

if __name__ == '__main__':
    main.run()


# TODAY


# TOMORROW


# testare se da vittoria quando giocatore si disconnette per mancata connessione (probabilmente no)
# aggiungere tabelle end game per re e pedoni (+ logica di quando si entra in end game)
# ai prova a fare scacco matto e non si muove a caso
# forse ai non arrocca più
# regole strane per i 50 turni eccetrea (anche nelle fen board)
# estetica settings single player
# estetica popup loading (numero di puntini dinamico nel tempo, oppure rotella che gira)
# ottimizzare conversione immagini pezzi (vedere se si può fare solo al cambio fullscreen)
# vedere se possono non passare la board ai metodi draw tutte le volte in "game_screen.py"
# aggiungere tempo nel multigiocatore ???


# funzione end turn in "board.py" ???
# funzione grab piece and release ???
# AI sottoforma di classe ???
# tempo e board nel server ??? e agli utenti vengono mandate le fen ???


# SICUREZZA
# vedere se cambiando il codice di un solo utente si possono fare mosse illegali
# soluzione: server controlla con una sua board, e se mossa illegale butta fuori utente