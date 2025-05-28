from app import app, CalendarioEsame, db

with app.app_context():
    print('Totale tipi di attività:', CalendarioEsame.query.count())
    
    # Stampa il conteggio per ogni tipo di attività
    tipi_attivita = {
        'definizione_argomento_scritta': CalendarioEsame.query.filter_by(attivita='definizione_argomento_scritta').count(),
        'definizione_argomento_lezione': CalendarioEsame.query.filter_by(attivita='definizione_argomento_lezione').count(),
        'definizione_criteri': CalendarioEsame.query.filter_by(attivita='definizione_criteri').count(),
        'prova_scritta_presenza': CalendarioEsame.query.filter_by(attivita='prova_scritta_presenza').count(),
        'prova_scritta_consegna': CalendarioEsame.query.filter_by(attivita='prova_scritta_consegna').count(),
        'valutazione_prova_scritta': CalendarioEsame.query.filter_by(attivita='valutazione_prova_scritta').count(),
        'lezione_simulata': CalendarioEsame.query.filter_by(attivita='lezione_simulata').count(),
        'altro': CalendarioEsame.query.filter_by(attivita='altro').count()
    }
    
    # Stampa anche i vecchi tipi per verificare che non ne rimangano
    vecchi_tipi = {
        'prova_scritta': CalendarioEsame.query.filter_by(attivita='prova_scritta').count(),
        'prova_orale': CalendarioEsame.query.filter_by(attivita='prova_orale').count(),
        'prova_pratica': CalendarioEsame.query.filter_by(attivita='prova_pratica').count(),
    }
    
    print("\nStatistiche per nuovi tipi di attività:")
    for tipo, conteggio in tipi_attivita.items():
        print(f"{tipo}: {conteggio}")
        
    print("\nVerifica vecchi tipi di attività (dovrebbero essere tutti 0 dopo la migrazione):")
    for tipo, conteggio in vecchi_tipi.items():
        print(f"{tipo}: {conteggio}")
