def migrate(cr, version):
    # Rename the lone Spanish strategy key to match the English keys
    cr.execute("UPDATE qms_hazard SET strategy = 'avoid' WHERE strategy = 'evitar'")
