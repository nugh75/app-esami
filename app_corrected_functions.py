# index() - Funzione corretta
def index():
    # Parametri di ricerca e filtro
    search = request.args.get('search', '')
    classe_filter = request.args.get('classe', '')
    modalita_filter = request.args.get('modalita', '')
    
    # Query base
    query = Esame.query
    
    # Applicazione filtri
    if search:
        query = query.filter(
            db.or_(
                Esame.classe_concorso.contains(search),
                Esame.sede.contains(search),
                Esame.note.contains(search)
            )
        )
    
    if classe_filter:
        query = query.filter(Esame.classe_concorso == classe_filter)
    
    if modalita_filter:
        query = query.filter(Esame.modalita == modalita_filter)
    
    # Usa created_at per l'ordinamento per essere sicuri
    try:
        esami = query.order_by(Esame.created_at.desc()).all()
    except Exception as e:
        print(f"Errore nell'ordinamento: {e}")
        # Fallback: carica senza ordinamento
        esami = query.all()
    
    # Statistiche per il dashboard
    stats = {
        'totale_esami': Esame.query.count(),
        'online': Esame.query.filter_by(modalita='online').count(),
        'presenza': Esame.query.filter_by(modalita='presenza').count(),
        'mista': Esame.query.filter_by(modalita='mista').count(),
        'con_commissione': Esame.query.join(Commissione).distinct().count(),
        # Statistiche per i ruoli delle commissioni
        'commissioni': {
            'titolari': Commissione.query.filter_by(tipologia='T').count(),
            'supplenti': Commissione.query.filter_by(tipologia='S').count(),
            'presidenti': Commissione.query.filter_by(ruolo='presidente').count(),
            'docenti_interni': Commissione.query.filter_by(ruolo='docente_interno').count(),
            'esperti_esterni': Commissione.query.filter_by(ruolo='esperto_esterno').count(),
            'referenti_usr': Commissione.query.filter_by(ruolo='referente_usr').count()
        },
        # Statistiche per i profili
        'profili': {
            'prof_ricercatori': Commissione.query.filter_by(profilo='prof_ricercatore_roma3').count(),
            'assegnisti': Commissione.query.filter_by(profilo='assegnista_roma3').count(),
            'cultori': Commissione.query.filter_by(profilo='cultore_roma3').count(),
            'docenti_contratto': Commissione.query.filter_by(profilo='docente_contratto').count(),
            'tutor': Commissione.query.filter_by(profilo='tutor_coordinatore').count(),
            'ref_usr': Commissione.query.filter_by(profilo='referente_usr').count(),
            'esterni': Commissione.query.filter_by(profilo='esterno_altro').count()
        }
    }
    
    return render_template('index.html', 
                         esami=esami, 
                         stats=stats,
                         classi_concorso=CLASSI_CONCORSO,
                         search=search,
                         classe_filter=classe_filter,
                         modalita_filter=modalita_filter)

# scarica_excel() - Funzione corretta
@app.route('/scarica_excel')
def scarica_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Esami PEF"
    
    # Headers
    headers = ['ID', 'Classe Concorso', 'Percorso PEF', 'Data Inizio', 'Data Fine', 'Modalità', 'Sede', 'Note', 'Commissione', 'Date Aggiuntive']
    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)
    
    esami = Esame.query.all()
    for row, esame in enumerate(esami, 2):
        ws.cell(row=row, column=1, value=esame.id)
        ws.cell(row=row, column=2, value=dict(CLASSI_CONCORSO).get(esame.classe_concorso, esame.classe_concorso))
        
        # Gestione percorsi multipli
        percorsi_nomi = [dict(PERCORSI_PEF).get(p, p) for p in esame.get_percorsi_list()]
        percorsi_str = ', '.join(percorsi_nomi)
        ws.cell(row=row, column=3, value=percorsi_str)

        # Verifica che data_inizio e data_fine esistano
        if hasattr(esame, 'data_inizio') and esame.data_inizio:
            ws.cell(row=row, column=4, value=esame.data_inizio.strftime('%d/%m/%Y %H:%M'))
        else:
            ws.cell(row=row, column=4, value='Non definita')
            
        if hasattr(esame, 'data_fine') and esame.data_fine:
            ws.cell(row=row, column=5, value=esame.data_fine.strftime('%d/%m/%Y %H:%M'))
        else:
            ws.cell(row=row, column=5, value='Non definita')
            
        ws.cell(row=row, column=6, value=esame.modalita)
        ws.cell(row=row, column=7, value=esame.sede or '')
        ws.cell(row=row, column=8, value=esame.note or '')
        
        # Commissione
        commissione_str = '; '.join([
            f"{c.nome_membro} {c.cognome_membro} ({c.ruolo}, {c.tipologia})"
            for c in esame.commissioni
        ])
        ws.cell(row=row, column=9, value=commissione_str)
        
        # Date aggiuntive (ora chiamate calendario_esami)
        calendario = getattr(esame, 'calendario_esami', [])
        date_agg_str = '; '.join([
            f"{d.data_inizio.strftime('%d/%m/%Y %H:%M')} - {d.data_fine.strftime('%d/%m/%Y %H:%M')} ({d.modalita}) - {dict(TIPI_ATTIVITA).get(getattr(d, 'attivita', 'altro'), 'Non specificato')}" 
            for d in calendario
        ])
        ws.cell(row=row, column=10, value=date_agg_str)
    
    # Salva il file temporaneo
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.xlsx') as f:
        wb.save(f.name)
        temp_path = f.name
    
    return send_file(temp_path, as_attachment=True, download_name='esami_pef.xlsx', 
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# calendario() - Funzione corretta
@app.route('/calendario')
def calendario():
    """Visualizza tutte le date degli esami in formato calendario"""
    # Ottieni tutti gli esami con le loro date principali e del calendario
    esami = Esame.query.all()
    
    # Prepara gli eventi per il calendario
    eventi = []
    
    for esame in esami:
        # Aggiungi data principale dell'esame
        if esame.data_inizio:
            classe_concorso_nome = dict(CLASSI_CONCORSO).get(esame.classe_concorso, esame.classe_concorso)
            percorsi_str = ', '.join([dict(PERCORSI_PEF).get(p, p) for p in esame.get_percorsi_list()])
            
            # Evento principale
            eventi.append({
                'id': f'esame_{esame.id}',
                'title': f"{classe_concorso_nome}",
                'description': f"{percorsi_str} - {esame.note or ''}",
                'start': esame.data_inizio.isoformat(),
                'end': esame.data_fine.isoformat() if esame.data_fine else None,
                'url': url_for('dettaglio_esame', id=esame.id),
                'color': '#3788d8',  # Blu per eventi principali
                'textColor': '#ffffff',
                'allDay': False
            })
        
        # Aggiungi date del calendario esami
        for data in esame.calendario_esami:
            attivita_nome = dict(TIPI_ATTIVITA).get(data.attivita, 'Altro')
            eventi.append({
                'id': f'calendario_{data.id}',
                'title': f"{classe_concorso_nome} - {attivita_nome}",
                'description': f"{percorsi_str} - {data.sede or ''}",
                'start': data.data_inizio.isoformat(),
                'end': data.data_fine.isoformat(),
                'url': url_for('dettaglio_esame', id=esame.id),
                'color': '#28a745',  # Verde per date aggiuntive
                'textColor': '#ffffff',
                'allDay': False
            })
    
    return render_template('calendario.html', eventi=eventi)
